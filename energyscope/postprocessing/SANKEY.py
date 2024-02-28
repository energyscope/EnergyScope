import pandas as pd
import csv
import os
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import colors

def Sankey_plot(df, storage):
    """Generates a Sankey plot of the energy flows from a Pandas DataFrame.

    Args:
        df: A Pandas DataFrame containing the energy flows between technologies.
        storage: A Pandas DataFrame containing the flows of energy stored over time
    Returns:
        A Plotly Sankey plot.
    """
    list_storage = ["BATT_LI", "BEV_BATT", "PHEV_BATT", "PHS", "TS_DEC_DIRECT_ELEC", "TS_DEC_HP_ELEC", "TS_DEC_THHP_GAS", "TS_DEC_COGEN_GAS", "TS_DEC_COGEN_OIL", "TS_DEC_ADVCOGEN_GAS", "TS_DEC_ADVCOGEN_H2", "TS_DEC_BOILER_GAS", "TS_DEC_BOILER_WOOD", "TS_DEC_BOILER_OIL", "TS_DHN_DAILY", "TS_DHN_SEASONAL", "TS_HIGH_TEMP", "H2_STORAGE"]
    #Reforming the dataframe to be ready for the plot
    df = df.reset_index()
    print(df)
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != 'END_USES_DEMAND' and 'URANIUM': #Warning : There is a space before and after the name for the lines
            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)
            name_row = dfi2['Tech'].item()
            
            for col in dfi2:
                #To make a plot where the storage is looping
                if col not in  ['Tech', 'END_USES_DEMAND', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'URANIUM', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    if i in list_storage:
                        VAL_in = storage.loc[i][col+'_in']
                        VAL_out = storage.loc[i][col+'_out']
                        if (VAL_out)<500:
                            VAL_in, VAL_out = 0, 0
                        if i.startswith('TS_DEC'):
                            i = 'TS_DEC'
                        SOURCE, TARGET = col, i 
                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VAL_in}, ignore_index=True)
                        sankey_df = sankey_df.append({'source': TARGET, 'target': SOURCE, 'realValue': VAL_out}, ignore_index=True)
                    else:
                        VAL = dfi2[col].item()
                        if col == name_row:
                            name_row = name_row +'_IMP'
                        if abs(VAL)>500:
                            if VAL >=0:
                                SOURCE, TARGET, VALUE = name_row , col, VAL
                            else:
                                SOURCE, TARGET, VALUE = col, name_row, -VAL
                            sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
                
                if col in ['END_USES_DEMAND']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
        if i == 'END_USES_DEMAND': #plot the end_uses demand differentiated by the vector

            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)
            name_row = dfi2['Tech'].item()
            for col in dfi2:
                if col not in ['Tech', 'MOB_PRIVATE', 'MOB_AVIATION', 'MOB_PUBLIC', 'MOB_FREIGHT_RAIL', 'MOB_FREIGHT_ROAD', 'HVC', 'MOB_SHIPPING']:
                    VAL = dfi2[col].item()
                    print(VAL, '1', col, 2, name_row)
                    if abs(VAL)>500:
                        SOURCE, TARGET, VALUE = col, 'EUD_'+col, -VAL
                    sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)

    #To plot the EUD with energy unit instead of final demand unit
    EUD_energy_unit = True
    if EUD_energy_unit == True :
        for EUD in ['MOB_PRIVATE', 'MOB_AVIATION', 'MOB_PUBLIC', 'MOB_FREIGHT_RAIL', 'MOB_FREIGHT_ROAD']:
            list_source_EUD = sankey_df[sankey_df['target']==EUD]['source'] #Get the different source for the EUD
            for i in range (0, list_source_EUD.size):
                name_source = list_source_EUD.iloc[i] #Get the name of the different source
                if sankey_df[sankey_df['target']==name_source]['realValue'].size != 0: #Replace the value with the corresponding energy value
                    sankey_df['realValue'][(sankey_df['target']==EUD) & (sankey_df['source']==name_source)] = sankey_df[sankey_df['target']==name_source]['realValue'].iloc[0]

    #Generating the sankey
    ss = sankey_df['source'].tolist()
    tt = sankey_df['target'].tolist()
    st = ss+tt
    st_uni = list(set(st))
    pos_source = [st_uni.index(i) for i in ss]
    pos_target = [st_uni.index(i) for i in tt]
    
    change_color = True #True to make the node and link corresponding to the color in techno_color file
    print(list(map(str, sankey_df['realValue'].tolist())))
    if change_color == True :
        techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
        COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item() for i in st_uni]
        NAME_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Name_sankey'].item() for i in st_uni]
        sankey_df_color = [make_rgb_transparent(techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].iloc[0],  0.5) for i in ss]
        Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, 'color' : COLOR_node, 'label':NAME_node},
            link={"source": pos_source,"target": pos_target, "value": sankey_df['realValue'].tolist(), "customdata": sankey_df['realValue'].tolist(),"arrowlen" : 20,'color': sankey_df_color}))
    else:
        Sankey = go.Figure(go.Sankey(
        node={
            'pad': 10,
            'thickness': 20,
            'label': st_uni
        },
        link={
            "source": pos_source,
            "target": pos_target,
            "value": sankey_df['realValue'].tolist(),
            "label": sankey_df['realValue'].tolist()
        }))
    #Sankey.update_layout(title_text="Sankey Diagram", font_size=10, font_family="Times New Roman")
    return Sankey



