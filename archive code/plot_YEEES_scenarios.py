import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import energyscope as es

        
OUTPUTS = pd.DataFrame(columns=['DAC_LT', 'JETFUEL_prod', 'f_max_nuc', 'c_inv_nuc', 'f_max_wood', 'total_cost', 'COST_JETFUEL', 'COST_ELEC', 'COST_H2'], index=np.arange(0,10))
L = []
directory_path = os.path.join(os.getcwd(), 'case_studies', 'YEEES', 'scenarios')
#for folder_name in os.listdir(directory_path):
for j in range (1, 1):
    folder_name = 'scenario_'+str(j)
    folder_path = os.path.join(directory_path, folder_name)
       # define project path
    project_path = Path(__file__).parents[0]

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
    config['Working_directory'] = os.getcwd() # keeping current working directory into config
    config['case_studies'] = os.path.join(os.getcwd(),'case_studies', 'YEEES', 'scenarios')
    config['case_study'] = folder_name
    #config['ampl_options']['log_file'] = os.path.join(config['case_studies'], config['case_study'], config['ampl_options']['log_file'])
   # Reading the data of the csv
    #es.import_data(config)

    # Example to print the sankey from this script
    
    #print(config)
    print(folder_name, config['case_study'])
    # Reading outputs
    if os.path.exists(os.path.join(config['case_studies'], config['case_study'], 'output', 'year_balance.txt')) == True: 
        print(1, config['case_study'])
        outputs = es.read_outputs(config, hourly_data=False)#, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN','layer_HEAT_LOW_T_DHN', 'layer_HEAT_HIGH_T', 'layer_AMMONIA', 'layer_H2', 'layer_LFO' , 'layer_GAS'])
        L.append(outputs)
        """fig = es.Sankey_plot(outputs['year_balance'])
        fig.show()

        fig = es.Sankey_carbon(outputs['year_balance'], outputs['gwp_breakdown'])
        fig.show()"""
