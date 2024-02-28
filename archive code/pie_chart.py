import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import energyscope as es
import plotly.graph_objects as go
from plotly.subplots import make_subplots

project_path = Path(__file__).parents[0]
config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
config['case_studies'] = os.path.join(os.getcwd(),'case_studies')
config['Working_directory'] = os.getcwd() # keeping current working directory into config
config['print_hourly_data'] = False
outputs = es.read_outputs(config, hourly_data=False)

#fig = es.Sankey_plot(outputs['year_balance'], outputs['sto_year'])
#fig.show()

print_comparison_snbc = True
if print_comparison_snbc == True:
    
    list_primary_energy_elec = ['WIND_ONSHORE', 'NUCLEAR', 'PV', 'WIND_OFFSHORE', 'HYDRO_RIVER']
    list_primary_energy_elec_name = ['Wind Onshore', 'Nuclear', 'PV', 'Wind Offshore', 'Hydroelectricity']
    dict_1, a = {}, 0
    for i in range(0, 5):
        index = list_primary_energy_elec[i]
        index_name = list_primary_energy_elec_name[i]
        a = a + 1
        dict_1[a] = (index_name, int(0.001*outputs['year_balance']['ELECTRICITY'].loc[index]))
    a = a + 1
    dict_1[a] = ('Biomass', int(0.001*outputs['year_balance']['WOOD'].loc['WOOD_GROWTH']))
    a = a + 1
    dict_1[a] = ('Wet Biomass', int(0.001*outputs['year_balance']['WET_BIOMASS'].loc['WET_BIOMASS_GROWTH']))
    a = a + 1
    dict_1[a] = ('Waste', int(0.001*outputs['year_balance']['WASTE'].loc['WASTE']))
    a = a + 1
    dict_1[a] = ('Non Energy', 42.3)
    df_2 = pd.DataFrame.from_dict(dict_1, orient='index', columns=['Tech', 'Value'])
    fig = px.pie(df_2, values='Value', names='Tech', title='Primary energy')
    fig.update_traces(textposition='inside', textinfo='percent+label+value')


    labels = ['Coal', 'Refined Oil', 'Natural Gas', 'Electricity', 'Biomass', 'Waste', 'Non Energy', 'International transport', 'Wind Onshore', 'Nuclear', 'PV', 'Hydroelectricity', 'Wind Offshore', 'Wet Biomass']
    colors = ['black', 'darkslategrey', 'grey', 'yellow', 'forestgreen', 'brown', 'pink', 'orange', 'lightskyblue', 'olive', 'yellowgreen', 'aqua', 'steelblue', 'lawngreen'] #'lawngreen'
    fig = make_subplots(1, 3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['2019 Total = 1847 TWh', '2050 SNBC Total = 1325 TWh', '2050 Energyscope Total = '+str(df_2['Value'].sum())+' TWh'])
    fig.add_trace(go.Pie(labels=labels, values=[14, 890, 342, 0, 100, 70, 0, 0, 482*0.063, 482*0.706, 482*0.022, 482*0.112, 0.01, 0.01], marker_colors=colors, scalegroup='one',
                        name="World GDP 1980", sort=False, hole=0.4), 1, 1) #, pull=[0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 0]
    fig.add_trace(go.Pie(labels=labels, values=[0, 0, 0, 1060*0.55, 400, 85, 156, 117, 0, 0, 0, 0, 0], scalegroup='one',
                        name="World GDP 2007", sort=False, hole=0.4), 1, 2)
    fig.add_trace(go.Pie(labels=df_2['Tech'], values=df_2['Value'], scalegroup='one',
                        name="World GDP 2007", sort=False, hole=0.4), 1, 3)
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update_layout(title_text='Primary energy for France')
    fig.show()

plot_cost_system = False
if plot_cost_system == True :
    cost_out = outputs['cost_breakdown']
    dict_cost, a = {}, 0
    for index, row in cost_out.iterrows():
        cost = int(cost_out.loc[index, 'C_inv'] + cost_out.loc[index, 'C_maint'] + cost_out.loc[index, 'C_op'])
        dict_cost[a] = (index, cost)
        a = a+1
    df = pd.DataFrame.from_dict(dict_cost, orient='index', columns=[ 'Tech', 'Value'])
    df = df[df['Value'].ge(100)]
    fig = px.pie(df, values='Value', names='Tech')
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update_layout(title_text='Total yearly cost of French energy system; Total = '+str(df['Value'].sum())+' MEUR/year')
    fig.show()

plot_ghg_constr = False
if plot_ghg_constr == True :
    df = outputs['gwp_breakdown']
    print(df)
    df = df[df['GWP_constr'].ge(100)]
    df = df.reset_index()
    fig = px.pie(df, values='GWP_constr', names='Name')
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update_layout(title_text='Total yearly emission of GHG from construction; Total = '+str(df['GWP_constr'].sum())+' ktCO2eq/year')
    fig.show()