def Sankey_carbon(df, gwp_construct):
    """Generates a Sankey plot of the carbon flows from a Pandas DataFrame.

    Args:
        df: A Pandas DataFrame containing the energy flows between technologies.
        gwp_construct: A Pandas DataFrame containing the global warming potential (GWP) of construction materials.

    Returns:
        A Plotly Sankey plot.
    """
    resources = pd.read_excel(os.path.join(os.getcwd(), '2020', "resources.xlsx"), header=2, index_col=False)
    df = df.reset_index()

    # Create a new DataFrame to store the data for the Sankey plot.
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])

    # Iterate over each technology in the df DataFrame.
    for i in df['Tech']:
        if i != 'END_USES_DEMAND': #Warning : There is a space before and after the name for the lines
            dfi = df[df['Tech']==i]
            
            dfi2 = dfi[dfi!=0].dropna(axis=1)   
            name_row = dfi2['Tech'].item()      
            # Iterate over each column in the technology's DataFrame.
            for col in dfi2:
                # If the column is one of the GHG emissions columns, then add a new row to the sankey_df DataFrame.
                if col == name_row:
                    name_row = name_row +'_IMP'
                if col in  ['CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'OTHER_GHG']:
                    VAL = dfi2[col].item()

                    # Link directly some node for a more efficient representation
                    if (name_row == 'GHG_EMISSIONS' and col == 'OTHER_GHG') or (name_row == 'CO2_EMISSIONS' and col=='CO2_DECENTRALISED') or (name_row == 'CO2_ATMOSPHERE_IMP' and col=='CO2_CENTRALISED'):
                        name_row = 'CO2_ATMOSPHERE'
                    if (name_row == 'GHG_EMISSIONS' and col == 'CO2_ATMOSPHERE') or (name_row == 'CO2_EMISSIONS' and col == 'CO2_ATMOSPHERE') or (name_row == 'CO2_ATMOSPHERE_IMP' and col == 'CO2_ATMOSPHERE'):
                        VAL = 0

                    # Supress some small flows for a more efficient representation
                    if abs(VAL)>100:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row, col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL

                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)

                # The carbon flows are calculated by multiplying the energy flow by the CO2 emission factor for the energy source.
                if col in  ['GAS', 'JETFUEL', 'WOOD', 'DIESEL', 'GASOLINE', 'LFO', 'COAL', 'WET_BIOMASS', 'METHANOL', 'WASTE', 'CEMENT_PROCESS', 'FT_FUEL', 'HVC']:
                    if col=='HVC':
                        VAL = dfi2[col].item() * 0.24
                    else:
                        VAL = dfi2[col].item() * resources[resources['parameter name']==col]['CO2_op'].item()

                    if abs(VAL)>100:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row, col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL

                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)

    # Add the emissions due to construction of technologies
    sankey_df = sankey_df.append({'source': 'GHG_CONSTRUCTION', 'target': 'CO2_ATMOSPHERE', 'realValue': gwp_construct['GWP_constr'].sum()}, ignore_index=True)

    ss = sankey_df['source'].tolist()
    tt = sankey_df['target'].tolist()
    st = ss+tt
    st_uni = list(set(st))

    pos_source = [st_uni.index(i) for i in ss]
    pos_target = [st_uni.index(i) for i in tt]
    change_color = True #True to make the node and link corresponding to the color in techno_color file
    if change_color == True :
        techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
        COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_carbon'].item() for i in st_uni]
        NAME_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Name_sankey'].item() for i in st_uni]
        sankey_df_color = [make_rgb_transparent(techno_color[techno_color['Name']==i.replace(' ', '')]['Color_carbon'].item(),  0.5) for i in tt]
        Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, 'color' : COLOR_node, 'label':NAME_node},
            link={"source": pos_source,"target": pos_target,"value": sankey_df['realValue'].tolist(), "label": sankey_df['realValue'].tolist(),  'color': sankey_df_color, "arrowlen" : 15})
        )#,visible=True)
    else : 
        Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, },
            link={"source": pos_source,"target": pos_target,"value": sankey_df['realValue'].tolist(), "label": sankey_df['realValue'].tolist(), "arrowlen" : 150}))
    
    #Sankey.update_layout(title_text="Sankey Diagram", font_size=10, font_family="Times New Roman")
    return Sankey


def make_rgb_transparent(color, alpha):
    """Take a color in the form of text like 'red' and convert it into a rgb color and adding alpha as a transp"""
    rgb = colors.colorConverter.to_rgb(color)
    return ("rgba(" + str(255*rgb[0]) + "," + str(255*rgb[1]) + "," + str(255*rgb[2]) + "," + str(alpha) + ")" )