#print(L)
print_atmo = False
if print_atmo == True:
    dict_1, a = {}, 0
    for i in range (0, 5):
        for index, row in L[i]['year_balance'].iterrows():  
            a = a + 1
            if L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'] <= 100:
                L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'] = 0
            if index not in ['CO2_EMISSIONS', 'GHG_EMISSIONS']:
                if  abs(L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'] + L[i]['year_balance'].loc[index, 'OTHER_GHG'] + L[i]['year_balance'].loc[index, 'CO2_ATMOSPHERE']) >=100:
                    if index.startswith('BUS'):
                        dict_1[a] = (i+1, 'BUS', L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'], L[i]['year_balance'].loc[index, 'OTHER_GHG'], L[i]['year_balance'].loc[index, 'CO2_ATMOSPHERE'])
                    elif index.startswith('TRUCK'):
                        dict_1[a] = (i+1, 'TRUCK', L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'], L[i]['year_balance'].loc[index, 'OTHER_GHG'], L[i]['year_balance'].loc[index, 'CO2_ATMOSPHERE'])
                    else:
                        dict_1[a] = (i+1, index, L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'], L[i]['year_balance'].loc[index, 'OTHER_GHG'], L[i]['year_balance'].loc[index, 'CO2_ATMOSPHERE'])
            if index == 'CO2_ATMOSPHERE':
                dict_1[a] = (i+1, 'CENTRALISED_EMISSIONS', L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'], L[i]['year_balance'].loc[index, 'OTHER_GHG'], L[i]['year_balance'].loc[index, 'CO2_ATMOSPHERE'])
        dict_1[a] = (i+1, 'GHG_CONSTRUCTION', L[i]['gwp_breakdown']['GWP_constr'].sum(), 0, 0)
    df_2 = pd.DataFrame.from_dict(dict_1, orient='index', columns=['Scenario', 'Tech', 'Value_ghg', 'Value_dec', 'Value_atm'])

    techno_color = pd.read_excel(os.path.join(Path(__file__).parents[0], 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False).fillna('')
    name_color_mapping = dict(zip(techno_color['Name'], techno_color['Color_bar_plot_2']))
    #name_pattern_mapping = dict(zip(techno_color['Name'], techno_color['Pattern_shape']))
    fig = px.bar(df_2, x='Scenario', y=['Value_ghg', 'Value_dec', 'Value_atm'], color='Tech', color_discrete_map=name_color_mapping #, pattern_shape='Tech'
                  , labels={'Scenario': 'Scenario', 'Value_ghg': 'GHG emission/removal (ktCO2eq)'})
    #fig.add_trace(go.Bar(filtered_df_ghg.T)) #, pattern_shape_map=name_pattern_mapping
    fig.update_yaxes(title_text='GHG emission/removal (ktCO2eq)', row=1)  # Value_ghg

    fig.update_layout(shapes=[dict(type='line', y0=0, y1=0, x0=0.5, x1=5.5, line=dict(color='black'))])
    fig.update_xaxes(categoryorder='total descending')
    fig.show()

print_capt = False
if print_capt == True:
    CAPT = []
    for i in range (0, 5):
        data_capt = L[i]['year_balance']['CO2_CAPTURED'].rename(i)
        data_capt.at['CO2_EMISSIONS'] = 0
        data_capt.at['GHG_EMISSIONS'] = 0
        CAPT.append(data_capt)

    df_CAPT = pd.concat(CAPT, axis=1)
    #df_CAPT = df_CAPT.sub(df_CAPT[1], axis='index')
    filtered_df = df_CAPT[df_CAPT.iloc[:, 1:].abs().ge(100).any(axis=1)] 
    techno_color = pd.read_excel(os.path.join(Path(__file__).parents[0], 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False).fillna('')
    name_color_mapping = dict(zip(techno_color['Name'], techno_color['Color_bar_plot_2']))
    name_pattern_mapping = dict(zip(techno_color['Name'], techno_color['Pattern_shape']))
    a = 0
    dict_1 = {}
    for index, row in filtered_df.iterrows():
        for j in range(0, 5):
            a = a + 1
            dict_1[a] = (j+1, index, filtered_df[j].loc[index]/1000)
    df_2 = pd.DataFrame.from_dict(dict_1, orient='index', columns=['Scenario', 'Technologies', 'Value'])
    fig = px.bar(df_2, x='Scenario', y='Value', color='Technologies', color_discrete_map=name_color_mapping
                 , labels={'Scenario': 'Scenario', 'Value': 'Carbon captured/used (MtCO2)'})
    fig.update_layout(shapes=[dict(type='line', y0=0, y1=0, x0=0.5, x1=5.5, line=dict(color='black'))])
    fig.update_layout(legend=dict(title_font=dict(size=20), font=dict(size=20)))
    fig.update_layout(xaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)))
    fig.update_layout(yaxis=dict(title_font=dict(size=20), tickfont=dict(size=16)))
    fig.update_xaxes(categoryorder='total descending')
    fig.show()

print_cost = False
if print_cost == True:
    #f_atmo = pd.DataFrame(columns=[i for i in range(0,2)])
    ATMO = []
    for i in range (0, 5):
        #print(i)
        data_atmo = L[i]['cost_breakdown']['C_inv'].rename(i)
        for index, row in L[i]['cost_breakdown'].iterrows(): 
            cost_index = L[i]['cost_breakdown'].loc[index, 'C_inv'] + L[i]['cost_breakdown'].loc[index, 'C_maint'] + L[i]['cost_breakdown'].loc[index, 'C_op']
            if cost_index>0.1 :
                data_atmo.at[index] = cost_index #+ L[i]['year_balance'].loc(index)['CO2_ATMOSPHERE'] 
        ATMO.append(data_atmo)

    df_ATMO = pd.concat(ATMO, axis=1)
    df_ATMO = df_ATMO.sub(df_ATMO[0], axis='index')
    filtered_df = df_ATMO[df_ATMO.iloc[:, 1:].abs().ge(300).any(axis=1)] 
    techno_color = pd.read_excel(os.path.join(Path(__file__).parents[0], 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False).fillna('')
    name_color_mapping = dict(zip(techno_color['Name'], techno_color['Color_bar_plot_2']))
    name_pattern_mapping = dict(zip(techno_color['Name'], techno_color['Pattern_shape']))
    a = 0
    dict_1 = {}
    for index, row in filtered_df.iterrows():
        for j in range(0, 5):
            a = a + 1
            dict_1[a] = (j+1, index, filtered_df[j].loc[index])
    df_2 = pd.DataFrame.from_dict(dict_1, orient='index', columns=['Scenario', 'Technologies', 'Value'])
    fig = px.bar(df_2, x='Scenario', y='Value', color='Technologies', color_discrete_map=name_color_mapping, pattern_shape='Technologies'
                 , pattern_shape_map=name_pattern_mapping, labels={'Scenario': 'Scenario', 'Value': 'Cost variation (MEUR)'})
    print(df_2.groupby('Scenario')['Value'].sum().reset_index())
    a = df_2.groupby('Scenario')['Value'].sum().reset_index()
    fig.add_trace(go.Scatter(x=a['Scenario'], y=a['Value'],name='Total Cost increase (MEUR)',
    mode='markers+text',  # Use 'markers+text' mode to display both markers and text
    marker=dict(color='red', size=16),
    text=a['Value'].astype(int),
    textposition='bottom center',  # Position text below the point
    textfont=dict(color='white',size=18),  # Set the text color to red
))
    fig.update_layout(shapes=[dict(type='line', y0=0, y1=0, x0=0.5, x1=5.5, line=dict(color='black'))])
    fig.update_layout(legend=dict(title_font=dict(size=20), font=dict(size=18)))
    fig.update_layout(xaxis=dict(title_font=dict(size=18), tickfont=dict(size=16)))
    fig.update_layout(yaxis=dict(title_font=dict(size=18), tickfont=dict(size=16)))
    fig.update_xaxes(categoryorder='total descending')
    fig.show()
    


print_elec = False
if print_elec == True:
    CAPT = []
    for i in range (0, 5):
        data_capt = L[i]['year_balance']['ELECTRICITY'].rename(i)
        data_capt.at['CO2_EMISSIONS'] = 0
        data_capt.at['GHG_EMISSIONS'] = 0
        CAPT.append(data_capt)

    df_CAPT = pd.concat(CAPT, axis=1)
    #df_CAPT = df_CAPT.sub(df_CAPT[1], axis='index')
    filtered_df = df_CAPT[df_CAPT.iloc[:, 1:].abs().ge(100).any(axis=1)] 
    techno_color = pd.read_excel(os.path.join(Path(__file__).parents[0], 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False).fillna('')
    name_color_mapping = dict(zip(techno_color['Name'], techno_color['Color_bar_plot_2']))
    name_pattern_mapping = dict(zip(techno_color['Name'], techno_color['Pattern_shape']))
    a = 0
    dict_1 = {}
    for index, row in filtered_df.iterrows():
        for j in range(0, 5):
            a = a + 1
            dict_1[a] = (j+1, index, filtered_df[j].loc[index]-filtered_df[0].loc[index])
    df_2 = pd.DataFrame.from_dict(dict_1, orient='index', columns=['Scenario', 'Tech', 'Value'])
    fig = px.bar(df_2, x='Scenario', y='Value', color='Tech', color_discrete_map=name_color_mapping, pattern_shape='Tech'
                 , pattern_shape_map=name_pattern_mapping
                 , labels={'Scenario': 'Scenario', 'Value': 'Electricity consumed/produced (GWh)'})
    fig.update_layout(shapes=[dict(type='line', y0=0, y1=0, x0=0.5, x1=5.5, line=dict(color='black'))])
    fig.update_xaxes(categoryorder='total descending')
    fig.show()



print_table_sce = True
if print_table_sce == True:
    total_cost_sce_1 = L[0]['cost_breakdown']['C_inv'].sum() + L[0]['cost_breakdown']['C_maint'].sum() + L[0]['cost_breakdown']['C_op'].sum()
    for i in range (0, len(L)):
        
        balance = L[i]['year_balance']
        print('scenario ' +str(i))
        #print(L[i]['year_balance']['ELECTRICITY'].ge(0))
        print('Elec production '+str(balance[balance['ELECTRICITY'].ge(0)]['ELECTRICITY'].sum())+' GWh')
        total_qtt_e_bio = balance.loc['E_WOOD_TO_FT', 'FT_FUEL'] + balance.loc['E_WOOD_TO_METHANOL', 'METHANOL'] + balance.loc['E_WOOD_TO_METHANE', 'GAS']
        total_qtt_bio = balance.loc['WOOD_TO_FT', 'FT_FUEL'] + balance.loc['WOOD_TO_METHANOL', 'METHANOL'] + balance.loc['WOOD_TO_METHANE', 'GAS']
        total_qtt_e = balance.loc['CO2_TO_FT', 'FT_FUEL'] + balance.loc['CO2_TO_METHANOL', 'METHANOL'] + balance.loc['CO2_TO_METHANE', 'GAS']
        total_qtt_fuel = total_qtt_e + total_qtt_bio + total_qtt_e_bio
        print('Fuel % BIO/E-BIO/E ',total_qtt_bio/total_qtt_fuel, total_qtt_e_bio/total_qtt_fuel, total_qtt_e/total_qtt_fuel)
        print('Biomass sequestration', balance.loc['BIOMASS_SEQUESTRATION', 'WOOD'], balance.loc['BIOMASS_SEQUESTRATION', 'WOOD']*0.39)

        total_cost_sce_i = L[i]['cost_breakdown']['C_inv'].sum() + L[i]['cost_breakdown']['C_maint'].sum() + L[i]['cost_breakdown']['C_op'].sum()
        print('variation total cost %', -100*(1-total_cost_sce_i/total_cost_sce_1))

def prod_elec(L, i):
    i = i-1
    return(L[i]['year_balance'][L[i]['year_balance']['ELECTRICITY'].ge(0)]['ELECTRICITY'].sum())

print('diff scenario availability sequestration', ((prod_elec(L, 1)+prod_elec(L, 4)+prod_elec(L, 6)+prod_elec(L, 8))-(prod_elec(L, 2)+prod_elec(L, 5)+prod_elec(L, 7)+prod_elec(L, 9)))/4)
print('diff scenario qtt biomass', ((prod_elec(L, 1)+prod_elec(L, 2)+prod_elec(L, 4)+prod_elec(L, 5))-(prod_elec(L, 6)+prod_elec(L, 8)+prod_elec(L, 7)+prod_elec(L, 9)))/4)
print('diff scenario use biomass', ((prod_elec(L, 1)+prod_elec(L, 2)+prod_elec(L, 6)+prod_elec(L, 7))-(prod_elec(L, 4)+prod_elec(L, 8)+prod_elec(L, 5)+prod_elec(L, 9)))/4)






"""#print(L)
print_atmo = True
if print_atmo == True:
    #f_atmo = pd.DataFrame(columns=[i for i in range(0,2)])
    ATMO_dec = []
    ATMO_ghg = []
    for i in range (0, len(L)):
        #print(i)
        data_atmo_dec = L[i]['year_balance']['CO2_ATMOSPHERE'].rename(i)
        data_atmo_ghg = L[i]['year_balance']['CO2_ATMOSPHERE'].rename(i)
        #print(L[i]['year_balance'])
        for index, row in L[i]['year_balance'].iterrows(): 
            if L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'] + L[i]['year_balance'].loc[index, 'OTHER_GHG']>0.1 :
                data_atmo_dec.at[index] = L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED']  #+ L[i]['year_balance'].loc(index)['CO2_ATMOSPHERE'] 
                data_atmo_ghg.at[index] = L[i]['year_balance'].loc[index, 'OTHER_GHG'] + L[i]['year_balance'].loc[index, 'CO2_DECENTRALISED'] 
        #M.append(L[i]['year_balance']['CO2_ATMOSPHERE'])
        data_atmo_dec.loc['CO2_EMISSIONS'] = 0
        data_atmo_ghg.loc['CO2_EMISSIONS'] = 0
        data_atmo_ghg.loc['GHG_EMISSIONS'] = 0
        ATMO_dec.append(data_atmo_dec)
        #print(data_atmo_ghg.loc['CO2_EMISSIONS'])
        ATMO_ghg.append(data_atmo_ghg)
    df_ATMO_ghg = pd.concat(ATMO_ghg, axis=1)
    #print(df_ATMO_ghg)
    #df_ATMO_ghg = df_ATMO_ghg.sub(df_ATMO_ghg[1], axis='index')
    filtered_df_ghg = df_ATMO_ghg[df_ATMO_ghg.iloc[:, 1:].abs().ge(1).any(axis=1)]
    filtered_df_ghg_T = filtered_df_ghg.T
    dict_1, a = {}, 0
    for index, row in filtered_df_ghg.iterrows():
        for j in range(0, 9):
            a = a + 1
            dict_1[a] = (j+1, index, filtered_df_ghg[j].loc[index])
    df_2 = pd.DataFrame.from_dict(dict_1, orient='index', columns=['Scenario', 'Tech', 'Value'])
    techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False).fillna('')
    name_color_mapping = dict(zip(techno_color['Name'], techno_color['Color_bar_plot_2']))
    name_pattern_mapping = dict(zip(techno_color['Name'], techno_color['Pattern_shape']))
    fig = px.bar(df_2, x='Scenario', y='Value', color='Tech', color_discrete_map=name_color_mapping , pattern_shape='Tech'
                 , pattern_shape_map=name_pattern_mapping , labels={'Scenario': 'Scenario', 'Value': 'GHG emission/removal (ktCO2eq)'})
    #fig.add_trace(go.Bar(filtered_df_ghg.T))

    fig.update_layout(shapes=[dict(type='line', y0=0, y1=0, x0=0.5, x1=9.5, line=dict(color='black'))])
    fig.update_xaxes(categoryorder='total descending')
    fig.show()"""