# -*- coding: utf-8 -*-
"""
This script modifies the input data and runs the EnergyScope model

@author: Louis Merceron based on previous work by Paolo Thiran, Matija Pavičević, Xavier Rixhon, Gauthier Limpens
"""

import os
from pathlib import Path
import energyscope as es
import matplotlib.pyplot as plt
import warnings
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    analysis_only = False
    compute_TDs = False

    # define project path
    project_path = Path(__file__).parents[0]

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)

    config['Working_directory'] = os.getcwd() # keeping current working directory into config
    #config['case_studies'] = os.path.join(os.getcwd(),'case_studies', 'ECOS', 'test', 'base_case')#, 'YEEES', 'scenarios')
    config['case_studies'] = os.path.join(os.getcwd(),'case_studies', 'paper1', 'base_case')#'import_analysis', 'scenarios_jetfuel_import_price_emi_reduc_ft100')
    config['case_study'] = '70_ebiofuel'



    config['ampl_options']['log_file'] = os.path.join(config['case_studies'], config['case_study'], config['ampl_options']['log_file'])
    
    # Reading the data of the csv
    es.import_data(config)

    if compute_TDs:
        es.build_td_of_days(config)
   
    if not analysis_only:
        # Printing the .dat files for the optimisation problem       
        es.print_data(config)

        # Running EnergyScope
        es.run_es(config)

    # Example to print the sankey from this script
    
    print(config)

    # Reading outputs
    #outputs = es.read_outputs(config)
    outputs = es.read_outputs(config, hourly_data=True, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN','layer_HEAT_LOW_T_DHN', 'layer_HEAT_HIGH_T', 'layer_AMMONIA', 'layer_H2', 'layer_LFO' , 'layer_GAS', 'layer_JETFUEL', 'layer_FT_FUEL'])

    #To print the Sankey diagrams 
    print_sankey = True
    if print_sankey == True:
        fig = es.Sankey_plot(outputs['year_balance'], outputs['sto_year'])
        fig.update_layout(width=3000, height=1800)
        fig.update_layout(font=dict(size=22, color='black'))
        fig.show()

        fig = es.Sankey_carbon(outputs['year_balance'], outputs['gwp_breakdown'])
        fig.update_layout(width=2500, height=1500)
        fig.update_layout(font=dict(size=22, color='black'))
        fig.show()
        print('Total cost of the system (MEUR/year)', outputs['cost_breakdown']['C_inv'].sum() + outputs['cost_breakdown']['C_maint'].sum() +outputs['cost_breakdown']['C_op'].sum())
        print('Total electricity production (TWh/year)', outputs['year_balance'].loc[outputs['year_balance'].loc[:,'ELECTRICITY' ].ge(100),'ELECTRICITY' ].sum())

    # To print the layer balance for the different typical days for different energies
    print_layer_balance_elec = True
    if print_layer_balance_elec == True :
        elec_layer_plot = es.plot_layer_balance_td(outputs['layer_ELECTRICITY'])
        elec_layer_plot.show() 
    print_layer_balance_other = False
    if print_layer_balance_other == True :
        heat_low_t_decen_layer_plot = es.plot_layer_balance_td(outputs['layer_HEAT_LOW_T_DECEN'])
        heat_low_t_decen_layer_plot.show() 
        heat_low_t_dhn_layer_plot = es.plot_layer_balance_td(outputs['layer_HEAT_LOW_T_DHN'])
        heat_low_t_dhn_layer_plot.show() 
        heat_high_t_layer_plot = es.plot_layer_balance_td(outputs['layer_HEAT_HIGH_T'])
        heat_high_t_layer_plot.show() 
        heat_h2_layer_plot = es.plot_layer_balance_td(outputs['layer_H2'])
        heat_h2_layer_plot.show() 
        heat_ammonia_layer_plot = es.plot_layer_balance_td(outputs['layer_AMMONIA'])
        heat_ammonia_layer_plot.show() 
        heat_ammonia_layer_plot = es.plot_layer_balance_td(outputs['layer_FT_FUEL'])
        heat_ammonia_layer_plot.show() 
    # Print the evolution of the energy stored with different energy vectors over the entire year
    print_energy_stored = False
    if print_energy_stored == True :
        energy_stored = es.plot_energy_stored(outputs['energy_stored'])
        energy_stored.show()
        

    # Print the pie chart of the repartition of the cost of the system 
    plot_cost_system = False
    if plot_cost_system == True :
        fig = es.plot_total_cost_system (outputs)
        fig.show()
        share_ghg_construction = es.plot_share_ghg_construction (outputs)
        share_ghg_construction.show()

    print_load_factor = True
    if print_load_factor == True:
        es.compute_load_factors(outputs)
    


    

    
    