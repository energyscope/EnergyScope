import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

from energyscope import elec_order_graphs, plotting_names, rename_storage_power, colors_elec
import energyscope as es

#This file gather the important functions for the analyze of the results at the output of the model 

def plot_layer_balance_td (layer_balance: pd.DataFrame, title='Layer electricity', tds = np.arange(1,13), reorder_elec=None, figsize=(13,7), xticks=None):
    """Print the layer balance for the different typical days
    The type of layer is contained in layer balance
    """
    plotdata = layer_balance.copy()
    plotdata = plotdata.fillna(0)
    #Modify data to supress values lower than 0
    colonnes_zeros = plotdata.columns[plotdata.abs().eq(0).all()]
    
    plotdata = plotdata.drop(colonnes_zeros, axis=1)
    colonnes_zeros = plotdata.columns[plotdata.abs().sum() < 100]
    plotdata = plotdata.drop(colonnes_zeros, axis=1)

    names_column = plotdata.columns
    plotdata = plotdata.reset_index()
    plotdata[' Time'] = plotdata[' Time'] + 24 * (plotdata['Td ']-1)

    #Adjust the values for the storage technologies
    column_storage_out = plotdata.columns[plotdata.columns.str.endswith('_Pout')]
    column_storage_in = plotdata.columns[plotdata.columns.str.endswith('_Pin')]
    prefix = column_storage_out.str.split('_Pout').str[0].tolist()

    dfin = pd.DataFrame()
    dfin[prefix] = plotdata[column_storage_in]
    dfout = pd.DataFrame()
    dfout[prefix] = plotdata[column_storage_out]
    plotdata[prefix] = dfin + dfout

    names_column = names_column.difference(column_storage_in).difference(column_storage_out).insert(0, prefix)
    techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
    COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_bar_plot_1'].item() for i in names_column]
    fig = px.bar(plotdata, x=' Time' ,y=names_column, color_discrete_sequence=COLOR_node)
    colors = ["rgba(230, 25, 75, 0.2)", "rgba(60, 180, 75, 0.2)", "rgba(255, 225, 25, 0.2)",
          "rgba(0, 130, 200, 0.2)", "rgba(245, 130, 48, 0.2)", "rgba(145, 30, 180, 0.2)"]
    
    # Add color values behind for each layer
    x_ranges = [(i, i+24) for i in range(0, 265, 24)]
    for i, (x_start, x_end) in enumerate(x_ranges):
        color = colors[i % len(colors)]  # Select the corresponding color from the list in a loop.
        fig.add_shape(
        type="rect",
        xref="x",
        yref="paper",
        x0=x_start,
        y0=0,
        x1=x_end,
        y1=1,
        fillcolor=color,
        layer="below",
        line=dict(color="rgba(0, 0, 0, 0)"),
        )
    time_intervals = [i for i in range(24, 289, 24)]
    fig.add_shape(
                type="line",
                x0=0,x1=1,
                y0=0, y1=0,
                xref='paper', yref='y',
                line=dict(color="black", width=1)
            )
    for interval in time_intervals:
        fig.add_shape(
                type="line",
                x0=interval,x1=interval,
                y0=0, y1=1,
                xref='x', yref='paper',
                line=dict(color="black", width=1)
            )
    custom_ticks = [12 + 24*i for i in range(0, 12)]
    custom_tick_labels = ['TD {}'.format(i) for i in range(1, 13)]
    fig.update_layout(xaxis_title= "Time (hours)", yaxis_title="Energy production/consumption (GW)"
                      , xaxis=dict(tickmode='array',tickvals=custom_ticks,ticktext=custom_tick_labels), font=dict(size=20))
    fig.update_layout(font=dict(size=16))
    fig.update_xaxes(title_font=dict(size=20))
    fig.update_yaxes(title_font=dict(size=20))
    fig.update_layout(width=2000, height=1200)
    return(fig)

def plot_total_cost_system (outputs):
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
    return(fig)

def plot_share_ghg_construction (outputs):
    df = outputs['gwp_breakdown']
    df = df[df['GWP_constr'].ge(100)]
    df = df.reset_index()
    fig = px.pie(df, values='GWP_constr', names='Name')
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update_layout(title_text='Total yearly emission of GHG from construction; Total = '+str(int(df['GWP_constr'].sum()))+' ktCO2eq/year')
    return(fig)

