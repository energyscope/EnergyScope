import os
from pathlib import Path
import energyscope as es
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

analysis_sensibility_only = False

if not analysis_sensibility_only:
    OUTPUTS = []
    # define project path
    project_path = Path(__file__)#.parents[1]
    sensibility_data = pd.read_excel(os.path.join(project_path, 'sensibility_data.xlsx'))
    number_of_cases = sensibility_data['Case_number'].loc[-1]
    print(number_of_cases)
    for case_number in range(1, number_of_cases+1):
        analysis_only= True
        compute_TDs = True



        # loading the config file into a python dictionnary
        config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
        config['GWP_limit'] = str(GWP_limit) + ';'
        config['case_studies'] = os.join(project_path, 'case_studies', 'sensibility', 'test_sensibility')
        config['case_study'] = 'GWP_limit=' + str(GWP_limit)
        config['Working_directory'] = os.getcwd() # keeping current working directory into config
        
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
        if config['print_sankey']:
            #sankey_path = config['cs_path']/ config['case_study'] / 'output' / 'sankey'
            #es.drawSankey(path=sankey_path)
            fig = es.Sankey_plot('C:/Users/LM272782/Documents/Energyscope/FRANCE/Version_Python_Carbone/case_studies/' + config['case_study'] + '/output')
            fig.show()
            fig = es.Sankey_carbon('C:/Users/LM272782/Documents/Energyscope/FRANCE/Version_Python_Carbone/case_studies/' + config['case_study'] + '/output')
            fig.show()
            print(1)

        # Reading outputs
        #outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN'])
        
        outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=[])
        outputs['GWP_limit'] = GWP_limit
        print(outputs)
        OUTPUTS.append(outputs)

