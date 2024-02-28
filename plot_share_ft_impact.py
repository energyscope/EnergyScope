import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import energyscope as es
import plotly.subplots as sp

################## Figure Plot##################

def integral_cost_calculation (df, outputs, shape_x, shape_y, var, var_name):
    "Compute the cost of production of jet fuel based on the evolution of the quantity of jet fuel imported over the cost of import"
    for ite_y in range(0, shape_y):
        price_qtt_import = []
        qtt_import = []
        elec_prod = []
        h2_prod = []
        cc_share = []
        df['REDUC_EMI_JETFUEL'].append(int(-outputs[shape_x*ite_y]['year_balance'].loc['JETFUEL_RE', 'CO2_ATMOSPHERE']/outputs[shape_x*ite_y]['year_balance'].loc['JETFUEL_RE', 'JETFUEL']*100/0.26+0.1))
        df['BIOMASS_SEQU'].append(outputs[shape_x*ite_y]['year_balance'].loc['BIOMASS_SEQUESTRATION', 'WOOD']-outputs[shape_x*ite_y+shape_x-1]['year_balance'].loc['BIOMASS_SEQUESTRATION', 'WOOD'])
        for ite_x in range (shape_x*ite_y, shape_x*(ite_y+1)): 
            price_qtt_import.append(outputs[ite_x]['cost_breakdown'].loc['JETFUEL_RE', 'C_op'])
            qtt_import.append(outputs[ite_x]['year_balance'].loc['JETFUEL_RE', 'JETFUEL'])
            elec_prod.append(outputs[ite_x]['year_balance'].loc[outputs[ite_x]['year_balance'].loc[:,'ELECTRICITY' ].ge(100),'ELECTRICITY' ].sum())
            cc_share.append(100*(outputs[ite_x]['year_balance'].loc['INDUSTRY_CCS','CO2_CAPTURED'])/( outputs[ite_x]['year_balance'].loc[outputs[ite_x]['year_balance'].loc[:,'CO2_CENTRALISED' ].ge(10),'CO2_CENTRALISED' ].sum()))
            h2_prod.append(outputs[ite_x]['year_balance'].loc['ALKALINE_ELECTROLYSIS', 'H2']+outputs[ite_x]['year_balance'].loc['HT_ELECTROLYSIS', 'H2'])
        price_0 = 1000*price_qtt_import[0]/qtt_import[0]+1000*(price_qtt_import[1]/qtt_import[1]-price_qtt_import[0]/qtt_import[0])*sum(qtt_import)/(max(qtt_import))
        df['COST_PROD_JETFUEL'].append(price_0)
        df['ELEC_PROD'].append((elec_prod[-1]-elec_prod[0])/1000)
        df['CC_SHARE'].append(cc_share[-1]-cc_share[0])
        df['H2_PROD'].append((h2_prod[-1]-h2_prod[0])/1000)
        df[var_name].append(var)


#fig.line(all_ps)
df = {'COST_PROD_JETFUEL' : [], 'ELEC_PROD' : [], 'FT_SHARE' : [], 'REDUC_EMI_JETFUEL' : [], 'CC_SHARE' : [], 'H2_PROD' : [], 'BIOMASS_SEQU': []}


directory_path = os.path.join(os.getcwd(),'case_studies', 'paper1', 'import_analysis', 'jetfuel_import_price_ft'+str(40))
outputs = es.read_data_post_process(directory_path, False, True)
integral_cost_calculation (df, outputs, 56, 3, 40, 'FT_SHARE')
for i in range (50, 110, 10):
    directory_path = os.path.join(os.getcwd(),'case_studies', 'paper1', 'import_analysis', 'jetfuel_import_price_ft'+str(i))
    outputs = es.read_data_post_process(directory_path, False, True)
    integral_cost_calculation (df, outputs, 46, 3, i, 'FT_SHARE')


df = pd.DataFrame(df)
print(df)



############## SUBPLOT #################
subplot = sp.make_subplots(rows=3, cols=2, shared_xaxes=True, vertical_spacing=0.04, horizontal_spacing=0.06
                           , subplot_titles=['a', 'd', 'b', 'e', 'c', 'f'])



