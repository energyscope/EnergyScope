import pandas as pd
import csv
import os
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import colors

def Sankey_plot(df):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    #del df['\n']
    
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
                if col not in  ['Tech', 'END_USES_DEMAND', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'URANIUM', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
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
    
    change_color = True
    print(list(map(str, sankey_df['realValue'].tolist())))
    if change_color == True :
        
        techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
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



def Sankey_carbon(df, gwp_construct):

    #resources = pd.read_csv(, delimiter =';', header=2)
    resources = pd.read_excel(os.path.join(os.getcwd(), '2020', "resources.xlsx"), header=2, index_col=False)
    df = df.reset_index()
    print(df[df['Tech']=='AGRICULTURE_EMISSIONS']['OTHER_GHG'])
    #del df['\n']
    #Reforming the dataframe to be ready for the plot
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != 'END_USES_DEMAND': #Warning : There is a space before and after the name for the lines
            dfi = df[df['Tech']==i]
            
            dfi2 = dfi[dfi!=0].dropna(axis=1)   
            name_row = dfi2['Tech'].item()      
            for col in dfi2:
                if col == name_row:
                    name_row = name_row +'_IMP'
                if col in  ['CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'OTHER_GHG']:
                    VAL = dfi2[col].item()
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row, col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL

                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
                        
                        


                if col in  ['GAS', 'JETFUEL', 'WOOD', 'DIESEL', 'GASOLINE', 'LFO', 'COAL', 'WET_BIOMASS', 'METHANOL', 'WASTE', 'CEMENT_PROCESS']:
                    #print (resources[resources['parameter name']==col]['CO2_op'])
                    VAL = dfi2[col].item() * resources[resources['parameter name']==col]['CO2_op'].item()
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row, col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL

                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)


    sankey_df = sankey_df.append({'source': 'GWP_Construction', 'target': 'CO2_ATMOSPHERE', 'realValue': gwp_construct['GWP_constr'].sum()}, ignore_index=True)
    #print(sankey_df)
    #sankey_df.to_csv(os.path.join(path_output, "carbon_sankey.csv"), index=False, header=True)
    #print(sankey_df)
    #sankey_df['color'] = sankey_df['color'].fillna('grey')
    #Generating the sankey
    ss = sankey_df['source'].tolist()
    tt = sankey_df['target'].tolist()
    st = ss+tt
    st_uni = list(set(st))

    find_cycle_sankey(sankey_df)
    pos_source = [st_uni.index(i) for i in ss]
    pos_target = [st_uni.index(i) for i in tt]
    change_color = False
    if change_color == False :
        techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
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


def make_rgb_transparent(color, alpha):
    """Take a color in the form of text like 'red' and convert it into a rgb color and adding alpha as a transp"""
    rgb = colors.colorConverter.to_rgb(color)
    return ("rgba(" + str(255*rgb[0]) + "," + str(255*rgb[1]) + "," + str(255*rgb[2]) + "," + str(alpha) + ")" )

def sankey_cycle_test(df):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    #del df['\n']
    
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
                if col not in  ['Tech', 'END_USES_DEMAND', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'URANIUM', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
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
    print(sankey_df)
    return(find_cycle_sankey(sankey_df))


def has_cycle_sankey(df):
    graph = {}
    visited = set()

    # Conversion du DataFrame en une représentation de graphe
    for i, row in df.iterrows():
        source = row['source']
        target = row['target']
        if source not in graph:
            graph[source] = []
        graph[source].append(target)

    # Algorithme de détection de cycle (DFS)
    for node in graph:
        if node not in visited:
            if dfs(graph, node, visited, None):
                return True
    return False

def dfs(graph, node, node_initial,  list_cycle, visited, cycle_nodes):
    visited.append(node)
    #print(1, node, node_initial,  list_cycle)
    if node not in graph:
        return (False, 0)
    for neighbor in graph[node]:
        list_cycle = remove_elements_after_string(list_cycle, neighbor, graph[node])  
        if neighbor == node_initial:
            list_cycle.append(neighbor)
            cycle_nodes.append(list_cycle)
            #print(list_cycle, 'fafafa')
            #return(True, list_cycle)
        elif neighbor in graph and neighbor not in visited:
            list_cycle.append(neighbor)
            dfs(graph, neighbor, node_initial, list_cycle, visited, cycle_nodes)
         

    #return False
def remove_elements_after_string(lst, neighbor, graph_node):
    index = None
    for i, element in enumerate(graph_node):
        """if i == 0:
            #print(i)
            return(lst)"""
        if neighbor == element:
            target_string = graph_node[i-1]

    for i, element in enumerate(lst):
        if element == target_string:
            index = i
            break
    
    if index is not None:
        lst = lst[:index]

    return lst

from collections import Counter
def find_cycle_sankey(df):
    graph = {}
    visited = set()
    cycle_nodes = []
    CYCLE = []
    # Conversion du DataFrame en une représentation de graphe
    for i, row in df.iterrows():
        source = row['source']
        target = row['target']
        if target not in graph:
            graph[target] = []
        graph[target].append(source)
    #print(graph)
    # Algorithme de détection de cycle (DFS)
    for node in graph:
        #print(node, graph[node])#, visited)
        list_cycle = []
        visited = []
        
        result = dfs(graph, node, node, list_cycle, visited, cycle_nodes)
        #print(result)
        if result is not None or False :
            
            CYCLE.append(result[1]) 
    #print(remove_permutations(cycle_nodes), len(remove_permutations(cycle_nodes)), len(cycle_nodes))
    nodes_important = []
    for j in cycle_nodes:
        nodes_important.append(j[-1])
    print(nodes_important)
    return (remove_permutations(cycle_nodes))#, cycle_nodes)#, remove_permutations(cycle_nodes))





def check_permutations(liste):
    if not liste:
        return False

    counters = [Counter(sublist) for sublist in liste]
    first_counter = counters[0]

    for counter in counters[1:]:
        if counter != first_counter:
            return False

    return True

def remove_permutations(liste):
    unique_liste = []
    for sublist in liste:
        if not is_permutation_of_existing(unique_liste, sublist):
            unique_liste.append(sublist)
    return unique_liste

def is_permutation_of_existing(unique_liste, sublist):
    for existing_sublist in unique_liste:
        if len(existing_sublist) == len(sublist) and sorted(existing_sublist) == sorted(sublist):
            return True
    return False

"""if neighbor not in visited:
            if dfs(graph, neighbor, visited, node, cycle_nodes):
                cycle_nodes.add(neighbor)
                return True
        elif parent != neighbor:
            cycle_nodes.add(neighbor)
            return True"""




def Sankey_cost(df, assets, resources, cost_breakdown):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    #del df['\n']
    
    #Reforming the dataframe to be ready for the plot
    year_balance = df
    df = df.reset_index()
    print(df)
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != 0:#'END_USES_DEMAND' and 'URANIUM': #Warning : There is a space before and after the name for the lines 'END_USES_DEMAND'
            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)
            name_row = dfi2['Tech'].item()
            for col in dfi2:
                if col not in  ['Tech', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
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
    print(assets, resources)
    print(sankey_df)
    graph = {}
    # Conversion du DataFrame en une représentation de graphe
    for i, row in sankey_df.iterrows():
        source = row['source']
        target = row['target']
        if target not in graph:
            graph[target] = []
        graph[target].append(source)
    
    list_cycle = find_cycle_sankey(sankey_df)
    unique_list = []
    for sublist in list_cycle:
        unique_list += sublist
    unique_list = list(set(unique_list))
    COST = {}
    calculated = []
    sankey_cost = pd.DataFrame(columns=['source', 'target', 'realValue'])
    print(graph)
    for node in graph:
        if node not in unique_list:
            cost_iterator_calculator(graph, node, COST, None , cost_breakdown, unique_list, calculated, sankey_df, [list_cycle])
        if node not in COST:
            capex_parent, opex_parent, cost_energy = 0, 0, 0
            if all(elem in COST for elem in graph[node]):
                for neighbor_2 in graph[node]:
                    proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['target']==node)]['realValue'].sum()
                    cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 
                if node in cost_breakdown.index :
                    capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                COST[node] = (capex_parent, opex_parent, cost_energy)
    eud = 'MOB_PRIVATE'
    print(graph)
    print(cost_breakdown.loc['H2_ELECTROLYSIS'])
    print(COST)
    print([i for i in year_balance.columns], year_balance[eud].loc[year_balance[eud] > 0].sum())
    EUD = ['MOB_PRIVATE', 'MOB_AVIATION', 'MOB_PUBLIC', 'MOB_FREIGHT_RAIL', 'MOB_FREIGHT_ROAD', 'HEAT_HIGH_T', 'ELECTRICITY', 'HEAT_LOW_T_DHN', 'HEAT_LOW_T_DECEN', 'HVC', 'AMMONIA', 'METHANOL']
    total_cost = 0
    for eud in EUD:
        cost_eud = -(COST[eud][0] + COST[eud][1] + COST[eud][2])*(year_balance[eud].loc['END_USES_DEMAND']/(year_balance[eud].loc[year_balance[eud] > 0].sum()))
        total_cost += cost_eud
        cost_normalised = 1000*(COST[eud][0] + COST[eud][1] + COST[eud][2])/(year_balance[eud].loc[year_balance[eud] > 0].sum())
        print(eud, cost_normalised, 'EUR/(MWh-kpkm-ktkm)', (year_balance[eud].loc[year_balance[eud] > 0].sum()), (COST[eud][0] + COST[eud][1]))#, -year_balance[eud].loc['END_USES_DEMAND']/(year_balance[eud].loc[year_balance[eud] > 0].sum()), year_balance[eud].loc['END_USES_DEMAND'])
    print(total_cost)
    print(list_cycle)


