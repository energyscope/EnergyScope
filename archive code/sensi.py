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

analysis_sensibility_only = False

if analysis_sensibility_only == False:
    
    # define project path
    project_path = Path(__file__).parents[0]
    sensibility_data = pd.read_excel(os.path.join(project_path, 'sensibility_data.xlsx'))
    number_of_cases = sensibility_data['Case_number'].iloc[-1]
    OUTPUTS = pd.DataFrame(columns=['DAC_LT', 'JETFUEL_prod', 'f_max_nuc', 'c_inv_nuc', 'f_max_wood', 'total_cost', 'COST_JETFUEL', 'COST_ELEC', 'COST_H2'], index=np.arange(0,number_of_cases))
    
    for case_number in range(161, 191):#  number_of_cases):
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
        config['all_data'][File_name].loc[Techno_ress, 'avail'] = 10000000
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

                #fig = es.Sankey_carbon(outputs['year_balance'], outputs['gwp_breakdown'])
                #fig.show()

            # Reading outputs
            #outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN'])
            #fig = es.Sankey_plot(outputs['year_balance'])
            #fig.show()
            
            #outputs['GWP_limit'] = GWP_limit

            analysis = True
            if analysis == True :
                """COST = es.cost_calculator(outputs['year_balance'], outputs['assets'], outputs['resources_breakdown'], outputs['cost_breakdown'])
                cost_h2 = es.cost_calculator_vector(outputs['year_balance'], COST, 'H2')
                cost_elec = es.cost_calculator_vector(outputs['year_balance'], COST, 'ELECTRICITY')
                cost_jetfuel = es.cost_calculator_vector(outputs['year_balance'], COST, 'JETFUEL')"""
                print(outputs['year_balance'].loc['DAC_LT']['CO2_ATMOSPHERE'])
                #new_data = pd.DataFrame({'DAC_LT': outputs['year_balance'].loc['DAC_LT']['CO2_ATMOSPHERE']}, index=[case_number])
                OUTPUTS['DAC_LT'].loc[case_number] = outputs['year_balance'].loc['DAC_LT']['CO2_ATMOSPHERE']        
                OUTPUTS['JETFUEL_prod'].loc[case_number] = outputs['year_balance'].loc['REFINERY_JETFUEL']['JETFUEL']
                OUTPUTS['c_inv_nuc'].loc[case_number] = config['all_data']['Technologies'].loc['NUCLEAR', 'c_inv']
                OUTPUTS['f_max_nuc'].loc[case_number] = outputs['assets'].loc['NUCLEAR']['f'] #config['all_data']['Technologies'].loc['NUCLEAR', 'f_max']
                OUTPUTS['f_max_wood'].loc[case_number] = config['all_data']['Technologies'].loc['WOOD_GROWTH', 'f_max']
                OUTPUTS['total_cost'].loc[case_number] = outputs['cost_breakdown'].sum(axis=1).transpose().sum()
                """OUTPUTS['COST_JETFUEL'].loc[case_number] = cost_jetfuel
                OUTPUTS['COST_H2'].loc[case_number] = cost_h2
                OUTPUTS['COST_ELEC'].loc[case_number] = cost_elec"""

"""#OUTPUTS['DAC_LT'] = OUTPUTS['DAC_LT'].append(pd.Series(outputs['year_balance'].loc['DAC_LT']['CO2_ATMOSPHERE'], name=case_number))
print(OUTPUTS)

fig = px.parallel_coordinates(OUTPUTS,  dimensions = ['DAC_LT', 'JETFUEL_prod', 'f_max_nuc', 'f_max_wood', 'total_cost'],color_continuous_scale=px.colors.diverging.Tealrose,color_continuous_midpoint=2)#, color="total_cost",
                              #labels={'DAC': 'DAC_LT', 'JETFUEL' : 'JETFUEL_prod', 'capa_nuc' : 'f_max_nuc','capa_wood' : 'f_max_wood', 'cost' : 'total_cost'})#,
                              #color_continuous_scale=px.colors.diverging.Tealrose,
                              #color_continuous_midpoint=2)
print(fig)
#fig.show()
fig = px.parallel_coordinates(OUTPUTS)#, labels={'DAC': 'DAC_LT', 'JETFUEL' : 'JETFUEL_prod', 'capa_nuc' : 'f_max_nuc','capa_wood' : 'f_max_wood', 'cost' : 'total_cost'})#,
                              #color_continuous_scale=px.colors.diverging.Tealrose,
                              #color_continuous_midpoint=2)
print(fig)
#fig.show()
import plotly.graph_objects as go
df = OUTPUTS
fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = df['total_cost'],
                   colorscale = [[0,'purple'],[0.5,'lightseagreen'],[1,'gold']]),
        dimensions = list([
            dict(label = 'Capacity nuclear', values = df['f_max_nuc']),
            dict(label = 'Investment cost nuclear', values = df['c_inv_nuc']),
            #dict(label='f_max_wood', values = df['f_max_wood']),
            dict(label = 'Total Cost', values = df['total_cost'], range= [200000, 800000]),
            #dict(label = 'DAC', values = df['DAC_LT']),
            dict(label = 'COST_ELEC', values = df['COST_ELEC']),
            dict(label = 'COST_H2', values = df['COST_H2']),
            dict(label = 'COST_JETFUEL', values = df['COST_JETFUEL']),
            #dict(label = 'Jetfuel production', values = df['JETFUEL_prod'])     
            ])))
fig.show()
analysis = False
if analysis == True :"""

for j in range(1, 6):
    os.path.join(project_path, 'case_studies', 'sensibility', 'energy_demand')

