import logging

import pandas as pd
from pathlib import Path

from ..common import *

def read_outputs(cs:str, hourly_data=False, layers=[]):
    """Reads the EnergyScope outputs in the case study (cs) specified
    Parameters
    ----------
    cs : str
    Case study to read output from

    hourly_data: boolean (default False)
    Whether to read the hourly data ouput or not

    layers: list(str)
    List of the names of the layers to be read (ex: ['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN'])

    Returns
    -------
    outputs: dict()
    Dictionnary containing the different output dataframes as pd.DataFrame
    """
    path = Path(__file__).parents[2]/'case_studies'/str(cs)/'output'

    logging.info('Reading outputs from: '+str(path))
    outputs = dict()
    outputs['assets'] = pd.read_csv(path/'assets.txt', sep="\t", skiprows=[1], index_col=False).set_index('TECHNOLOGIES')
    outputs['assets'].dropna(how='all', axis=1, inplace=True)
    outputs['cost_breakdown'] = pd.read_csv(path/'cost_breakdown.txt', sep='\t', index_col=0)
    outputs['gwp_breakdown'] = pd.read_csv(path/'gwp_breakdown.txt', sep='\t', index_col=0)
    outputs['losses'] = pd.read_csv(path/'losses.txt', sep='\t', index_col=0)
    outputs['resources_breakdown'] = pd.read_csv(path/'resources_breakdown.txt', sep='\t', index_col=0)
    outputs['year_balance'] = pd.read_csv(path/'year_balance.txt', sep='\t', index_col=0).dropna(how='all', axis=1)

    for o in outputs:
        outputs[o] = clean_col_and_index(outputs[o])

    if hourly_data:
        outputs['energy_stored'] = pd.read_csv(path/'hourly_data'/'energy_stored.txt', sep='\t', index_col=0)
        for l in layers:
            outputs[l] = read_layer(cs,l)
    return outputs

def read_layer(cs:str, layer_name, ext='.txt'):
    """Reads the output file of the layer specified and returns it as a dataframe

        Parameters
        ----------
        cs : str
        Case study to read output from

        : pd.DataFrame()
        Dataframe to be cleaned

        Returns
        -------
        df2: pd.DataFrame()
        The stripped dataframe
    """

    layer = pd.read_csv(Path(__file__).parents[2]/'case_studies'/str(cs)/'output' / 'hourly_data' / (layer_name+ext), sep='\t',
                                               index_col=[0, 1])
    return clean_col_and_index(layer)



def clean_col_and_index(df):
    """Strip the leading and trailing white space in columns and index

        Parameters
        ----------
        df: pd.DataFrame()
        Dataframe to be cleaned

        Returns
        -------
        df2: pd.DataFrame()
        The stripped dataframe
        """
    df2 = df.copy()
    if df2.columns.inferred_type == 'string':
        df2.rename(columns=lambda x: x.strip(), inplace=True)
    if df2.index.inferred_type == 'string':
        df2.rename(index=lambda x: x.strip(), inplace=True)
    return df2


def rename_storage_power(s):
    """Rename storage input and output power to plotting name

     Parameters
    ----------
    s: str
    String to be renamed should be of the form "XXX_in" or "XXX_out" with "XXX" the name of the storage technology in capital letters.

    Returns
    -------
    A string with the plotting name corresponding to the storage technology and the "in" or "out"

    """

    l = s.rsplit(sep='_')
    name = plotting_names['_'.join(l[:-1])]
    suffix = l[-1]
    return name + ' ' + suffix

def from_td_to_year(ts_td, t_h_td):
    """Converts time series on TDs to yearly time series

    Parameters
    ----------
    ts_td: pandas.DataFrame
    Multiindex dataframe of hourly data for each hour of each TD.
    The index should be of the form (TD_number, hour_of_the_day).

    t_h_td: pandas.DataFrame


    """
    td_h = t_h_td.loc[:,['TD_number','H_of_D']]
    ts_yr = td_h.merge(ts_td, left_on=['TD_number','H_of_D'], right_index=True).sort_index()
    return ts_yr.drop(columns=['TD_number', 'H_of_D'])


def get_assets_l(layer: str, eff_tech: pd.DataFrame, assets: pd.DataFrame, treshold=0.05):
    """Get the assets' characteristics of the specified layer
    The installed capacity is in the units of the specified layer

    Parameters
    ----------
    layer: str
    Name of the layer to consider

    eff_tech: pd.DataFrame
    Layers_in_out withtout the resources rows (i.e. the conversion efficiencies of all the technologies)

    assets: pandas.DataFrame
    Assets dataframe (as outputted by the model),
    i.e. rows=technologies, columns=[c_inv, c_maint, lifetime, f_min, f, f_max, fmin_perc, f_perc, fmax_perc, c_p, c_p_max, tau, gwp_constr]

    treshold: float, default=0.1
    Treshold to select efficiencies of tech. Default gives producing technologies.
    Set to negative value (ex:-0.05) to get consuming technologies)

    Returns
    -------
    df: pd.DataFrame
    Assets' characteristics of the specified layer
    i.e. rows=technologies of the layer, columns=[c_inv, c_maint, lifetime, f_min, f, f_max, fmin_perc, f_perc, fmax_perc, c_p, c_p_max, tau, gwp_constr]

    """
    # take the tech and resources that produce something on the layer
    tech = list(eff_tech.loc[eff_tech.loc[:,layer]>treshold,:].index)
    # drop the resources
    tech = [i for i in tech if i in list(assets.index)]
    # select the assets
    df = assets.loc[tech,:].copy()
    # scale the assets tho their efficiency
    df.loc[tech, 'f'] = df.loc[tech,'f'] * eff_tech.loc[tech, layer]
    return df