def cost_iterator_calculator (graph, node, COST, parent, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, list_cycle, cycle_turn=0, name_proportion_min='Nothing'):
    #print(node, parent, COST)#, graph )


    if node not in graph:
        return(False)
    if node not in calculated:
        ######iterate over the preceding of the node #########
        for neighbor in graph[node]: 
            print(node, neighbor, cycle_turn)#, graph[node])#, COST)
            ##########objective compute the node where the proportion of the energy coming from the cycle is minimal########### 
            if cycle_turn == 0 and neighbor in list_all_nodes_cycle:
                for list_node_cycle in list_cycle: 
                    proportion_min, name_proportion_min = 1, 'nothing'
                    for i, node in enumerate(list_node_cycle):
                        if i == len(list_node_cycle)-1:
                            neighbor = list_node_cycle[0]               
                        else :
                            neighbor = list_node_cycle[i+1] 
                        #print(list_node_cycle)
                        #print(5, neighbor, node)
                        #print(sankey_df.loc[(sankey_df['source']==neighbor) & (sankey_df['target']==node)]['realValue'])
                        proportion_node = (sankey_df.loc[(sankey_df['source']==neighbor) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['target']==node)]['realValue'].sum()
                        if proportion_node <= proportion_min:
                            proportion_min, name_proportion_min, name_start_cycle = proportion_node, node, neighbor
                    print(5, proportion_min, name_proportion_min)
                    graph_cycle = [x for x in graph[name_proportion_min]if x not in list_node_cycle]
                    capex_parent, opex_parent, cost_energy = 0, 0, 0
                    print(graph_cycle)
                    for neighbor in  graph_cycle:
                        node = name_proportion_min
                        proportion = (sankey_df.loc[(sankey_df['source']==neighbor) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['target']==node)]['realValue'].sum()
                        if neighbor not in COST:
                            cost_iterator_calculator (graph, neighbor, COST, node, cost_breakdown, list_node_cycle, calculated, sankey_df, list_cycle)
                        cost_energy = cost_energy  + (COST[neighbor][1] + COST[neighbor][0] + COST[neighbor][2]) * proportion #transfère le coût sur l'usage suivant 
                        if node in cost_breakdown.index :
                            capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                        COST[node] = (capex_parent, opex_parent, cost_energy)
                    cycle_turn = cycle_turn + 1
                    print(7, node, name_start_cycle)
                    cost_iterator_calculator (graph, name_start_cycle, COST, parent, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, list_cycle, cycle_turn, name_proportion_min=node)

            # Compute the cost for the technologies and resources that are source of energy
            if neighbor not in graph:
                if neighbor.endswith('_IMP') : 
                    neighbor2 = neighbor[:-4]
                    capex_neighbor = cost_breakdown.loc[neighbor2]['C_inv'] 
                    opex_neighbor = cost_breakdown.loc[neighbor2]['C_maint'] + cost_breakdown.loc[neighbor2]['C_op']
                    COST[neighbor] = (capex_neighbor, opex_neighbor, 0)        
                else:
                    capex_neighbor = cost_breakdown.loc[neighbor]['C_inv'] 
                    opex_neighbor = cost_breakdown.loc[neighbor]['C_maint'] + cost_breakdown.loc[neighbor]['C_op']
                    COST[neighbor] = (capex_neighbor, opex_neighbor, 0)
                if neighbor not in list_all_nodes_cycle:
                    calculated.append(neighbor)
            
            #Base case to calculate all the preceding values
            elif neighbor not in list_all_nodes_cycle: 
                cost_iterator_calculator (graph, neighbor, COST, node, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, list_cycle, cycle_turn, name_proportion_min)
            
            # Iterate over the cycle 
            else : 
                print(2, node, neighbor, cycle_turn)
                if neighbor not in COST and cycle_turn <= 4:
                    cost_iterator_calculator (graph, neighbor, COST, node, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, list_cycle, cycle_turn, name_proportion_min)
                    print(3.5, node, neighbor, cycle_turn)
                capex_parent, opex_parent, cost_energy = 0, 0, 0
                if all(elem in COST for elem in graph[node]):
                    for neighbor_2 in graph[node]:
                        #, COST)
                        proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['target']==node)]['realValue'].sum()
                        cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 
                    if node in cost_breakdown.index :
                        capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                    COST[node] = (capex_parent, opex_parent, cost_energy)
                    #print('kas', name_proportion_min)
                    if name_proportion_min == node : 
                        print('kastor')
                        if cycle_turn >= 4:
                            print('kastor')
                            for j in list_all_nodes_cycle :
                                calculated.append(j)
                        cycle_turn = cycle_turn + 1
            
            #Compute the value of cost based on the value of the preceding 
            if parent != None :
                if neighbor == graph[node][-1] and neighbor not in list_all_nodes_cycle:
                    capex_parent, opex_parent, cost_energy = 0, 0, 0
                    if all(elem in COST for elem in graph[node]):
                        for neighbor in graph[node]:
                            print(parent, neighbor, node)
                            if neighbor not in COST :
                                cost_iterator_calculator (graph, neighbor, COST, node, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, list_cycle, cycle_turn, name_proportion_min)
                            if pd.isna(sankey_df.loc[(sankey_df['target']==neighbor)]['realValue'].sum()) == False :
                                proportion = (sankey_df.loc[(sankey_df['source']==neighbor) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor)]['realValue'].sum()
                            else: 
                                proportion = 1
                            print(proportion, sankey_df.loc[(sankey_df['target']==neighbor)]['realValue'].sum())
                            cost_energy = cost_energy  + (COST[neighbor][1] + COST[neighbor][0] + COST[neighbor][2]) * proportion #transfère le coût sur l'usage suivant 
                        if node in cost_breakdown.index :
                            capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                        print(node, capex_parent, opex_parent, cost_energy)
                        COST[node] = (capex_parent, opex_parent, cost_energy)
                        if neighbor not in list_all_nodes_cycle:
                            calculated.append(node)
                        


                                        #print(parent, neighbor, node)
                        #if neighbor.endswith('_IMP') :
                            #neighbor2 = neighbor[:-4]
                            #print([i for i in year_balance.columns], [i for i in year_balance.index])
                            #print(year_balance.loc['URANIUM'])#.loc['URANIUM'])#.loc['URANIUM'])


                        #proportion = (year_balance.loc[neighbor][node]/year_balance[neighbor].sum())

                        def sankey_cycle_test(df):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    #del df['\n']
    
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
                if col not in  ['Tech', 'END_USES_DEMAND', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'URANIUM', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
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
    print(sankey_df)
    return(find_cycle_sankey(sankey_df))


def has_cycle_sankey(df):
    graph = {}
    visited = set()

    # Conversion du DataFrame en une représentation de graphe
    for i, row in df.iterrows():
        source = row['source']
        target = row['target']
        if source not in graph:
            graph[source] = []
        graph[source].append(target)

    # Algorithme de détection de cycle (DFS)
    for node in graph:
        if node not in visited:
            if dfs(graph, node, visited, None):
                return True
    return False

def dfs(graph, node, node_initial,  list_cycle, visited, cycle_nodes):
    visited.append(node)
    #print(1, node, node_initial,  list_cycle)
    if node not in graph:
        return (False, 0)
    for neighbor in graph[node]:
        list_cycle = remove_elements_after_string(list_cycle, neighbor, graph[node])  
        if neighbor == node_initial:
            list_cycle.append(neighbor)
            cycle_nodes.append(list_cycle)
            #print(list_cycle, 'fafafa')
            #return(True, list_cycle)
        elif neighbor in graph and neighbor not in visited:
            list_cycle.append(neighbor)
            dfs(graph, neighbor, node_initial, list_cycle, visited, cycle_nodes)
         

    #return False
def remove_elements_after_string(lst, neighbor, graph_node):
    index = None
    for i, element in enumerate(graph_node):
        """if i == 0:
            #print(i)
            return(lst)"""
        if neighbor == element:
            target_string = graph_node[i-1]

    for i, element in enumerate(lst):
        if element == target_string:
            index = i
            break
    
    if index is not None:
        lst = lst[:index]

    return lst

from collections import Counter
def find_cycle_sankey(df):
    graph = {}
    visited = set()
    cycle_nodes = []
    CYCLE = []
    # Conversion du DataFrame en une représentation de graphe
    for i, row in df.iterrows():
        source = row['source']
        target = row['target']
        if target not in graph:
            graph[target] = []
        graph[target].append(source)
    #print(graph)
    # Algorithme de détection de cycle (DFS)
    for node in graph:
        #print(node, graph[node])#, visited)
        list_cycle = []
        visited = []
        
        result = dfs(graph, node, node, list_cycle, visited, cycle_nodes)
        #print(result)
        if result is not None or False :
            
            CYCLE.append(result[1]) 
    #print(remove_permutations(cycle_nodes), len(remove_permutations(cycle_nodes)), len(cycle_nodes))
    nodes_important = []
    for j in cycle_nodes:
        nodes_important.append(j[-1])
    print(nodes_important)
    return (remove_permutations(cycle_nodes))#, cycle_nodes)#, remove_permutations(cycle_nodes))





def check_permutations(liste):
    if not liste:
        return False

    counters = [Counter(sublist) for sublist in liste]
    first_counter = counters[0]

    for counter in counters[1:]:
        if counter != first_counter:
            return False

    return True

def remove_permutations(liste):
    unique_liste = []
    for sublist in liste:
        if not is_permutation_of_existing(unique_liste, sublist):
            unique_liste.append(sublist)
    return unique_liste

def is_permutation_of_existing(unique_liste, sublist):
    for existing_sublist in unique_liste:
        if len(existing_sublist) == len(sublist) and sorted(existing_sublist) == sorted(sublist):
            return True
    return False

"""if neighbor not in visited:
            if dfs(graph, neighbor, visited, node, cycle_nodes):
                cycle_nodes.add(neighbor)
                return True
        elif parent != neighbor:
            cycle_nodes.add(neighbor)
            return True"""


def cost_calculator(df, assets, resources, cost_breakdown):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    #del df['\n']
    
    #Reforming the dataframe to be ready for the plot
    year_balance = df
    df = df.reset_index()
    print(df)
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != 'END_USES_DEMAND':#'END_USES_DEMAND' and 'URANIUM': #Warning : There is a space before and after the name for the lines 'END_USES_DEMAND'
            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)
            name_row = dfi2['Tech'].item()
            for col in dfi2:
                if col not in  ['Tech', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
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
    print(assets, resources)
    print(sankey_df)
    graph = {}
    # Conversion du DataFrame en une représentation de graphe
    for i, row in sankey_df.iterrows():
        source = row['source']
        target = row['target']
        if target not in graph:
            graph[target] = []
        graph[target].append(source)
    
    list_cycle = find_cycle_sankey(sankey_df)
    unique_list = []
    for sublist in list_cycle:
        for j in sublist:
            #j.insert
            if j not in unique_list:
                unique_list.append(j)
    unique_list = list(set(unique_list))
    COST = {}
    calculated = []
    sankey_cost = {'source': [], 'target': [], 'realValue': []}#pd.DataFrame(columns=['source', 'target', 'realValue'])
    print(graph)
    print('List of nodes that are in a cycle', unique_list)
    print(-5, list_cycle)
    for node in graph:
        #print(1000, sankey_cost)
        #if node not in unique_list:
        print(-2, node, COST)
        cost_iterator_calculator(graph, node, COST, None , cost_breakdown, unique_list, calculated, sankey_df, sankey_cost, list_cycle)
        if node not in COST:
            capex_parent, opex_parent, cost_energy = 0, 0, 0
            if all(elem in COST for elem in graph[node]):
                for neighbor_2 in graph[node]:
                    proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['target']==node)]['realValue'].sum()
                    cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant
                    sankey_cost['source'].append(neighbor_2)
                    sankey_cost['target'].append(node)
                    sankey_cost['realValue'].append(((COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion))
                    #sankey_cost = sankey_cost.append({'source': neighbor_2, 'target': node, 'realValue': ((COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion)}, ignore_index=True)
                if node in cost_breakdown.index :
                    capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                COST[node] = (capex_parent, opex_parent, cost_energy)
    return(COST)

def cost_calculator_vector(df, COST, vector):
    """Return the cost of producing an energy vector given in EUR/MWh"""
    print(COST)
    return((COST[vector][0] + COST[vector][1] + COST[vector][2])/(df[vector].loc[df[vector] > 0].sum()))

def Sankey_cost(df, assets, resources, cost_breakdown):
    """df is the data frame generated from the outputs from the year_balance.txt file"""
    #del df['\n']
    
    #Reforming the dataframe to be ready for the plot
    year_balance = df
    df = df.reset_index()
    print(df)
    sankey_df = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for i in df['Tech']:
        if i != 0:#'END_USES_DEMAND' and 'URANIUM': #Warning : There is a space before and after the name for the lines 'END_USES_DEMAND'
            dfi = df[df['Tech']==i]
            dfi2 = dfi[dfi!=0].dropna(axis=1)
            name_row = dfi2['Tech'].item()
            for col in dfi2:
                if col not in  ['Tech', 'CO2_DECENTRALISED', 'CO2_CENTRALISED','CO2_CAPTURED', 'CO2_ATMOSPHERE', 'OTHER_GHG', 'RES_WIND', 'RES_HYDRO', 'RES_SOLAR', 'RES_GEO']:
                    VAL = dfi2[col].item()
                    if col == name_row:
                        name_row = name_row +'_IMP'
                    if abs(VAL)>0.1:
                        if VAL >=0:
                            SOURCE, TARGET, VALUE = name_row , col, VAL
                        else:
                            SOURCE, TARGET, VALUE = col, name_row, -VAL
                        sankey_df = sankey_df.append({'source': SOURCE, 'target': TARGET, 'realValue': VALUE}, ignore_index=True)
    #To plot the EUD with energy unit
    EUD_energy_unit = False
    if EUD_energy_unit == True :
        for EUD in ['MOB_PRIVATE', 'MOB_AVIATION', 'MOB_PUBLIC', 'MOB_FREIGHT_RAIL', 'MOB_FREIGHT_ROAD']:
            list_source_EUD = sankey_df[sankey_df['target']==EUD]['source'] #Get the different source for the EUD
            for i in range (0, list_source_EUD.size):
                name_source = list_source_EUD.iloc[i] #Get the name of the different source
                if sankey_df[sankey_df['target']==name_source]['realValue'].size != 0: #Replace the value with the corresponding energy value
                    sankey_df['realValue'][(sankey_df['target']==EUD) & (sankey_df['source']==name_source)] = sankey_df[sankey_df['target']==name_source]['realValue'].iloc[0]

    #Generating the sankey
    print(assets, resources)
    print(sankey_df)
    #Invert the source and the target so has for example the price of Pumped hydro storage cpntribute to the price of electricity
    list_storage = ['PHS', 'BEV_BATT', 'TS_DHN_HP_ELEC', 'TS_DHN_SEASONAL', 'TS_DEC_HP_ELEC', 'GAS_STORAGE', 'TS_DEC_THHP_GAS']
    for i, row in sankey_df.iterrows():
        if row['target'] in list_storage:
            sankey_df.loc[i, 'target'], sankey_df.loc[i, 'source'] = sankey_df.loc[i, 'source'], sankey_df.loc[i, 'target']
    graph = {}
    # Conversion du DataFrame en une représentation de graphe
    for i, row in sankey_df.iterrows():
        source = row['source']
        target = row['target']
        if target not in graph:
            graph[target] = []
        graph[target].append(source)
    
    list_cycle = find_cycle_sankey(sankey_df)
    unique_list = []
    for sublist in list_cycle:
        unique_list += sublist
    unique_list = list(set(unique_list))
    COST = {}
    calculated = []
    sankey_cost = {'source': [], 'target': [], 'realValue': []}#pd.DataFrame(columns=['source', 'target', 'realValue'])
    print(graph)
    print(list_cycle)
    
    list_cycle = [lst for lst in list_cycle if len(lst) >= 3]
    for node in graph:
        print(-2, node)#), COST)
        #if node not in unique_list:
        if node not in COST:
            cost_iterator_calculator(graph, node, COST, None , cost_breakdown, unique_list, calculated, sankey_df, sankey_cost, list_cycle)
        if node not in COST:
            capex_parent, opex_parent, cost_energy = 0, 0, 0
            if all(elem in COST for elem in graph[node]):
                for neighbor_2 in graph[node]:
                    
                    proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()
                    cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant
                    sankey_cost['source'].append(neighbor_2)
                    sankey_cost['target'].append(node)
                    sankey_cost['realValue'].append(((COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion))
                    #sankey_cost = sankey_cost.append({'source': neighbor_2, 'target': node, 'realValue': ((COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion)}, ignore_index=True)
                if node in cost_breakdown.index :
                    capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                COST[node] = (capex_parent, opex_parent, cost_energy)
    eud = 'MOB_PRIVATE'
    print([i for i in year_balance.columns], year_balance[eud].loc[year_balance[eud] > 0].sum())
    EUD = ['MOB_PRIVATE', 'MOB_AVIATION', 'MOB_PUBLIC', 'MOB_FREIGHT_RAIL', 'MOB_FREIGHT_ROAD', 'HEAT_HIGH_T', 'ELECTRICITY', 'HEAT_LOW_T_DHN', 'HEAT_LOW_T_DECEN', 'HVC', 'AMMONIA', 'METHANOL', 'JETFUEL', 'GASOLINE', 'DIESEL']
    total_cost = 0
    for eud in EUD:
        cost_eud = -(COST[eud][0] + COST[eud][1] + COST[eud][2])*(year_balance[eud].loc['END_USES_DEMAND']/(year_balance[eud].loc[year_balance[eud] > 0].sum()))
        total_cost += cost_eud
        cost_normalised = 1000*(COST[eud][0] + COST[eud][1] + COST[eud][2])/(year_balance[eud].loc[year_balance[eud] > 0].sum())
        print(eud, cost_normalised, 'EUR/(MWh-kpkm-ktkm)', (year_balance[eud].loc[year_balance[eud] > 0].sum()), (COST[eud][0] + COST[eud][1]))#, -year_balance[eud].loc['END_USES_DEMAND']/(year_balance[eud].loc[year_balance[eud] > 0].sum()), year_balance[eud].loc['END_USES_DEMAND'])

    sankey_cost_final = pd.DataFrame(columns=['source', 'target', 'realValue'])
    for index, row in sankey_df.iterrows():
        #print(row['source'], row['target'], row['realValue'], (COST[row['source']][0] + COST[row['source']][1] + COST[row['source']][2]), (sankey_df['realValue'][sankey_df['source']==row['source']].sum()))
        sankey_cost_final.loc[index, 'source'] = row['source']
        sankey_cost_final.loc[index, 'target'] = row['target']
        sankey_cost_final.loc[index, 'realValue'] = row['realValue'] * (COST[row['source']][0] + COST[row['source']][1] + COST[row['source']][2])/(sankey_df['realValue'][sankey_df['source']==row['source']].sum())
        print(row['target'], row['source'], row['realValue'] * (COST[row['source']][0] + COST[row['source']][1] + COST[row['source']][2])/(sankey_df['realValue'][sankey_df['source']==row['source']].sum()))    
    print(COST)
    print(sankey_cost_final)
    ss = sankey_cost_final['source'].tolist()
    tt = sankey_cost_final['target'].tolist()
    st = ss+tt
    st_uni = list(set(st))

    pos_source = [st_uni.index(i) for i in ss]
    pos_target = [st_uni.index(i) for i in tt]
    techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),  index_col=False)
    COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item() for i in st_uni]
    sankey_df_color = [make_rgb_transparent(techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item(),  0.5) for i in ss]
    Sankey = go.Figure(go.Sankey(
            node={'pad': 10, 'thickness': 20, 'label': st_uni, 'color' : COLOR_node},
            link={"source": pos_source,"target": pos_target,"value": sankey_cost_final['realValue'].tolist(), "label": sankey_cost_final['realValue'].tolist(), 'color': sankey_df_color}))
    
    
    Sankey.update_layout(title_text="Sankey Diagram", font_size=10, font_family="Times New Roman")
    return Sankey