# Store colors for each unique 'FT_SHARE' value
color_mapping = {}
print(df['REDUC_EMI_JETFUEL'].unique())
colormap = ['blue', 'red', 'green', 'yellow', 'purple', 'pink', 'gray', 'black']
name_color = ['Emission = +10%', 'Emission = -90%', 'Emission = -290%']
# Iterate over unique values of 'FT_SHARE'
df = df[df['REDUC_EMI_JETFUEL'].isin([-9, 90, 290])]
for i, color_value in enumerate(df['REDUC_EMI_JETFUEL'].unique()):
    color_data = df[df['REDUC_EMI_JETFUEL'] == color_value]

    color = colormap[i]

    subplot.add_trace(go.Scatter(x=color_data['FT_SHARE'], y=color_data['COST_PROD_JETFUEL'],
            mode='markers+lines', marker=dict(color=color), line=dict(color=color), name=name_color[i]), row=1, col=1)

    subplot.add_trace(go.Scatter(x=color_data['FT_SHARE'], y=color_data['ELEC_PROD'],
            mode='markers+lines', marker=dict(color=color), line=dict(color=color), showlegend=False), row=2, col=1)

    subplot.add_trace(go.Scatter(x=color_data['FT_SHARE'] ,y=color_data['H2_PROD'],
            mode='markers+lines', marker=dict(color=color), line=dict(color=color),showlegend=False), row=3, col=1)
    

directory_path = os.path.join(os.getcwd(),'case_studies', 'paper1', 'ft_analysis')
df = es.file_compute_parameters(directory_path, False, False)
df = df.sort_values(by ='SHARE_JETFUEL_OUT_FT')
fig = px.scatter(df, x='SHARE_JETFUEL_OUT_FT', y='COST')
name_color = ['70-OP', '100-OP', 'RF-EU']
colormap = ['purple', 'orange', 'black']
for i, color_value in enumerate(df['FOLDER_NAME'].str[:13].unique()):
    color_data = df[df['FOLDER_NAME'].str[:13] == color_value]
    color = colormap[i]

    subplot.add_trace(go.Scatter(x=color_data['SHARE_JETFUEL_OUT_FT']*100, y=color_data['COST']/1000,
            mode='markers+lines', marker=dict(color=color), line=dict(color=color), name=name_color[i]), row=1, col=2)

    subplot.add_trace(go.Scatter(x=color_data['SHARE_JETFUEL_OUT_FT']*100, y=color_data['HYDROGEN_PROD_FT']/1000,
            mode='markers+lines', marker=dict(color=color), line=dict(color=color), showlegend=False), row=2, col=2)

    subplot.add_trace(go.Scatter(x=color_data['SHARE_JETFUEL_OUT_FT']*100, y=color_data['BIOMASS_PROD_FT']/1000,
            mode='markers+lines', marker=dict(color=color), line=dict(color=color),showlegend=False), row=3, col=2)


subplot.update_layout(font=dict(size=18, color='black'))
subplot.update_xaxes(title_text='Share of jet fuel at the output of FT process (%)', row=3, col=1, title_font=dict(size=20))
subplot.update_yaxes(title_text='Cost jet fuel (EUR/MWh)', col=1, row=1, title_font=dict(size=18), title_standoff=10)
subplot.update_yaxes(title_text='Electricity prod. (TWh)', col=1, row=2, title_font=dict(size=18), title_standoff=10)
subplot.update_yaxes(title_text='Hydrogen prod. (TWh)', col=1, row=3, title_font=dict(size=18), title_standoff=10)
subplot.update_xaxes(title_text='Share of jet fuel at the output of FT process (%)', row=3, col=2, title_font=dict(size=20))
subplot.update_yaxes(title_text='Cost of the system (GEUR)', col=2, row=1, title_font=dict(size=18), title_standoff=10)
subplot.update_yaxes(title_text='Hydrogen used (TWh)', col=2, row=2, title_font=dict(size=18), title_standoff=10)
subplot.update_yaxes(title_text='Biomass used (TWh)', col=2, row=3, title_font=dict(size=18), title_standoff=10)

subplot.show()