def plot_energy_stored(energy_stored: pd.DataFrame, title='Layer electricity', tds = np.arange(1,13), reorder_elec=None, figsize=(13,7), xticks=None):
    """
    Print the evolution of the energy stored with different energy vectors over the entire year
    """
    plotdata = energy_stored.copy()

    plotdata = plotdata.fillna(0)
    colonnes_zeros = plotdata.columns[plotdata.eq(0).all()]
    plotdata = plotdata.drop(colonnes_zeros, axis=1)
    col_sum = plotdata.abs().sum()

    # Supress vectors with not enough energy stored
    threshold = 8760
    cols_to_drop = col_sum[col_sum < threshold].index
    plotdata = plotdata.drop(cols_to_drop, axis=1)

    names_column = plotdata.columns
    plotdata = plotdata.reset_index()
    plotdata = plotdata[::24]
    column_storage_out = plotdata.columns[plotdata.columns.str.endswith('_out')]
    column_storage_in = plotdata.columns[plotdata.columns.str.endswith('_in')]
    names_column = names_column.difference(column_storage_in).difference(column_storage_out)
    plotdata[names_column] = plotdata[names_column] - plotdata[names_column].min(axis=0)
    techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
    COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item() for i in names_column]
    fig = px.bar(plotdata, x='Time' ,y=names_column, color_discrete_sequence= COLOR_node)
    fig.update_layout(xaxis_title= "Time (hours)", yaxis_title="Energy stored (GWh)")
    fig.update_layout(font=dict(size=18))
    fig.update_xaxes(title_font=dict(size=20))
    fig.update_yaxes(title_font=dict(size=20))
    fig.update_layout(width=2000, height=1200)
    return(fig)

def compute_load_factors(outputs):
    alk_ely_load_factor = -outputs['year_balance'].loc['ALKALINE_ELECTROLYSIS', 'ELECTRICITY']/(outputs['assets'].loc['ALKALINE_ELECTROLYSIS', 'f']*8760)
    PV_load_factor = outputs['year_balance'].loc['PV', 'ELECTRICITY']/(outputs['assets'].loc['PV', 'f']*8760)
    WIND_ONSHORE_load_factor = outputs['year_balance'].loc['WIND_ONSHORE', 'ELECTRICITY']/(outputs['assets'].loc['WIND_ONSHORE', 'f']*8760)
    WIND_OFFSHORE_load_factor = outputs['year_balance'].loc['WIND_OFFSHORE', 'ELECTRICITY']/(outputs['assets'].loc['WIND_OFFSHORE', 'f']*8760)
    #EMISSIONS_ELEC_MIX = (outputs['gwp_breakdown'][outputs['gwp_breakdown']['GWP_constr']].ge(100).sum())/(outputs['year_balance'].loc[outputs['year_balance'].loc[:,'ELECTRICITY' ].ge(100),'ELECTRICITY' ].sum())
    print('Alkaline Electrolysis load factor (%) :', alk_ely_load_factor)
    print('PV panels load factor (%) :', PV_load_factor)
    print('Onshore wind load factor (%) :', WIND_ONSHORE_load_factor)
    print('Offshore wind load factor (%) :', WIND_OFFSHORE_load_factor)
    #print('Emissions of electricity on a LCA basis for electricity mix (gCO2/kWh) :', EMISSIONS_ELEC_MIX)
    return(alk_ely_load_factor, PV_load_factor, WIND_ONSHORE_load_factor, WIND_OFFSHORE_load_factor)



##################### Chantier ###########################

def read_data_post_process(directory_path, hourly_read, name_folder_scenario):
    L = []   
    
    for j, folder_name in enumerate(os.listdir(directory_path)):
        #folder_path = os.path.join(directory_path, folder_name)
        if name_folder_scenario == True:
            folder_name = 'scenario_'+str(j+1)
        folder_path = os.path.join(directory_path, folder_name)
        # define project path
        project_path = Path(__file__).parents[2]

        # loading the config file into a python dictionnary
        config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
        config['Working_directory'] = os.getcwd() # keeping current working directory into config
        config['case_studies'] = directory_path
        config['case_study'] = folder_name

        print(folder_name, config['case_study'])
        # Reading outputs
        if os.path.exists(os.path.join(config['case_studies'], config['case_study'], 'not_working.txt')) == True: 
            print(1, config['case_study'])
            outputs['folder_name'] = folder_name
            L.append(False)
        else:
            outputs = es.read_outputs(config, hourly_data=hourly_read)#, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN','layer_HEAT_LOW_T_DHN', 'layer_HEAT_HIGH_T', 'layer_AMMONIA', 'layer_H2', 'layer_LFO' , 'layer_GAS'])
            outputs['folder_name'] = folder_name
            L.append(outputs)
    return(L)

