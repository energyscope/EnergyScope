# -*- coding: utf-8 -*-
"""
This function proceeds to the clustering according to a given number of typical days

@author: Paolo Thiran, Pierre Jacques
"""

import os
import logging
import numpy as np
import pandas as pd
import sys
from pathlib import Path
from subprocess import CalledProcessError, run


from energyscope import ampl_syntax, print_set, print_df, newline, print_param, print_header, print_run


def build_td_of_days(config):
    """Assigns a typical day to each of the 365 days of the year and prints the
      result in a .dat file
    
    Parameters
    ----------
    config :   dict
               contains all the information about the energy system and the 
               optimization problem solved by EnergyScope

    Returns
    ----------
    Returns none.
    Creates the .dat files 'td_of_days.out' and 'TD_of_days_XX.out' in the
    data_dir directory
    """
    all_data = config['all_data']
    
    # pivot ts to have (365x(24*N_ts))
    n_daily_ts = pivot_ts(all_data['Time_series'].copy())
    weights = pd.DataFrame()
    compute_cell_w(all_data, weights)
    normalize_weights(weights)
    n_data = weight(weights, n_daily_ts)
    
    # run clustering algorithm
    td_of_days = kmedoid_clustering(config, n_data, weights)
    td_of_days.to_csv(config['step1_path'] / 'td_of_days.out', index=False, header=False)
    return


def pivot_ts(ts):
    """Pivot time series in daily format
    Transforms the time series in the data to have normalized daily time series of shape (365x(N_ts*24))
    
    Parameters
    ----------
    ts : pd.DataFrame()
        Time series to pivot under the form (365xN_ts)
    
    Returns
    ----------
    Normalized and pivoted time series in the daily format (365x(N_ts*24))
    """
    ###### THE FOLLOWING LINE MIGHT NEED TO BE ADAPTED ######
    ts.rename(columns={'Electricity (%_elec)': 'LIGHTING', 'Space Heating (%_sh)': 'HEAT_LOW_T_SH'}, inplace=True)
    ts_names = ts.columns
    # normalize the timeseries
    ts = ts/ts.sum()
    # adding columns for pivoting
    ts['Days'] = np.repeat(np.arange(1, 366), 24, axis=0)
    ts['H_of_D'] = np.resize(np.arange(1, 25), ts.shape[0])
    # pivoting normalized time series (norm_ts) to get daily normalized time series (n_daily_ts)
    n_daily_ts = ts.pivot(index='Days', columns='H_of_D', values=ts_names)
    return n_daily_ts.fillna(0)


def compute_cell_w(all_data, weights):
    """Compute the weight of each time series (Cell_w).
    To compute the weights, the importance of each time series is defined as 
    the yearly demand for energy demands and as potential yearly production at 
    full scale deployment for renewable energies.
            
    Parameters
    ----------
    all_data: dict
              contains the input data for the optimization problem solved by 
              EnergyScope. 
    weights : pandas data frame
              empty data frame to which the computed weights will be appended
              as the column 'Cell_w'.
    """
    tot_ts = all_data['Time_series'].sum(axis=0)
    ###### THE FOLLOWING 4 LINES MIGHT NEED TO BE ADAPTED ######
    demand_ts = ['LIGHTING', 'HEAT_LOW_T_SH']
    prod_ts = ['PV', 'Wind_onshore', 'Wind_offshore', 'Hydro_river']
    prod_ts2 = ['PV', 'WIND_ONSHORE', 'WIND_OFFSHORE', 'HYDRO_RIVER']
    tot_ts.rename({'Electricity (%_elec)': 'LIGHTING', 'Space Heating (%_sh)': 'HEAT_LOW_T_SH'}, inplace=True)
    
    # multiply demand time series sum by the year consumption
    tot_ts[demand_ts] = tot_ts[demand_ts] * all_data['Demand'].loc[demand_ts, :].sum(axis=1, numeric_only=True).values
    
    # Weight the heating time series by a conversion coefficient to
    # account for the difference in energy quality compared to the electricity
    # time series
    tot_ts.loc['HEAT_LOW_T_SH'] *= 0.204

    # multiply the sum of the production time series by the maximum potential
    # (f_max in GW) of the corresponding technologies
    tot_ts[prod_ts] = tot_ts[prod_ts] * all_data['Technologies'].loc[prod_ts2, 'f_max'].values
    tot_ts.loc[~tot_ts.index.isin(demand_ts+prod_ts)] = np.nan
    
    # Add Cell_w to the weights data frame
    weights['Cell_w'] = tot_ts
    return 


def normalize_weights(weights):
    """Normalize the weights so that their sum equals 1 and the sum of 
    weights related to resp. production or demand each equals 0.5
    The results are stored in a new column of the weights attribute called 'Weights_n'
    """
    ###### THE FOLLOWING 2 LINES MIGHT NEED TO BE ADAPTED ######
    demand_ts = ['LIGHTING', 'HEAT_LOW_T_SH']
    prod_ts = ['PV', 'Wind_onshore', 'Wind_offshore', 'Hydro_river']
    
    demand_total = weights.loc[demand_ts, 'Cell_w'].sum()
    prod_total = weights.loc[prod_ts, 'Cell_w'].sum()
    weights['Weights_n'] = weights['Cell_w'] 
    weights.loc[weights['Weights_n'] < 0.001, 'Weights_n'] = np.nan
    weights.loc[demand_ts, 'Weights_n'] = weights.loc[demand_ts, 'Weights_n'] / demand_total / 2
    weights.loc[prod_ts, 'Weights_n'] = weights.loc[prod_ts, 'Weights_n'] / prod_total / 2
    return