def cost_iterator_calculator (graph, node, COST, parent, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, sankey_cost, list_cycle, cycle_turn=[0, 0], name_proportion_min='Nothing'):
    """The objective is to compute the cost of every vector in the energy system. 
    This function iterates over every vector and compute the cost of one vector based on the capex the opex and the cost of the energy"""
    print(-1, node)
    if node not in graph:
        print(0)
        if node.endswith('_IMP') : 
            node_2 = node[:-4]
            capex_neighbor = cost_breakdown.loc[node_2]['C_inv'] 
            opex_neighbor = cost_breakdown.loc[node_2]['C_maint'] + cost_breakdown.loc[node_2]['C_op']
            COST[node] = (capex_neighbor, opex_neighbor, 0)        
        else:
            capex_neighbor = cost_breakdown.loc[node]['C_inv'] 
            opex_neighbor = cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
            COST[node] = (capex_neighbor, opex_neighbor, 0)
        print(COST)
        if node not in list_all_nodes_cycle:
            #node has been calculated
            calculated.append(node)
    if node in COST:
        print('calculated', node)
    if node not in calculated and node not in COST:
        if all(elem in COST for elem in graph[node]):
            print(-0.5, node,)
            ######iterate over the preceding of the node #########
            if  node not in list_all_nodes_cycle:  #Test if node is belonging to a cycle
                capex_parent, opex_parent, cost_energy = 0, 0, 0
                if all(elem in COST for elem in graph[node]):
                    for neighbor_2 in graph[node]:
                        
                        if sankey_df.loc[(sankey_df['target']==neighbor_2)]['realValue'].sum() != 0 :
                            proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()
                        else: 
                            proportion = 1
                        cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 
                        print(1.4, node, neighbor_2, proportion, (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]))                    
                    if node in cost_breakdown.index :
                        capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                    COST[node] = (capex_parent, opex_parent, cost_energy)
                    
                    calculated.append(node)
        
        else:
            for neighbor in graph[node]: 
                ##########objective compute the node where the proportion of the energy coming from the cycle is minimal########### 
                print(0, node, neighbor)

            ######iterate over the preceding of the node #########
                #If neighbor has an antecedent 
                if neighbor in graph:
                    if all(elem in COST for elem in graph[neighbor]):
                        capex_parent, opex_parent, cost_energy = 0, 0, 0
                        for neighbor_2 in graph[neighbor]:
                            print(1.4, node, neighbor, neighbor_2)
                            if sankey_df.loc[(sankey_df['target']==neighbor_2)]['realValue'].sum() != 0 :
                                proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==neighbor)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()
                            else: 
                                proportion = 1
                            cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 
                        if neighbor in cost_breakdown.index :
                            capex_parent, opex_parent = cost_breakdown.loc[neighbor]['C_inv'], opex_parent + cost_breakdown.loc[neighbor]['C_maint'] + cost_breakdown.loc[neighbor]['C_op']
                        COST[neighbor] = (capex_parent, opex_parent, cost_energy)
                        
                        calculated.append(neighbor)
                #If neighbor is in a cycle and is in the first iteration over a cycle 
                if cycle_turn[0] == 0 and neighbor in list_all_nodes_cycle and neighbor not in COST:
                    for cycle_index, list_node_cycle in enumerate(list_cycle): 
                        cycle_turn = [0, cycle_index]
                        proportion_min, name_proportion_min = 1.4, 'nothing'
                        for i, node_2 in enumerate(list_node_cycle):
                            
                            if i == len(list_node_cycle)-1:
                                neighbor_2 = list_node_cycle[0]               
                            else :
                                neighbor_2 = list_node_cycle[i+1] 
                            print(0.5, node_2, neighbor_2, cycle_turn)
                            print(0.6, list_node_cycle)
                            if neighbor_2 not in graph[node_2]:
                                proportion_node = 1.5
                            else:
                                proportion_node = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node_2)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()
                            count_different_antecedent_in_cycle = sum(1 for valeur in graph[node_2] if valeur in list_all_nodes_cycle) #count if the node has 2 or more diffrent antecedent in a cycle
                            print(0.75, neighbor_2, node_2, count_different_antecedent_in_cycle, proportion_node, proportion_min)
                            if proportion_node <= proportion_min and count_different_antecedent_in_cycle <=2 and len([x for x in graph[node_2]if x not in list_all_nodes_cycle])!=0:
                                proportion_min, name_proportion_min, name_start_cycle = proportion_node, node_2, neighbor_2
                        if name_proportion_min =='nothing':
                            print(1, 'breaking', proportion_min, list_node_cycle, list_all_nodes_cycle, list_cycle)
                            break
                        graph_cycle = [x for x in graph[name_proportion_min]if x not in list_all_nodes_cycle] 
                        capex_parent, opex_parent, cost_energy = 0, 0, 0
                        cycle_turn[0] = cycle_turn[0] + 1
                        print(node, cycle_turn, list_node_cycle)
                        print(1, graph_cycle, proportion_min, name_proportion_min)
                        
                        for neighbor_2 in  graph_cycle:
                            node_2 = name_proportion_min
                            proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node_2)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()
                            if neighbor_2 not in COST:
                                print(1.5, node_2, neighbor_2)
                                cost_iterator_calculator (graph, neighbor_2, COST, node_2, cost_breakdown, list_node_cycle, calculated, sankey_df, sankey_cost, list_cycle, cycle_turn, name_proportion_min)
                            cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 
                            if node in cost_breakdown.index :
                                capex_parent, opex_parent = cost_breakdown.loc[node_2]['C_inv'], opex_parent + cost_breakdown.loc[node_2]['C_maint'] + cost_breakdown.loc[node_2]['C_op']
                        COST[node_2] = (capex_parent, opex_parent, cost_energy)
                        

                # Compute the cost for the technologies and resources that are source of energy and not in a cycle
                if neighbor not in graph and neighbor not in calculated:
                    print(2, node, neighbor)
                    if neighbor.endswith('_IMP') : 
                        neighbor2 = neighbor[:-4]
                        capex_neighbor = cost_breakdown.loc[neighbor2]['C_inv'] 
                        opex_neighbor = cost_breakdown.loc[neighbor2]['C_maint'] + cost_breakdown.loc[neighbor2]['C_op']
                        COST[neighbor] = (0, 0, 0)
                        COST[node] = (capex_neighbor, opex_neighbor, 0) 
                        calculated.append(node)       
                    else:
                        capex_neighbor = cost_breakdown.loc[neighbor]['C_inv'] 
                        opex_neighbor = cost_breakdown.loc[neighbor]['C_maint'] + cost_breakdown.loc[neighbor]['C_op']
                        COST[neighbor] = (capex_neighbor, opex_neighbor, 0)
                    if neighbor not in list_all_nodes_cycle:
                        calculated.append(neighbor)
                        
                    #if neighbor == graph[node][-1]:
                        #cost_iterator_calculator (graph, node, COST, 0, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, sankey_cost, list_cycle, cycle_turn, name_proportion_min)
                #Base case to calculate all the preceding values
                else:
                    #############Case if neighbor in the cycle##############
                    if neighbor in list_all_nodes_cycle:
                        if name_proportion_min == node : 
                            if cycle_turn[0] >= 4:
                                for j in list_cycle[cycle_turn[1]] :
                                    calculated.append(j)
                            cycle_turn[0] = cycle_turn[0] + 1
                            print(3.5, name_proportion_min, cycle_turn)
                        if neighbor not in COST and cycle_turn[0] <= 4:
                            print(3, node, neighbor, cycle_turn[0], name_proportion_min)
                            cost_iterator_calculator (graph, neighbor, COST, node, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, sankey_cost, list_cycle, cycle_turn, name_proportion_min)
                        capex_parent, opex_parent, cost_energy = 0, 0, 0
                        
                        if all(elem in COST for elem in graph[node]):
                            for neighbor_2 in graph[node]:
                                #, COST)
                                proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()
                                cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 
                                print('A0', node, neighbor_2, proportion, cost_energy)
                            if node in cost_breakdown.index :
                                capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                            COST[node] = (capex_parent, opex_parent, cost_energy)
                            print('A1', node, capex_parent, opex_parent, cost_energy)
                            #print('kas', name_proportion_min)
                        


                    if neighbor not in list_all_nodes_cycle and neighbor not in calculated: 
                        #print(1, 'basic_iteration', node, neighbor)#, sankey_cost)
                        print(4, node, neighbor)
                        cost_iterator_calculator (graph, neighbor, COST, node, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, sankey_cost, list_cycle, cycle_turn, name_proportion_min)
                    #Compute the value of cost based on the value of the preceding 
                if all(elem in COST for elem in graph[node]):
                    if parent != None :
                        if neighbor not in list_all_nodes_cycle: #neighbor == graph[node][-1]
                            print(5, node, neighbor, COST)
                            capex_parent, opex_parent, cost_energy = 0, 0, 0
                            node2 = node
                            #node = parent
                            if all(elem in COST for elem in graph[node]):
                                for neighbor_2 in graph[node]:
                                    print(6, node, neighbor_2, neighbor)
                                    proportion = (sankey_df.loc[(sankey_df['source']==neighbor_2) & (sankey_df['target']==node)]['realValue'].values[0])/sankey_df.loc[(sankey_df['source']==neighbor_2)]['realValue'].sum()         
                                    cost_energy = cost_energy  + (COST[neighbor_2][1] + COST[neighbor_2][0] + COST[neighbor_2][2]) * proportion #transfère le coût sur l'usage suivant 

                                if node in cost_breakdown.index :
                                    capex_parent, opex_parent = cost_breakdown.loc[node]['C_inv'], opex_parent + cost_breakdown.loc[node]['C_maint'] + cost_breakdown.loc[node]['C_op']
                                COST[node] = (capex_parent, opex_parent, cost_energy)
                                if neighbor not in list_all_nodes_cycle:
                                    calculated.append(node)
                                if neighbor == graph[node][-1]:
                                    print(7, node, neighbor)
                                    cost_iterator_calculator (graph, node, COST, 0, cost_breakdown, list_all_nodes_cycle, calculated, sankey_df, sankey_cost, list_cycle, cycle_turn, name_proportion_min)
