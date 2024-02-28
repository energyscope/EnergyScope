import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import energyscope as es

analysis_sensibility_only = False
for j in range(40, 50, 10):
    ft_share = j
    if analysis_sensibility_only == False:
        
        # define project path
        project_path = Path(__file__).parents[0]
        
        # define the parameter to do a variation on
        # either using an excel file or 
        
        # numbers define in a list
        biomass_avail = [i for i in range (150, 620, 50)]*10
        sequ_avail = []
        [sequ_avail.extend([j] * 10) for j in range (0, 75, 7)]
        import_avail = [i for i in range (0, 100, 23)]
        price_import = [j for j in range (90, 350, 5)]


        share_jetfuel_refinery = [30, 40, 50, 60, 70, 80, 90, 100]
        share_gasoline_refinery = [35, 30, 25, 20, 15, 10, 5,  0]
        share_diesel_refinery = [35, 30, 25, 20, 15, 10, 5, 0]

        #
        import_fuel_price = [i for i in range (50, 605, 10)]*3
        share_emission_reduction = []
        [share_emission_reduction.extend([j] * 56) for j in [-10, 90, 290]]

        share_nuc = [i for i in range (0, 70, 10)]*5
        share_PV = [30, 40, 50, 60, 70]
        max_storage_h2 = []
        [max_storage_h2.extend([j]*7 ) for j in range (30, 80, 10)]
        for case_number in range(0, 1000):
            print('--------------------------', case_number, '---------------------------------')
            analysis_only= False
            compute_TDs = False
            # loading the config file into a python dictionnary
            config = es.load_config(config_fn='config_ref.yaml', project_path=project_path) #'import_analysis', 'scenarios_jetfuel_import_price_2'#'analyis_impact_share_jet_fuel_produced', 'no_import'
            #config['case_studies'] = os.path.join(project_path,'case_studies', 'paper1', 'import_analysis', 'scenarios_jetfuel_import_price_emi_reduc_2')#, )##
            config['case_studies'] = os.path.join(project_path,'case_studies', 'paper1', 'import_analysis', 'jetfuel_import_price_ft'+str(j))
            config['case_study'] = 'scenario_' + str(case_number+1)
            config['Working_directory'] = os.getcwd() # keeping current working directory into config
            config['print_hourly_data'] = False
            
            # Reading the data of the csv
            es.import_data(config)

            # Change the value in the data
            #Value_bm_qtt = biomass_avail[case_number]#sensibility_data['BIOMASS_QTT'].iloc[case_number]
            Value_bm_use = 0#sensibility_data['BIOMASS_USE'].iloc[case_number]
            #Value_cap_sequ = sequ_avail[case_number]#sensibility_data['CAP_SEQU'].iloc[case_number]
            # For analysis on the quantity imported in relation with import price  
            config['all_data']['Resources'].loc['JETFUEL_RE', 'avail'] = 910000#import_avail[case_number]*1000
            config['all_data']['Resources'].loc['JETFUEL_RE', 'c_op'] = import_fuel_price[case_number]/1000
            config['all_data']['Layers_in_out'].loc['JETFUEL_RE', 'CO2_ATMOSPHERE'] = -share_emission_reduction[case_number]*0.26/100
            config['all_data']['Layers_in_out'].loc['REFINERY_JETFUEL', 'JETFUEL'] = j/100
            config['all_data']['Layers_in_out'].loc['REFINERY_JETFUEL', 'GASOLINE'] = (100-j)/200
            config['all_data']['Layers_in_out'].loc['REFINERY_JETFUEL', 'DIESEL'] = (100-j)/200
            print(case_number, import_fuel_price[case_number], share_emission_reduction[case_number])

            # For analysis on the share of nuclear 
            """config['all_data']['Technologies'].loc['NUCLEAR', 'f_max'] = share_nuc[case_number]
            #config['all_data']['Technologies'].loc['H2_STORAGE', 'f_max'] = max_storage_h2[case_number]
            config['all_data']['Technologies'].loc['PV', 'f_max'] = 800
            config['all_data']['Technologies'].loc['WIND_ONSHORE', 'f_max'] = 300
            config['all_data']['Technologies'].loc['WIND_OFFSHORE', 'f_max'] = 240
            config['all_data']['Technologies'].loc['PV', 'fmax_perc'] = max_storage_h2[case_number]/100
            config['all_data']['Technologies'].loc['WIND_ONSHORE', 'fmax_perc'] = (100-max_storage_h2[case_number])/200
            config['all_data']['Technologies'].loc['WIND_OFFSHORE', 'fmax_perc'] = (100-max_storage_h2[case_number])/200
            config['print_hourly_data'] = True"""

            # For analysis on biomass and sequestration availability
            """config['all_data']['Technologies'].loc['WOOD_GROWTH', 'f_max'] = Value_bm_qtt * 0.66 / 8.760
            config['all_data']['Technologies'].loc['WET_BIOMASS_GROWTH', 'f_max'] = Value_bm_qtt * 0.34 / 8.760
            config['all_data']['Misc']['min_biomass_use_dec_heat_lt'] = Value_bm_use * 1000 *0.585 #Energy for DEC change 563 if change heat_LT Industry 
            config['all_data']['Misc']['min_biomass_use_dhn_heat_lt'] = Value_bm_use * 1000 *0.10  #Energy for DHN change 563 if change heat_LT Industry 
            config['all_data']['Misc']['min_biomass_use_ind_heat_lt'] = Value_bm_use * 1000 *0.315 #Energy for IND change 563 if change heat_HT Industry """

            # For the analysis of the impact of the production share of jetfuel from FT 
            """config['all_data']['Layers_in_out'].loc['REFINERY_JETFUEL', 'JETFUEL'] = share_jetfuel_refinery[case_number]/100
            config['all_data']['Layers_in_out'].loc['REFINERY_JETFUEL', 'GASOLINE'] = share_gasoline_refinery[case_number]/100
            config['all_data']['Layers_in_out'].loc['REFINERY_JETFUEL', 'DIESEL'] = share_diesel_refinery[case_number]/100"""


            if not analysis_only:
                if compute_TDs:
                    es.build_td_of_days(config)

                # Printing the .dat files for the optimisation problem       
                es.print_data(config)
                filename = os.path.join(config['case_studies'], config['case_study'], "not_working.txt")
                if os.path.exists(filename):
                    # If the file exists, delete it
                    os.remove(filename)
                # Running EnergyScope
                run_ended = es.run_es_sensi(config)
                config['print_sankey'] = False
                if run_ended == False:           
                    file = open(filename, "w")
                    file.close()