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

import random

def generate_configurations(num_params, num_values):
    configurations = []
    total_configurations = num_values ** num_params
    
    for i in range(total_configurations):
        config = []
        for j in range(num_params):
            config.append(random.randint(0, num_values-1))
        configurations.append(config)
    
    return configurations

def main():
    num_params = 10
    num_values = 3
    
    
    #print("Total configurations:", len(configurations))
    #print(configurations)
    #for idx, config in enumerate(configurations, start=1):
        #print(f"Configuration {idx}: {config}")

def analysis_cost (assets, cost_breakdown):
    new_cost_breakdown = cost_breakdown.copy()
    
    
    techno_H2 = ['ALKALINE_ELECTROLYSIS', 'HT_ELECTROLYSIS']
    techno_DAC = ['DAC_LT', 'DAC_HT']
    techno_CC = ['INDUSTRY_CCS']
    techno_BtX = ['WOOD_TO_METHANOL', 'WOOD_TO_METHANE', 'WOOD_TO_FT']
    techno_PBtX = ['E_WOOD_TO_METHANOL', 'E_WOOD_TO_METHANE', 'E_WOOD_TO_FT']
    techno_PtX = ['CO2_TO_METHANOL', 'CO2_TO_METHANE', 'CO2_TO_FT']
    techno_NUCLEAR = ['NUCLEAR']
    techno_RENEWABLE = ['PV', 'WIND_ONSHORE', 'WIND_OFFSHORE']
    all_technos = [techno_H2, techno_DAC, techno_NUCLEAR, techno_PtX, techno_BtX, techno_PBtX, techno_RENEWABLE]
    num_params = len(all_technos)
    num_values = 3
    configurations = generate_configurations(num_params, 3)
    total_configurations = num_values ** num_params
    config_cost = []
    config_cost_detail = []
    for i in range(total_configurations):
        for j, list_tech in enumerate(all_technos):
            for name_tech in list_tech :
                if configurations[i][j] == 0:
                    new_cost_breakdown.loc[name_tech] = cost_breakdown.loc[name_tech] * 0.5
                if configurations[i][j] == 2:
                    new_cost_breakdown.loc[name_tech] = cost_breakdown.loc[name_tech] * 2
        config_cost.append(new_cost_breakdown['C_inv'].sum()+ new_cost_breakdown['C_maint'].sum()+ new_cost_breakdown['C_op'].sum())
        config_cost_detail.append([new_cost_breakdown['C_inv'].sum(), new_cost_breakdown['C_maint'].sum(), new_cost_breakdown['C_op'].sum()])
    print(config_cost)
    print(new_cost_breakdown)
    return(config_cost)



####################################################################################

analysis_sensibility_only = False

