import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import energyscope as es
import plotly.subplots as sp
     
def read_data(directory_path, hourly_read):
    L = []   
    #for folder_name in os.listdir(directory_path):
    for j in range (1, 547):
        folder_name = 'scenario_'+str(j)
        folder_path = os.path.join(directory_path, folder_name)
        # define project path
        project_path = Path(__file__).parents[0]

        # loading the config file into a python dictionnary
        config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
        config['Working_directory'] = os.getcwd() # keeping current working directory into config
        config['case_studies'] = directory_path
        config['case_study'] = folder_name

        print(folder_name, config['case_study'])
        # Reading outputs
        if os.path.exists(os.path.join(config['case_studies'], config['case_study'], 'not_working.txt')) == True: 
            print(1, config['case_study'])
            L.append(False)
        else:
            outputs = es.read_outputs(config, hourly_data=hourly_read)#, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN','layer_HEAT_LOW_T_DHN', 'layer_HEAT_HIGH_T', 'layer_AMMONIA', 'layer_H2', 'layer_LFO' , 'layer_GAS'])
            L.append(outputs)
    return(L)
pop = 67200000
##################################### FUNCTION ######################################

    
########################################## RESULTS ######################################
directory_path = os.path.join(os.getcwd(),'case_studies', 'ECOS', 'test', 'share_nuc_stor_h2')
x_axis_data = [i for i in range (0, 70, 10)]*5
y_axis_data = []
[y_axis_data.extend([j]*7 ) for j in range (30, 80, 10)]
title_x_axis = 'Nuc (GW)'
title_y_axis = 'PV share (%)'
#data = es.file_compute_parameters(directory_path, True, True)

directory_path = os.path.join(os.getcwd(),'case_studies', 'paper1', 'import_analysis', 'jf_import_price_emi_reduc')
x_axis_data = [i for i in range (50, 505, 5)]*7
y_axis_data = []
[y_axis_data.extend([j-10] * 91) for j in range(0, 350, 50)]
title_x_axis = 'Price of import (EUR/MWh)'
title_y_axis = 'Reduction of emissions (%)'
data = es.file_compute_parameters(directory_path, False, True)


data = data.sort_values(by='CASE_NUMBER', ascending=True)

subplot = sp.make_subplots(rows=3, cols=3, shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.06
                           , subplot_titles=['(a) Total cost (EUR/cap/year)', '(b) Electricity generation (kWh/cap/year)', '(c) DAC (MtCO2)'
                                                           , '(d) Electolyzer load factor (%)', '(e) PV prod (TWh)', '(f) Wind prod (TWh)'
                                                           , '(g) NG Storage max (TWh)', '(h) H2 storage max (TWh)', '(i) Ammonia Storage max (TWh)']) 
