import os
from pathlib import Path
import energyscope as es
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings
import numpy as np 
warnings.filterwarnings("ignore")

analysis_sensibility_only = True

if analysis_sensibility_only == False:
    
    # define project path
    project_path = Path(__file__).parents[0]
    sensibility_data = pd.read_excel(os.path.join(project_path, 'sensibility_data_2.xlsx'))
    number_of_cases = sensibility_data['Case_number'].iloc[-1]
    OUTPUTS = pd.DataFrame(columns=['DAC_LT', 'JETFUEL_prod', 'f_max_nuc', 'c_inv_nuc', 'f_max_wood', 'total_cost', 'COST_JETFUEL', 'COST_ELEC', 'COST_H2'], index=np.arange(0,number_of_cases))
    
    for case_number in range(0, 6):#  number_of_cases):
        analysis_only= False
        compute_TDs = True

        print(project_path)
        # loading the config file into a python dictionnary
        config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
        #config['GWP_limit'] = str(GWP_limit) + ';'
        folder_name = sensibility_data['Folder_name'].iloc[case_number]
        case_number_2 = sensibility_data['Case_number_2'].iloc[case_number]
        print(folder_name)
        config['case_studies'] = os.path.join(project_path, 'case_studies', 'sensibility', folder_name)
        config['case_study'] = str(case_number_2)
        config['Working_directory'] = os.getcwd() # keeping current working directory into config
        config['print_hourly_data'] = False
        
    # Reading the data of the csv
        es.import_data(config)
        File_name = sensibility_data['File_name'].iloc[case_number]
        Techno_ress = sensibility_data['Techno_ress'].iloc[case_number]
        Parameter = sensibility_data['Parameter'].iloc[case_number]
        New_value = sensibility_data['New_value'].iloc[case_number]
        
        #print(config['all_data'][File_name].loc[Techno_ress, Parameter], Parameter)
        config['all_data'][File_name].loc[Techno_ress, Parameter] = New_value
        #config['all_data'][File_name].loc[Techno_ress, 'avail'] = 10000000
        #config['all_data'][File_name].loc['WOOD_GROWTH', Parameter] = New_value
        #config['all_data']['Resources'].loc['ELECTRICITY', 'avail'] = 0#(30 - New_value)*8760
        #config['all_data'][File_name].loc['DAC_HT', Parameter] = New_value
        #print(config['all_data'][File_name].loc[Techno_ress, Parameter], Parameter)
        #print(config['all_data'][File_name])


        if not analysis_only:
            if compute_TDs:
                es.build_td_of_days(config)

            # Printing the .dat files for the optimisation problem       
            es.print_data(config)

            # Running EnergyScope
            run_ended = es.run_es_sensi(config)
            config['print_sankey'] = True
            if run_ended == False:
                filename = os.path.join(config['case_studies'], config['case_study'], "not_working.txt")
                file = open(filename, "w")
                file.close()


        if os.path.exists(os.path.join(config['case_studies'], config['case_study'], "not_working.txt")) == False: 
            outputs = es.read_outputs(config, hourly_data=False, layers=[])
            # Example to print the sankey from this script
            print_Sankey = False
            if print_Sankey == True:
                #sankey_path = config['cs_path']/ config['case_study'] / 'output' / 'sankey'
                #es.drawSankey(path=sankey_path)
                fig = es.Sankey_plot(outputs['year_balance'], outputs['sto_year'])
                fig.show()


project_path = Path(__file__).parents[0]
config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
for j in range(1, 6):
    
    config['case_studies'] = os.path.join(project_path, 'case_studies', 'sensibility', 'energy_demand')
    config['case_study'] = str(j) 
    outputs = es.read_outputs(config, hourly_data=False)
    balance = outputs['year_balance']
    print(balance[balance['ELECTRICITY'].ge(0)]['ELECTRICITY'].sum())