analysis = False
if analysis == True :
    techno_color = pd.read_csv(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color_3.csv"), delimiter =';',  index_col=False)

    COST_keys = OUTPUTS[0]['cost_breakdown'].index    
    COST = pd.DataFrame(columns=COST_keys.insert(0,'GWP_LIMIT').insert(1, 'Total_Cost'))

    for i in range(0,11):
        gwp_limit = OUTPUTS[i]['GWP_limit']
        COST.loc[i, COST_keys] = OUTPUTS[i]['cost_breakdown'].sum(axis=1).transpose()
        COST.loc[i, 'GWP_LIMIT'] = gwp_limit
        COST.loc[i, 'Total_Cost'] = OUTPUTS[i]['cost_breakdown'].sum(axis=1).transpose().sum()


    print_cost = True
    if print_cost == True :
        COST_keys_drop = COST[COST_keys].sum()[COST[COST_keys].sum() < 10000].index
        COST = COST.drop(COST_keys_drop, axis=1)
        COST_keys_updated = COST_keys.difference(COST_keys_drop)

        COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item() for i in COST_keys_updated.to_list()]
        fig = px.bar(COST.fillna(0), x='GWP_LIMIT', y=COST_keys_updated.to_list(), color_discrete_sequence= COLOR_node ,title='Total Cost as a function of GHG emission limit')
        fig.update_yaxes(title_text='Total Cost (MEUR)')
        fig.update_xaxes(title_text='GHG Emission limit (Kt CO2eq)')
        fig.update_layout(height=700)
        fig.show()


        std_values = COST.drop(['GWP_LIMIT', 'Total_Cost'], axis=1).std()
        print(std_values.sum(), COST['Total_Cost'].std())
        sorted_columns = std_values.sort_values(ascending=False)
        trace = go.Bar(x=sorted_columns.index, y=sorted_columns.values)

        # Create the layout
        layout = go.Layout(
            title='Principal contribution to the variation of the cost',
            xaxis=dict(title='Technologies'),
            yaxis=dict(title='Standard Deviation')
        )

        # Create the figure and add the trace
        fig = go.Figure(data=[trace], layout=layout)

        # Show the figure
        fig.show()
    print_emission = False
    if print_emission == True :
        from plotly.subplots import make_subplots
        print(OUTPUTS[0]['year_balance']['CO2_CENTRALISED'])
        fig = make_subplots(rows=2, cols=2, subplot_titles=['CO2_CENTRALISED', 'CO2_DECENTRALISED', 'CO2_ATMOSPHERE', 'OTHER_GHG'])
        GWP_keys = OUTPUTS[0]['year_balance'].index    
        GWP = pd.DataFrame(index=GWP_keys.insert(0,'GWP_LIMIT'))
        CO2_CENTRALISED = pd.DataFrame(columns=GWP_keys.insert(0,'GWP_LIMIT'))
        CO2_DECENTRALISED = pd.DataFrame(columns=GWP_keys.insert(0,'GWP_LIMIT'))
        CO2_ATMOSPHERE = pd.DataFrame(columns=GWP_keys.insert(0,'GWP_LIMIT').insert(1, 'GWP_Construction'))
        OTHER_GHG = pd.DataFrame(columns=GWP_keys.insert(0,'GWP_LIMIT'))
        GHG_CONSTR = pd.DataFrame(columns=OUTPUTS[0]['gwp_breakdown'].index.insert(0,'GWP_LIMIT'))

        for i in range(0,11):
            GWP_limit = OUTPUTS[i]['GWP_limit']
            
            CO2_CENTRALISED.loc[i, GWP_keys] = OUTPUTS[i]['year_balance']['CO2_CENTRALISED'].transpose()
            CO2_DECENTRALISED.loc[i, GWP_keys] = OUTPUTS[i]['year_balance']['CO2_DECENTRALISED'].transpose()
            CO2_ATMOSPHERE.loc[i, GWP_keys] = OUTPUTS[i]['year_balance']['CO2_ATMOSPHERE'].transpose()
            CO2_ATMOSPHERE.loc[i, 'GWP_Construction'] = OUTPUTS[i]['gwp_breakdown']['GWP_constr'].sum()
            CO2_ATMOSPHERE.loc[i, GWP_keys] = OUTPUTS[i]['year_balance']['CO2_ATMOSPHERE'].transpose()
            OTHER_GHG.loc[i, GWP_keys] = OUTPUTS[i]['year_balance']['OTHER_GHG'].transpose()
            GHG_CONSTR.loc[i, GWP_keys] = OUTPUTS[i]['gwp_breakdown']['GWP_constr'].transpose()
            print(GWP_limit)
            for df in [CO2_CENTRALISED,CO2_DECENTRALISED,CO2_ATMOSPHERE,OTHER_GHG, GHG_CONSTR]:
                df.loc[i, 'GWP_LIMIT'] = GWP_limit

        df_keys = GWP_keys
        print(CO2_CENTRALISED)
        fig = make_subplots(rows=4, cols=1, subplot_titles=['CO2_ATMOSPHERE', 'CO2_CENTRALISED', 'CO2_DECENTRALISED',  'OTHER_GHG', 'GHG_CONSTR'])
        i = 0
        for df in [CO2_ATMOSPHERE,CO2_CENTRALISED,CO2_DECENTRALISED,OTHER_GHG, GHG_CONSTR]:
            i = i+1
            COST_keys_drop = df[df_keys].sum()[df[df_keys].abs().sum() < 1000].index
            df = df.drop(COST_keys_drop, axis=1)
            if i != 1:
                df_keys_updated = df_keys.difference(COST_keys_drop).difference(['CO2_EMISSIONS', 'CO2_ATMOSPHERE', 'GHG_EMISSIONS'])
            else:
                df_keys_updated = df_keys.difference(COST_keys_drop).insert(0, 'GWP_Construction')
            """COLOR_node = {i : techno_color[techno_color['Name'] == i.replace(' ', '')]['Color_vector'].item() for i in df_keys_updated.to_list()}
            for j in df_keys_updated:
                fig.add_trace(go.Bar(x=df['GWP_LIMIT'], y=df[j], name=j, marker_color=COLOR_node[j], base="stack"), row=i, col=1)"""
            
            #Separate plot version
            COLOR_node = [techno_color[techno_color['Name'] == i.replace(' ', '')]['Color_vector'].item() for i in df_keys_updated.to_list()]
            fig = px.bar(df.fillna(0), x='GWP_LIMIT', y=df_keys_updated.to_list(), color_discrete_sequence=COLOR_node)
            fig.update_yaxes(title_text='Emission (Kt CO2eq)')
            fig.update_xaxes(title_text='GHG Emission limit (Kt CO2eq)')
            #fig['layout'].update(barmode='stack')
            fig.show()


#print(pd.concat([OUTPUTS[0], OUTPUTS[1]], keys='GWP_limit'))  
#px.line(OUT)