def file_compute_parameters(directory_path, hourly_read, name_folder_scenario):
    pop = 67200000
    def add_list_share_e_biofuel(outputs, i, data):
        "Add to the E_FUEL list the value of the share of fuel produced by PtX process "
        if outputs[i] == False:
            data['E_FUEL'].append(None)
            data['E_BIO_FUEL'].append(None)
            data['BIOFUEL'].append(None)
            data['TOTAL_FUEL_PRODUCED'].append(None)
        else:
            total_fuel_produced = outputs[i]['year_balance'].loc['CO2_TO_FT', 'FT_FUEL'] + outputs[i]['year_balance'].loc['CO2_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['CO2_TO_METHANE', 'GAS'] + outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'FT_FUEL'] + outputs[i]['year_balance'].loc['E_WOOD_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['E_WOOD_TO_METHANE', 'GAS'] + outputs[i]['year_balance'].loc['WOOD_TO_FT', 'FT_FUEL'] + outputs[i]['year_balance'].loc['WOOD_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['WOOD_TO_METHANE', 'GAS']
            share_e_fuel = 100*(outputs[i]['year_balance'].loc['CO2_TO_FT', 'FT_FUEL'] + outputs[i]['year_balance'].loc['CO2_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['CO2_TO_METHANE', 'GAS'])/total_fuel_produced
            share_e_bio_fuel = 100*(outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'FT_FUEL'] + outputs[i]['year_balance'].loc['E_WOOD_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['E_WOOD_TO_METHANE', 'GAS'])/total_fuel_produced
            share_bio_fuel = 100*(outputs[i]['year_balance'].loc['WOOD_TO_FT', 'FT_FUEL'] + outputs[i]['year_balance'].loc['WOOD_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['WOOD_TO_METHANE', 'GAS'])/total_fuel_produced
            data['E_FUEL'].append(share_e_fuel)
            data['E_BIO_FUEL'].append(share_e_bio_fuel)
            data['BIOFUEL'].append(share_bio_fuel)
            data['TOTAL_FUEL_PRODUCED'].append(total_fuel_produced)
        return(data)

    def add_list_cost (outputs, i, data):
        if outputs[i] == False:
            data['COST'].append(None)
        else: 
            cost = outputs[i]['cost_breakdown']['C_inv'].sum() + outputs[i]['cost_breakdown']['C_maint'].sum() +outputs[i]['cost_breakdown']['C_op'].sum()
            data['COST'].append(cost/1000)#*1000000/(pop))
        return(data)

    def add_list_sequ (outputs, i, data):
        if outputs[i] == False:
            data['SEQU'].append(None)
            data['BIOMASS_SEQU'].append(None)
        else: 
            sequ = -outputs[i]['year_balance'].loc['SEQUESTRATION','CO2_CAPTURED']
            biomass_sequ = -outputs[i]['year_balance'].loc['BIOMASS_SEQUESTRATION','WOOD']
            data['BIOMASS_SEQU'].append(biomass_sequ/1000)#*1000000/(pop))
            data['SEQU'].append(sequ/1000)#*1000000/(pop))
        return(data)

    def add_list_elec (outputs, i, data):
        if outputs[i] == False:
            data['ELEC'].append(None)
        else: 
            elec_generation = outputs[i]['year_balance'].loc[outputs[i]['year_balance'].loc[:,'ELECTRICITY' ].ge(100),'ELECTRICITY' ].sum()
            data['ELEC'].append(elec_generation/1000)#*1000000/(pop)
        return(data)

    def add_list_biomass_use (outputs, i, data):
        if outputs[i] == False:
            data['BIOMASS_USE'].append(None)
        else: 
            biomass_use = -(outputs[i]['year_balance'].loc['DEC_BOILER_WOOD','WOOD'] + outputs[i]['year_balance'].loc['DHN_BOILER_WOOD','WOOD'] + outputs[i]['year_balance'].loc['IND_BOILER_WOOD','WOOD'])
            data['BIOMASS_USE'].append(biomass_use/1000) #*1000000/(pop)
        return(data)

    def add_list_share_carbon_captured (outputs, i, data):
        if outputs[i] == False:
            data['CC_SHARE'].append(None)
        else: 
            cc_share = 100*(outputs[i]['year_balance'].loc['INDUSTRY_CCS','CO2_CAPTURED'])/( outputs[i]['year_balance'].loc[outputs[i]['year_balance'].loc[:,'CO2_CENTRALISED' ].ge(10),'CO2_CENTRALISED' ].sum())
            data['CC_SHARE'].append(cc_share)
        return(data)

    def add_list_qtt_jetfuel_imp (outputs, i, data):
        if outputs[i] == False:
            data['QTT_JETFUEL_IMP'].append(None)
            data['QTT_JETFUEL_RE_IMP'].append(None)
        else: 
            qtt_jetfuel_imp = outputs[i]['year_balance'].loc['JETFUEL_RE','JETFUEL']
            data['QTT_JETFUEL_RE_IMP'].append(qtt_jetfuel_imp/1000)
            data['QTT_JETFUEL_IMP'].append(int(outputs[i]['year_balance'].loc['JETFUEL','JETFUEL']/1000))
        return(data)


    

    def add_list_ely_load_factor (outputs, i, data):
        if outputs[i] == False:
            data['ELY_LOAD_FACTOR'].append(None)
            data['PV_PROD'].append(None)
            data['WIND_PROD'].append(None)
            data['H2_PROD'].append(None)
        else: 
            alk_ely_load_factor = -outputs[i]['year_balance'].loc['ALKALINE_ELECTROLYSIS', 'ELECTRICITY']/(outputs[i]['assets'].loc['ALKALINE_ELECTROLYSIS', 'f']*8760)
            pv_prod = outputs[i]['year_balance'].loc['PV', 'ELECTRICITY']
            wind_prod = outputs[i]['year_balance'].loc['WIND_ONSHORE', 'ELECTRICITY'] + outputs[i]['year_balance'].loc['WIND_OFFSHORE', 'ELECTRICITY']
            data['ELY_LOAD_FACTOR'].append(alk_ely_load_factor)
            data['PV_PROD'].append(pv_prod)
            data['WIND_PROD'].append(wind_prod)
            data['H2_PROD'].append((outputs[i]['year_balance'].loc['ALKALINE_ELECTROLYSIS', 'H2']+outputs[i]['year_balance'].loc['HT_ELECTROLYSIS', 'H2'])/1000)
        return(data)

    def add_list_storage (outputs, i, data):
        #print(outputs[i])
        if outputs[i] == False:
            data['NG_STORAGE'].append(None)
            data['H2_STORAGE'].append(None)
            data['METHANOL_STORAGE'].append(None)
            data['AMMONIA_STORAGE'].append(None)
        elif ('energy_stored' not in outputs[i]):
            data['NG_STORAGE'].append(None)
            data['H2_STORAGE'].append(None)
            data['METHANOL_STORAGE'].append(None)
            data['AMMONIA_STORAGE'].append(None)
        else: 
            plotdata = outputs[i]['energy_stored']
            plotdata = plotdata.fillna(0)
            colonnes_zeros = plotdata.columns[plotdata.eq(0).all()]
            plotdata = plotdata.drop(colonnes_zeros, axis=1)
            col_sum = plotdata.abs().sum()

            # Supress vectors with not enough energy stored
            threshold = 8760
            cols_to_drop = col_sum[col_sum < threshold].index
            plotdata = plotdata.drop(cols_to_drop, axis=1)

            names_column = plotdata.columns
            plotdata = plotdata.reset_index()
            plotdata = plotdata[::24]
            column_storage_out = plotdata.columns[plotdata.columns.str.endswith('_out')]
            column_storage_in = plotdata.columns[plotdata.columns.str.endswith('_in')]
            names_column = names_column.difference(column_storage_in).difference(column_storage_out)
            plotdata[names_column] = plotdata[names_column] - plotdata[names_column].min(axis=0)
            ng_storage = max(plotdata['GAS_STORAGE'])
            h2_storage = max(plotdata['H2_STORAGE'])
            data['NG_STORAGE'].append(ng_storage)
            data['H2_STORAGE'].append(h2_storage)
            data['METHANOL_STORAGE'].append(max(plotdata['METHANOL_STORAGE']))
            data['AMMONIA_STORAGE'].append(max(plotdata['AMMONIA_STORAGE']))
        return(data)

    def add_list_dac (outputs, i, data):
        if outputs[i] == False:
            data['DAC'].append(None)
        else: 
            dac = outputs[i]['year_balance'].loc['DAC_LT', 'CO2_CAPTURED'] + outputs[i]['year_balance'].loc['DAC_HT', 'CO2_CAPTURED']
            data['DAC'].append(dac)
        return(data)

    def add_list_prod_fuel (outputs, i, data):
        if outputs[i] == False:
            data['METHANOL_PROD'].append(None)
        else: 
            dac = outputs[i]['year_balance'].loc['CO2_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['WOOD_TO_METHANOL', 'METHANOL'] + outputs[i]['year_balance'].loc['E_WOOD_TO_METHANOL', 'METHANOL']
            data['METHANOL_PROD'].append(dac)
        return(data)

    def add_list_share_transport (outputs, i, data):
        if outputs[i] == False:
            data['TRUCK_H2'].append(None)
        else: 
            data['TRUCK_H2'].append(100*(outputs[i]['year_balance'].loc['TRUCK_FUEL_CELL', 'MOB_FREIGHT_ROAD'])/(outputs[i]['year_balance'].loc[outputs[i]['year_balance'].loc[:,'MOB_FREIGHT_ROAD' ].ge(10),'MOB_FREIGHT_ROAD' ].sum()) )
        return(data)
    
    outputs = read_data_post_process(directory_path, hourly_read, name_folder_scenario)
    data = {'CASE_NUMBER': [], 'FOLDER_NAME': [], 'E_FUEL': [], 'E_BIO_FUEL': [], 'BIOFUEL': [], 'TOTAL_FUEL_PRODUCED': [],
                'COST': [], 'BIOMASS_SEQU': [], 'SEQU': [], 'ELEC': [],
                'BIOMASS_USE': [], 'CC_SHARE': [], 'QTT_JETFUEL_IMP': [], 'QTT_JETFUEL_RE_IMP': [],
                'ELY_LOAD_FACTOR': [], 'PV_PROD': [], 'WIND_PROD': [], 'H2_PROD': [],
                'NG_STORAGE': [], 'H2_STORAGE': [], 'METHANOL_STORAGE': [], 'AMMONIA_STORAGE': [],
                'DAC': [], 'METHANOL_PROD': [], 'TRUCK_H2': [], 'PRICE_QTT_JETFUEL_IMPORT': [], 
                'SHARE_BIOFUEL_PROD_FT': [], 'SHARE_EBIOFUEL_PROD_FT': [], 'SHARE_EFUEL_PROD_FT': [],
                'HYDROGEN_PROD_FT': [], 'BIOMASS_PROD_FT': [],'CO2_PROD_FT': [], 'EMI_REDUC_JETFUEL': [], 'PRICE_JETFUEL_RE_IMPORT': [],
                'BIOMETHANE_PROD': [], 'E_BIOMETHANE_PROD': [], 'E_METHANE_PROD': [], 'PROD_ELEC_CCGT': [],
                'GASOLINE_TO_HVC': [], 'SHARE_METHANOL_TO_HVC': [], 'SHARE_JETFUEL_OUT_FT': []}
    for i in range (0, len(outputs)):
        data['CASE_NUMBER'].append(i)
        data['FOLDER_NAME'].append(outputs[i]['folder_name'])
        data['PRICE_QTT_JETFUEL_IMPORT'].append(outputs[i]['cost_breakdown'].loc['JETFUEL_RE', 'C_op'])
        data['PRICE_JETFUEL_RE_IMPORT'].append(outputs[i]['cost_breakdown'].loc['JETFUEL_RE', 'C_op']/outputs[i]['year_balance'].loc['JETFUEL_RE', 'JETFUEL'])
        data['SHARE_BIOFUEL_PROD_FT'].append(round(outputs[i]['year_balance'].loc['WOOD_TO_FT', 'FT_FUEL']/(outputs[i]['year_balance'].loc['CO2_TO_FT', 'FT_FUEL']+outputs[i]['year_balance'].loc['WOOD_TO_FT', 'FT_FUEL']+outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'FT_FUEL']), 3))
        data['SHARE_EBIOFUEL_PROD_FT'].append(round(outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'FT_FUEL']/(outputs[i]['year_balance'].loc['CO2_TO_FT', 'FT_FUEL']+outputs[i]['year_balance'].loc['WOOD_TO_FT', 'FT_FUEL']+outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'FT_FUEL']), 3))
        data['SHARE_EFUEL_PROD_FT'].append(round(outputs[i]['year_balance'].loc['CO2_TO_FT', 'FT_FUEL']/((outputs[i]['year_balance'].loc['CO2_TO_FT', 'FT_FUEL']+outputs[i]['year_balance'].loc['WOOD_TO_FT', 'FT_FUEL']+outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'FT_FUEL'])), 3))
        data['HYDROGEN_PROD_FT'].append(-round((outputs[i]['year_balance'].loc['CO2_TO_FT', 'H2']+outputs[i]['year_balance'].loc['WOOD_TO_FT', 'H2']+outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'H2']), 1))
        data['BIOMASS_PROD_FT'].append(-round((outputs[i]['year_balance'].loc['CO2_TO_FT', 'WOOD']+outputs[i]['year_balance'].loc['WOOD_TO_FT', 'WOOD']+outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'WOOD']), 1))
        data['CO2_PROD_FT'].append(-round((outputs[i]['year_balance'].loc['CO2_TO_FT', 'CO2_CAPTURED']+outputs[i]['year_balance'].loc['WOOD_TO_FT', 'CO2_CAPTURED']+outputs[i]['year_balance'].loc['E_WOOD_TO_FT', 'CO2_CAPTURED']), 1))
        data['EMI_REDUC_JETFUEL'].append(0)#str(int(0.1-outputs[i]['year_balance'].loc['JETFUEL_RE', 'CO2_ATMOSPHERE']/outputs[i]['year_balance'].loc['JETFUEL_RE', 'JETFUEL']*100/0.26)))
        data['BIOMETHANE_PROD'].append(outputs[i]['year_balance'].loc['WOOD_TO_METHANE', 'GAS'])
        data['E_BIOMETHANE_PROD'].append(outputs[i]['year_balance'].loc['E_WOOD_TO_METHANE', 'GAS'])
        data['E_METHANE_PROD'].append(outputs[i]['year_balance'].loc['CO2_TO_METHANE', 'GAS'])
        data['GASOLINE_TO_HVC'].append(outputs[i]['year_balance'].loc['OIL_TO_HVC', 'HVC'])
        data['SHARE_METHANOL_TO_HVC'].append(100*outputs[i]['year_balance'].loc['METHANOL_TO_HVC', 'HVC']/outputs[i]['year_balance'].loc[outputs[i]['year_balance'].loc[:,'HVC' ].ge(100),'HVC' ].sum())
        data['SHARE_JETFUEL_OUT_FT'].append(-outputs[i]['year_balance'].loc['REFINERY_JETFUEL', 'JETFUEL']/outputs[i]['year_balance'].loc['REFINERY_JETFUEL', 'FT_FUEL'])
        data['PROD_ELEC_CCGT'].append(outputs[i]['year_balance'].loc['CCGT', 'ELECTRICITY'])
        add_list_share_e_biofuel(outputs, i, data)
        add_list_cost (outputs, i, data)
        add_list_sequ (outputs, i, data)
        add_list_elec (outputs, i, data)
        add_list_biomass_use(outputs, i, data)
        add_list_share_carbon_captured (outputs, i, data)
        add_list_qtt_jetfuel_imp (outputs, i, data)
        add_list_ely_load_factor (outputs, i, data)
        add_list_dac (outputs, i, data)
        add_list_storage (outputs, i, data)
        add_list_prod_fuel (outputs, i, data)
        add_list_share_transport (outputs, i, data)
    #print(data)
    df = pd.DataFrame(data)
    return(df)