bar_length_33 = 0.33
# First subplot
subplot.add_trace(go.Heatmap(z=data['COST'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.286, colorbar_y=0.855
                             , colorbar_len=bar_length_33, hoverongaps = False), row=1, col=1)

subplot.add_trace(go.Heatmap(z=data['ELEC'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.643, colorbar_y=0.855
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=1, col=2)

subplot.add_trace(go.Heatmap(z=data['PROD_ELEC_CCGT'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.855
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=1, col=3)

# Second row share e/bio/fuel
subplot.add_trace(go.Heatmap(z=data['ELY_LOAD_FACTOR'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.287, colorbar_y=0.5
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=2, col=1)


subplot.add_trace(go.Heatmap(z=data['PV_PROD'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.643, colorbar_y=0.5
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=2, col=2)


subplot.add_trace(go.Heatmap(z=data['WIND_PROD'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.5
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=2, col=3)

# Sequestration
subplot.add_trace(go.Heatmap(z=data['NG_STORAGE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.288, colorbar_y=0.145
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=3, col=1)

subplot.add_trace(go.Heatmap(z=data['H2_STORAGE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.643, colorbar_y=0.145
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=3, col=2)

subplot.add_trace(go.Heatmap(z=data['E_METHANE_PROD'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.145
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=3, col=3)


subplot.update_xaxes(title_text=title_x_axis, row=3, col=2, title_font=dict(size=20))
subplot.update_yaxes(title_text=title_y_axis, col=1, row=2, title_font=dict(size=20))
subplot.update_layout(font=dict(size=18))
subplot.update_annotations(font_size=18)
#subplot.update_layout(width=3380, height=1556)
subplot.show()

subplot = sp.make_subplots(rows=3, cols=3, shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.06
                    , subplot_titles=['(a) Total cost (GEUR)', '(b) Electricity generation (TWh)', '(c) Quantity of jet fuel imported (TWh)'#'(c) Biomass used for heat (kWh/cap/year)'
                                                           , '(d) H2 production (TWh)', '(e) Biomass use for heat (TWh)', '(f) Fuel cell truck share (%)'
                                                           , '(g) Share methanol to HVCs (%)', '(h) Biomass sequestration (MtCO2)', '(i) Carbon captured share (%)'])
bar_length_33 = 0.33
# First subplot
subplot.add_trace(go.Heatmap(z=data['COST'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.286, colorbar_y=0.855
                             , colorbar_len=bar_length_33, hoverongaps = False), row=1, col=1)

subplot.add_trace(go.Heatmap(z=data['ELEC'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.643, colorbar_y=0.855
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=1, col=2)

subplot.add_trace(go.Heatmap(z=data['QTT_JETFUEL_RE_IMP'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.855
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=1, col=3)

# Second row share e/bio/fuel
subplot.add_trace(go.Heatmap(z=data['H2_PROD'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.287, colorbar_y=0.5
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=2, col=1)


subplot.add_trace(go.Heatmap(z=data['BIOMASS_USE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.643, colorbar_y=0.5
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=2, col=2)


subplot.add_trace(go.Heatmap(z=data['TRUCK_H2'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.5
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=2, col=3)

# Sequestration
subplot.add_trace(go.Heatmap(z=data['SHARE_METHANOL_TO_HVC'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.288, colorbar_y=0.145
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=3, col=1)

subplot.add_trace(go.Heatmap(z=data['BIOMASS_SEQU'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.643, colorbar_y=0.145
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=3, col=2)

subplot.add_trace(go.Heatmap(z=data['CC_SHARE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.145
                             , colorbar_len=bar_length_33,  hoverongaps = False), row=3, col=3)


subplot.update_xaxes(title_text=title_x_axis, row=3, col=2, title_font=dict(size=20))
subplot.update_yaxes(title_text=title_y_axis, col=1, row=2, title_font=dict(size=20))
subplot.update_layout(font=dict(size=18))
subplot.update_annotations(font_size=18)
#subplot.update_layout(width=3380, height=1556)
subplot.show()


# Create a subplot with shared x-axis
#subplot = sp.make_subplots(rows=2, cols=2 subplot_titles=["ELEC", "COST", "SEQU", "BIOMASS_SEQU"])
plot_22 =False
if plot_22 == True:
    subplot = sp.make_subplots(rows=2, cols=2) 
    # First subplot
    subplot.add_trace(go.Heatmap(z=data['CC_SHARE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.45, colorbar_y=0.8, colorbar_len=0.5, colorbar_title='Elec', hoverongaps = False), row=1, col=1)

    # Second subplot
    subplot.add_trace(go.Heatmap(z=data['CC_SHARE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.8, colorbar_len=0.5, colorbar_title='Cost', hoverongaps = False), row=1, col=2)

    # Third subplot
    subplot.add_trace(go.Heatmap(z=data['CC_SHARE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=0.45, colorbar_y=0.22, colorbar_len=0.5, colorbar_title='E-Fuel', hoverongaps = False), row=2, col=1)

    # Fourth subplot
    subplot.add_trace(go.Heatmap(z=data['CC_SHARE'], x=x_axis_data, y=y_axis_data, colorscale='Viridis', colorbar_x=1, colorbar_y=0.22, colorbar_len=0.5, colorbar_title='E-Bio-Fuel', hoverongaps = False), row=2, col=2)

    # Show the subplot
    subplot.update_xaxes(title_text='Biomass availability (TWh/year)', row=2)
    subplot.update_yaxes(title_text='Geological CO2 sequestration availability (MtCO2/year)', col=1)
    subplot.show()