def weight(weights, n_daily_ts):
    """Weighting the normalized daily time series
    The normalized daily concatenated time series (n_daily_ts) are weighted by the normalized weights
    (weights['Weights_n']).
    The time series with no weight or a null weight are dropped.
    The result (n_data) is ready to be used in a clustering algorithm and is of shape (365x(len(non_null_weights)*24))
    """
    # use numpy broadcasting to multiply each time series by its weight
    n_data = numpy_broadcasting(weights.loc[:, 'Weights_n'], n_daily_ts.transpose())
    # drop ts without weight
    n_data.dropna(axis=0, how='any', inplace=True)
    return n_data.transpose()  # transpose to the form (365x(n_ts*24))
    

def print_dat(dat_file, n_data, weights, nbr_td):
    """
    dat_file = path to the .dat file
    Returns
    -------
    """
    # set n_data columns index to numerical index
    n_data.columns = np.arange(1, n_data.shape[1] + 1)
    # printing signature of data file
    print_header(Path(__file__).parent/'header.txt', dat_file)
    newline(dat_file)
    # printing SET DIMENSIONS
    print_set(my_set=[str(i) for i in n_data.columns], out_path=dat_file, name='DIMENSIONS')
    # printing Nbr_TD
    print_param('Nbr_TD', nbr_td, '', dat_file)
    newline(dat_file)
    # printing weights as a comment
    weights = weights.reset_index().rename(columns={'index': 'Time series'})
    weights['#'] = '#'
    weights = weights[['#', 'Time series', 'Cell_w', 'Weights_n']]
    weights.to_csv(dat_file, sep='\t', header=True, index=False, mode='a')
    newline(dat_file)
    # printing param n_data in ampl syntax
    print_df(df=ampl_syntax(n_data, ''), out_path=dat_file, name='param Ndata :')
    return


def kmedoid_clustering(config, n_data, weights):
    """
    Returns
    -------
    """
    # extract info of interest from config
    nbr_td = config['nbr_td']
    step1_path = config['step1_path']
    
    # define path
    mod_path = step1_path / 'td_main.mod'
    data_path = step1_path / 'data.dat'
    log_file = step1_path / 'log.txt'
    run_file = 'td_main.run'

    # logging info
    logging.info('Starting kmedoid clustering of typical days based on ' + str(data_path))
    
    # print .dat file
    print_dat(data_path, n_data, weights, nbr_td)

    # define options
    cplex_options = ['mipdisplay=5',
                     'mipinterval=1000',
                     'mipgap=1e-6']
    cplex_options_str = ' '.join(cplex_options)
    options = {'show_stats': 3,
               'log_file': str(log_file),
               'times': 1,
               'gentimes': 1,
               'solver': 'cplex',
               'cplex_options': cplex_options_str}

    # using AMPL_path if specified. Otherwise, we assume ampl is in environment variables
    if config['AMPL_path'] is None:
        ampl_command = 'ampl ' + run_file
    else:
        config['AMPL_path'] = Path(config['AMPL_path'])
        print('AMPL path is', config['AMPL_path'])
        options ['solver'] = config['AMPL_path'] / options ['solver']
        ampl_command = str(config['AMPL_path'] / 'ampl ') + run_file

    # print .run
    print_run(run_fn=str(step1_path / run_file), mod_fns=[str(mod_path)],
              dat_fns=[str(data_path)],
              options=options, output_dir=step1_path,
              print_files=['printing_outputs.run'])

    os.chdir(step1_path)
    # running ES
    logging.info('Running kmedoid clustering')

    try:
        run(ampl_command, shell=True, check=True)
    except CalledProcessError as e:
        print("The run didn't end normally.")
        print(e)
        sys.exit(1)

    td_of_days = pd.read_csv('td_of_days.out', header=None)

    os.chdir(config['Working_directory'])

    logging.info('End of kmedoid clustering')

    return td_of_days


def numpy_broadcasting(df0, df1):
    """
    Multiplies 2 multiindexed pandas dataframes of different dimensions using numpy broadcasting
    Used to multiply each hour of each day for each time series by its respective weight
    Parameters
    ----------
    df0: pd.Series()
        Multiindexed dataframe containing the normalized weights of the time series
        (df0.index.levshape = n_ts)
    df1: pd.DataFrame()
        Multiindexed dataframe containing the times series under the form:
        df1.index.levshape = (n_ts, 24), df1.shape[1] = 365
    Returns
    -------
    df_out: pd.DataFrame()
        Multiindexed dataframe (same shape as df1), product of df1 by df0.
        For each time series, all the hours of all the days are multiplied by the normalized weight (df0)
    """
    m, n = map(len, df1.index.levels)
    a0 = df0.values.reshape(m, -1)
    a1 = df1.values.reshape(m, n, -1)
    out = (a1 * a0[..., None, :]).reshape(-1, a1.shape[-1])
    df_out = pd.DataFrame(out, index=df1.index, columns=df1.columns)
    return df_out