if analysis_sensibility_only == False:
    
    # define project path
    project_path = Path(__file__).parents[0]
    sensibility_data = pd.read_excel(os.path.join(project_path, 'sensibility_data.xlsx'))
    number_of_cases = sensibility_data['Case_number'].iloc[-1]
    OUTPUTS = pd.DataFrame(columns=['DAC', 'DAC_cost', 'PtX', 'BtX', 'PBtX', 'sequ', 'total_cost', 'total_cost-dac','total_cost-dac-energy','capa_wood', 'COST_JETFUEL', 'COST_ELEC', 'COST_H2'], index=np.arange(0,number_of_cases))
    COST = pd.DataFrame(columns=['DAC', 'DAC_cost', 'cost'], index=np.arange(0,12*3**7))
    
    
    for case_number in range(0, 20):#  number_of_cases):
        analysis_only= True
        compute_TDs = False

        print(project_path)
        # loading the config file into a python dictionnary
        config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
        #config['GWP_limit'] = str(GWP_limit) + ';'
        config['case_studies'] = os.path.join(project_path, 'case_studies', 'sensibility', 'config_wood_vs_elec')
        config['case_study'] = str(case_number)
        config['Working_directory'] = os.getcwd() # keeping current working directory into config
        config['print_hourly_data'] = False
        
    # Reading the data of the csv
        es.import_data(config)
        File_name = sensibility_data['File_name'].iloc[case_number]
        Techno_ress = sensibility_data['Techno_ress'].iloc[case_number]
        Parameter = sensibility_data['Parameter'].iloc[case_number]
        New_value = sensibility_data['New_value'].iloc[case_number]
        #print(config['all_data'][File_name].loc[Techno_ress, Parameter], Parameter)
        #config['all_data'][File_name].loc['DAC_LT', Parameter] = New_value
        #config['all_data'][File_name].loc['DAC_HT', Parameter] = New_value
        #print(config['all_data'][File_name].loc[Techno_ress, Parameter], Parameter)
        print(config['all_data'][File_name])


        #♦if os.path.exists(os.path.join(config['case_studies'], config['case_study'], "not_working.txt")) == 1: 
        if os.path.exists(os.path.join(config['case_studies'], config['case_study'], "output","assets.txt")) == True:
            outputs = es.read_outputs(config, hourly_data=False, layers=[])
            if 1 == 2 :
                fig = es.Sankey_plot(outputs['year_balance'])
                fig.show()
                fig = es.Sankey_carbon(outputs['year_balance'], outputs['gwp_breakdown'])
                fig.show()
            OUTPUTS['DAC'].loc[case_number] = -outputs['year_balance'].loc['DAC_LT']['CO2_ATMOSPHERE'] - outputs['year_balance'].loc['DAC_HT']['CO2_ATMOSPHERE'] 
            OUTPUTS['DAC_cost'].loc[case_number] = config['all_data']['Technologies'].loc['DAC_LT', 'c_inv']
            OUTPUTS['sequ'].loc[case_number] =  - outputs['year_balance'].loc['SEQUESTRATION']['CO2_CAPTURED']
            OUTPUTS['PtX'].loc[case_number] =  outputs['assets'].loc['CO2_TO_FT']['f'] + outputs['assets'].loc['CO2_TO_METHANE']['f']  + outputs['assets'].loc['CO2_TO_METHANOL']['f']
            OUTPUTS['BtX'].loc[case_number] =  outputs['assets'].loc['WOOD_TO_FT']['f'] + outputs['assets'].loc['WOOD_TO_METHANE']['f']  + outputs['assets'].loc['WOOD_TO_METHANOL']['f']
            OUTPUTS['PBtX'].loc[case_number] =  outputs['assets'].loc['E_WOOD_TO_FT']['f'] + outputs['assets'].loc['E_WOOD_TO_METHANE']['f']  + outputs['assets'].loc['E_WOOD_TO_METHANOL']['f'] 
            OUTPUTS['capa_wood'].loc[case_number] =  outputs['assets'].loc['WOOD_GROWTH']['f']
            OUTPUTS['total_cost'].loc[case_number] = outputs['cost_breakdown'].sum(axis=1).transpose().sum()
            OUTPUTS['total_cost-dac'].loc[case_number] = outputs['cost_breakdown'].sum(axis=1).transpose().sum() - outputs['cost_breakdown'].loc['DAC_HT'].sum() - outputs['cost_breakdown'].loc['DAC_LT'].sum()
            OUTPUTS['total_cost-dac-energy'].loc[case_number] = OUTPUTS['total_cost-dac'].loc[case_number] + outputs['year_balance'].loc['DAC_LT']['ELECTRICITY']*0.05 +  outputs['year_balance'].loc['DAC_LT']['HEAT_LOW_T_DHN']*0.03 + outputs['year_balance'].loc['DAC_HT']['ELECTRICITY']*0.05# - 0.03*outputs['assets'].loc['WOOD_GROWTH']['f']*8760
            """cost = analysis_cost(outputs['assets'], outputs['cost_breakdown'])
            a = config['all_data']['Technologies'].loc['DAC_LT', 'c_inv']
            for i, j in enumerate(cost):
                COST['cost'].loc[i+case_number*len(cost)] = j 
                COST['DAC_cost'].loc[i+case_number*len(cost)] = a """

print(OUTPUTS)
fig = px.scatter(OUTPUTS, x='capa_wood', y='DAC')
fig.show()

fig = px.scatter(OUTPUTS, x='capa_wood', y=['total_cost', 'total_cost-dac', 'total_cost-dac-energy'])
fig.show()

fig = px.scatter(OUTPUTS, x='capa_wood', y=['PtX', 'BtX', 'PBtX'], log_x=True)
fig.show()