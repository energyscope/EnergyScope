# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 22:26:29 2020

Contains functions to read data in csv files and print it with AMPL syntax in ESTD_data.dat
Also contains functions to analyse input data

@author: Paolo Thiran
"""
import logging

import numpy as np
import pandas as pd
import csv
import yaml
import os
import sys
import json
import shutil
from subprocess import CalledProcessError, run
from pathlib import Path

from energyscope import ampl_syntax, print_set, print_df, newline, print_param, print_header, print_run


# TODO
#  write doc
#  add step1 and reading of weights
#  add possibility to run with amplpy
#  fix sto_year print


def print_json(my_sets, file):  # printing the dictionary containing all the sets into directory/sets.json
    with open(file, 'w') as fp:
        json.dump(my_sets, fp, indent=4, sort_keys=True)
    return


def read_json(file):
    # reading the saved dictionary containing all the sets from directory/sets.json
    with open(file, 'r') as fp:
        data = json.load(fp)
    return data


def load_config(config_fn: str, project_path: Path):
    """
    Load the configuration into a dict.

    Parameters
    ----------
    config_fn: str
    configuration file name.

    project_path: pathlib.Path
    path to project EnergyScope

    Returns
    -------
    A dict with the configuration.
    """

    # Load parameters
    #print(config_fn)
    cfg = yaml.load(open(os.path.join(project_path, config_fn ), 'r'), Loader=yaml.FullLoader)
    # Extend path
    for param in ['data_dir', 'es_path', 'cs_path', 'step1_path']:
        cfg[param] = project_path / cfg[param]

    # Extend path for log_file
    #print(str(cfg['case_study'] / cfg['ampl_options']['log_file']))
    #print(os.path.join(config_fn['case_studies'], config_fn['case_study']))
    #cfg['ampl_options']['log_file'] = os.path.join(config_fn['case_studies'], config_fn['case_study'], cfg['ampl_options']['log_file'])#str(cfg['case_studies'] / cfg['case_study'] / cfg['ampl_options']['log_file'])

    return cfg


def import_data(config: dict):
    """
    Read the data into the csv and the misc.json into the data directory (config['data_dir'])
    and stores it into 2 dictionaries in the config (config['all_data'] and config['all_data']['Misc']).
    The data of the different csv are stored into dataframes and the miscallenous data of the user_defined is stored as
    dictionnary of different items

    Parameters
    ----------
    config : dict
    Dictionnary containing all the configurations to run the current case study of EnergyScope.
    For this function to work, it must contain and item of type pathlib.Path into the key 'data_dir'

    """

    data_dir = config['data_dir']
    logging.info('Importing data files from ' + str(data_dir))
    # Reading CSV #
    eud = pd.read_excel(data_dir / 'Demand.xlsx', index_col=2, header=0)
    resources = pd.read_excel(data_dir / 'Resources.xlsx', index_col=2, header=2)
    technologies = pd.read_excel(data_dir / 'Technologies.xlsx', index_col=3, header=0, skiprows=[1])
    end_uses_categories = pd.read_csv(data_dir / 'END_USES_CATEGORIES.csv', sep='\t')
    layers_in_out = pd.read_excel(data_dir / 'Layers_in_out.xlsx', index_col=0)
    storage_characteristics = pd.read_excel(data_dir / 'Storage_characteristics.xlsx', index_col=0)
    storage_eff_in = pd.read_excel(data_dir / 'Storage_eff_in.xlsx', index_col=0)
    storage_eff_out = pd.read_excel(data_dir / 'Storage_eff_out.xlsx', index_col=0)
    time_series = pd.read_excel(data_dir / 'Time_series.xlsx', header=0, index_col=0)

    # Reading misc.json
    misc = read_json(data_dir / 'misc.json')

    # Pre-processing #
    resources.drop(columns=['Comment'], inplace=True)
    resources.dropna(axis=0, how='any', inplace=True)
    technologies.drop(columns=['Comment'], inplace=True)
    technologies.dropna(axis=0, how='any', inplace=True)
    # cleaning indices and columns

    all_df = {'Demand': eud, 'Resources': resources, 'Technologies': technologies,
              'End_uses_categories': end_uses_categories, 'Layers_in_out': layers_in_out,
              'Storage_characteristics': storage_characteristics, 'Storage_eff_in': storage_eff_in,
              'Storage_eff_out': storage_eff_out, 'Time_series': time_series,
              }

    for key in all_df:
        if type(all_df[key].index[0]) == str:
            all_df[key].index = all_df[key].index.str.strip()
        if type(all_df[key].columns[0]) == str:
            all_df[key].columns = all_df[key].columns.str.strip()

    all_df['Misc'] = misc

    config['all_data'] = all_df

    return

