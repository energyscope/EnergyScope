import pandas as pd
import csv
import os
import plotly.graph_objects as go
import plotly.express as px


def Sankey_plot(df):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    del df['\n']
    
    #Reforming the dataframe to be ready for the plot
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != ' END_USES_DEMAND ' and ' URANIUM ': #Warning : There is a space before and after the name for the lines
            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)
            for col in dfi2:
                if col not in  ['Tech', 'END_USES_DEMAND', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'URANIUM']:
                    VAL = dfi2[col].item()
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = dfi2['Tech'].item(), col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, dfi2['Tech'].item(), -VAL
                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
    #sankey_df.to_csv(os.path.join(path_output, "sankey.csv"), index=False, header=True)

    #To plot the EUD with energy unit
    EUD_energy_unit = True
    if EUD_energy_unit == True :
        for EUD in ['MOB_PRIVATE', 'MOB_AVIATION', 'MOB_PUBLIC', 'MOB_FREIGHT_RAIL', 'MOB_FREIGHT_ROAD']:
            list_source_EUD = sankey_df[sankey_df['target']==EUD]['source'] #Get the different source for the EUD
            for i in range (0, list_source_EUD.size):
                name_source = list_source_EUD.iloc[i] #Get the name of the different source
                if sankey_df[sankey_df['target']==name_source]['realValue'].size != 0: #Replace the value with the corresponding energy value
                    sankey_df['realValue'][(sankey_df['target']==EUD) & (sankey_df['source']==name_source)] = sankey_df[sankey_df['target']==name_source]['realValue'].iloc[0]

    #Generating the sankey
    #print(sanke)
    ss = sankey_df['source'].tolist()
    tt = sankey_df['target'].tolist()
    st = ss+tt
    st_uni = list(set(st))
    pos_source = [st_uni.index(i) for i in ss]
    pos_target = [st_uni.index(i) for i in tt]
    
    change_color = False
    
    if change_color == True :
        
        techno_color = pd.read_csv(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color_3.csv"), delimiter =';',  index_col=False)
        COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item() for i in st_uni]
        sankey_df_color = [make_rgb_transparent(techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].iloc[0],  0.5) for i in ss]
        Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, 'color' : COLOR_node},
            link={"source": pos_source,"target": pos_target,"value": sankey_df['realValue'].tolist(), "label": sankey_df['realValue'].tolist(),'color': sankey_df_color}))
    else:
        Sankey = go.Figure(go.Sankey(
        node={
            'pad': 10,
            #'line': dict(color="black", width=0.5),
            'thickness': 20,
            'label': st_uni
        },
        link={
            "source": pos_source,
            "target": pos_target,
            "value": sankey_df['realValue'].tolist(),
            "label": sankey_df['realValue'].tolist()
        }))
    Sankey.update_layout(title_text="Sankey Diagram", font_size=10, font_family="Times New Roman")
    return Sankey



def Sankey_carbon(path_output):
    with open(os.path.join(path_output, 'year_balance.txt'), 'r') as infile:
        path = os.getcwd()
        with open(os.path.join(path_output, "pre_carbon_sankey.csv"), 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=';')
            for line in infile:
                fields = line.replace('\t', ';').split(';')
                writer.writerow(fields)
    df = pd.read_csv(os.path.join(path_output, "pre_carbon_sankey.csv"), delimiter =';', index_col=False)
    resources = pd.read_csv(os.path.join(path, '2020', "resources.csv"), delimiter =';', header=2, index_col=False)
    #print(resources)
    del df['\n']
    #Reforming the dataframe to be ready for the plot
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != ' END_USES_DEMAND ': #Warning : There is a space before and after the name for the lines
            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)            
            for col in dfi2:
                if col in  ['CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE']:
                    VAL = dfi2[col].item()
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = dfi2['Tech'].item(), col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, dfi2['Tech'].item(), -VAL

                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
                        
                        

                if col in  ['GAS', 'JETFUEL', 'WOOD', 'DIESEL', 'GASOLINE', 'LFO', 'COAL', 'WET_BIOMASS', 'METHANOL', 'WASTE']:
                    #print (resources[resources['parameter name']==col]['CO2_op'])
                    VAL = dfi2[col].item() * resources[resources['parameter name']==col]['CO2_op'].item()
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = dfi2['Tech'].item(), col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, dfi2['Tech'].item(), -VAL

                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)

    with open( os.path.join(path_output, 'gwp_breakdown.txt'), 'r') as infile:
        with open(os.path.join(path_output, "gwp_breakdown.csv"), 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=';')
            for line in infile:
                fields = line.replace('\t', ';').split(';')
                writer.writerow(fields)
    gwp_construct = pd.read_csv(os.path.join(path_output, "gwp_breakdown.csv"), delimiter =';', index_col=False)
    sankey_df = sankey_df.append({'source': 'GWP_Construction', 'target': 'CO2_ATMOSPHERE', 'realValue': gwp_construct['GWP_constr'].sum()}, ignore_index=True)
    print(sankey_df)
    sankey_df.to_csv(os.path.join(path_output, "carbon_sankey.csv"), index=False, header=True)
    #print(sankey_df)
    #sankey_df['color'] = sankey_df['color'].fillna('grey')
    #Generating the sankey
    ss = sankey_df['source'].tolist()
    tt = sankey_df['target'].tolist()
    st = ss+tt
    st_uni = list(set(st))


    pos_source = [st_uni.index(i) for i in ss]
    pos_target = [st_uni.index(i) for i in tt]
    change_color = False
    if change_color == False :
        techno_color = pd.read_csv(os.path.join(path, 'energyscope', 'postprocessing',"techno_color_3.csv"), delimiter =';',  index_col=False)
        COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_carbon'].item() for i in st_uni]
        sankey_df_color = [make_rgb_transparent(techno_color[techno_color['Name']==i.replace(' ', '')]['Color_carbon'].item(),  0.5) for i in tt]
        Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, 'color' : COLOR_node},
            link={"source": pos_source,"target": pos_target,"value": sankey_df['realValue'].tolist(), "label": sankey_df['realValue'].tolist(),'color': sankey_df_color}))
    else : 
        Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, },
            link={"source": pos_source,"target": pos_target,"value": sankey_df['realValue'].tolist(), "label": sankey_df['realValue'].tolist()}))
    
    Sankey.update_layout(title_text="Sankey Diagram", font_size=10, font_family="Times New Roman")
    #print(RGBColor)
    return Sankey

from matplotlib import colors
def make_rgb_transparent(color, alpha):
    """Take a color in the form of text like 'red' and convert it into a rgb color and adding alpha as a transp"""
    rgb = colors.colorConverter.to_rgb(color)
    return ("rgba(" + str(255*rgb[0]) + "," + str(255*rgb[1]) + "," + str(255*rgb[2]) + "," + str(alpha) + ")" )