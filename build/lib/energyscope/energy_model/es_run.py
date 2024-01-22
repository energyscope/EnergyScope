# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:18:00 2023

Script containing the function to run EnergyScope (es)

@author: Paolo Thiran
"""

import logging
import os
import sys
import shutil
from subprocess import CalledProcessError, run
from pathlib import Path

#from energyscope import print_run

def run_es(config):
    """

    :param config: configuration
    :return:
    """
    two_up = Path(__file__).parents[2]

    cs = two_up / 'case_studies'
    run_file = 'ESTD_main.run'

    # creating output directory
    (cs / config['case_study'] / 'output').mkdir(parents=True, exist_ok=True)
    (cs / config['case_study'] / 'output' / 'hourly_data').mkdir(parents=True, exist_ok=True)
    (cs / config['case_study'] / 'output' / 'sankey').mkdir(parents=True, exist_ok=True)

    # using AMPL_path if specified. Otherwise, we assume ampl is in environment variables
    if config['AMPL_path'] is None:
        ampl_command = 'ampl ' + run_file
        # call('ampl '+run, shell=True)
    else:
        config['AMPL_path'] = Path(config['AMPL_path'])
        print('AMPL path is', config['AMPL_path'])
        config['ampl_options']['solver'] = config['AMPL_path'] / config['ampl_options']['solver']
        ampl_command = str(config['AMPL_path'] / 'ampl ') + run_file

    # copy .mod to case_study directory
    shutil.copyfile((config['es_path'] / 'es_model.mod'), (cs / config['case_study'] / 'es_model.mod'))
    # list printing files to consider according to config
    ampl_run_dir = Path(__file__).parent / 'run'
    print_files = [str(ampl_run_dir / 'print_year_summary.run')]
    if config['print_hourly_data']:
        print_files.append(str(ampl_run_dir / 'print_hourly_data.run'))
    if config['print_sankey']:
        print_files.append(str(ampl_run_dir / 'print_sankey.run'))
    # print .run to case_study directory
    print_run(run_fn=(cs / config['case_study'] / run_file), mod_fns=[(cs / config['case_study'] / 'es_model.mod')],
              dat_fns=[(cs / config['case_study'] / 'ESTD_data.dat'),
                       (cs / config['case_study'] / ('ESTD_' + str(config['nbr_td']) + 'TD.dat'))],
              options=config['ampl_options'], output_dir=(cs / config['case_study'] / 'output'),
              print_files=print_files)

    os.chdir((cs / config['case_study']))
    # running ES
    logging.info('Running EnergyScope')

    try:
        run(ampl_command, shell=True, check=True)
    except CalledProcessError as e:
        print("The run didn't end normally.")
        print(e)
        sys.exit(1)

    os.chdir(config['Working_directory'])

    logging.info('End of run')

    return
