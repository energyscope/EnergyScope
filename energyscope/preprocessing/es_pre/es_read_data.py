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


def load_config(config_fn: str):
    """
    Load the configuration into a dict.

    Parameters
    ----------
    config_fn: str
    configuration file name.

    Returns
    -------
    A dict with the configuration.
    """
    # define project path
    project_path = Path(__file__).parents[3]
    
    # Load parameters
    cfg = yaml.load(open(config_fn, 'r'), Loader=yaml.FullLoader)
    # Extend path
    for param in ['data_dir', 'es_path', 'cs_path', 'step1_path']:
        cfg[param] = project_path / cfg[param]

    # Extend path for log_file
    cfg['ampl_options']['log_file'] = str(cfg['cs_path'] / cfg['case_study'] / cfg['ampl_options']['log_file'])

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
    eud = pd.read_csv(data_dir / 'Demand.csv', sep=';', index_col=2, header=0)
    resources = pd.read_csv(data_dir / 'Resources.csv', sep=';', index_col=2, header=2)
    technologies = pd.read_csv(data_dir / 'Technologies.csv', sep=';', index_col=3, header=0, skiprows=[1])
    end_uses_categories = pd.read_csv(data_dir / 'END_USES_CATEGORIES.csv', sep=';')
    layers_in_out = pd.read_csv(data_dir / 'Layers_in_out.csv', sep=';', index_col=0)
    storage_characteristics = pd.read_csv(data_dir / 'Storage_characteristics.csv', sep=';', index_col=0)
    storage_eff_in = pd.read_csv(data_dir / 'Storage_eff_in.csv', sep=';', index_col=0)
    storage_eff_out = pd.read_csv(data_dir / 'Storage_eff_out.csv', sep=';', index_col=0)
    time_series = pd.read_csv(data_dir / 'Time_series.csv', sep=';', header=0, index_col=0)

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

