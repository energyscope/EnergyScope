############ run_energyscope.py ################
    print_h_layer = False
    if print_h_layer == True :
        h2_layer_plot = es.plot_layer_louis(outputs['layer_H2'])
        h2_layer_plot.show()
        ammonia_layer_plot = es.plot_layer_louis(outputs['layer_AMMONIA'])
        ammonia_layer_plot.show()


    print_h_layer_year = False
    if print_h_layer_year == True :
        #h2_layer_plot = es.plot_layer_year_energy_stored(outputs['layer2_ELECTRICITY'], outputs['energy_stored'])
        #h2_layer_plot.show()
        outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=['layer2_ELECTRICITY','layer2_HEAT_LOW_T_DECEN','layer2_HEAT_LOW_T_DHN', 'layer2_HEAT_HIGH_T', 'layer2_AMMONIA', 'layer2_H2'])
        ammonia_layer_plot = es.plot_layer_year(outputs['layer2_ELECTRICITY'])
        ammonia_layer_plot.show()
        heat_layer_plot = es.plot_layer_year(outputs['layer2_HEAT_LOW_T_DECEN'])
        heat_layer_plot.show()
        heat_dhn_layer_plot = es.plot_layer_year(outputs['layer2_HEAT_LOW_T_DHN'])
        heat_dhn_layer_plot.show()

############## plots.py #############################

def hourly_plot(plotdata: pd.DataFrame, title='', xticks=None, figsize=(17,7), colors=None, nbr_tds=None, show=True):
    """Cleans and plot the hourly data
    Drops the null columns and plots the hourly data in plotdata dataframe as stacked bars

    Parameters
    ----------
    plotdata: pandas.DataFrame
    Hourly dataframe with producing (>0) and consumming (<0) technologies (columns) at each hour (rows)

    xticks: numpy.ndarray
    Array of xticks for the plot

    figsize: tuple
    Figure size for the plot

    nbr_tds: float
    Number of Typical Days if typical days are plotted. If not, leave to default value (None)

    show: Boolean
    Show or not the graph

    Returns
    -------
     fig: matplotlib.figure.Figure
    Figure object of the plot

    ax: matplotlib.axes._subplots.AxesSubplot
    Ax object of the plot
    """

    # select columns with non-null prod or cons
    plotdata = plotdata.loc[:, plotdata.sum().abs() > 1.0]
    # default xticks
    if xticks is None:
        xticks = np.arange(0, plotdata.shape[0]+1, 8)

    fig, ax = plt.subplots(figsize=figsize)
    if colors is None:
        plotdata.plot(kind='bar', position=0, width=1.0, stacked=True, ax=ax, legend=True, xticks=xticks,
                      colormap='tab20')
    else:
        plotdata.plot(kind='bar', position=0, width=1.0, stacked=True, ax=ax, legend=True, xticks=xticks,
                      color=colors)
    ax.set_title(title)
    ax.legend(loc='center right', bbox_to_anchor=(1.5, 0.5))
    ax.set_xlabel('Hour')
    ax.set_ylabel('Power [GW]')
    if nbr_tds is not None:
        for i in range(nbr_tds):
            ax.axvline(x=i * 24, color='dimgray', linestyle='--')
    plt.subplots_adjust(right=0.75)
    fig.tight_layout()
    fig.show()
    return fig, ax


def plot_layer_elec_td(layer_elec: pd.DataFrame, title='Layer electricity', tds = np.arange(1,13), reorder_elec=None, figsize=(13,7), xticks=None):
    """Cleans and plots the layer electricity
    Select the rows linked with specific TD, reorder the columns for the plot,
    merge the EVs columns with the batteries output, drop the null columns and plots

    Parameters
    ----------
    layer_elec: pandas.DataFrame
    Multiindex dataframe of hourly production (>0) and consumption (<0) of each technology (columns) for each hour of each typical day (rows)

    tds: numpy.ndarray
    Array containing the numbers of the TDs to plot

    reorder_elec: list
    Ordered list with all the columns names of layer_elec ordered in the way to be plotted
    (e.g. 'END_USES' should be the first consummer to be the one the closest to the x acis)

    figsize: tuple
    Size of the figure

    Returns
    -------
    Dict with:
        fig: matplotlib.figure.Figure
        Figure object of the plot

        ax: matplotlib.axes._subplots.AxesSubplot
        Ax object of the plot

        other_prods: list
        List of producing technologies with max<0.02*biggest producer (or consummer)

        other_cons: list
        List of cons technologies with max(abs)<0.02*biggest producer  (or consummer)
    """
    #TODO
    # add datetime
    # speed up
    # split into 2 parts -> clean_elec and plot_td
    plotdata = layer_elec.copy()
    plotdata2 = layer_elec.copy()
    # select specified TDs
    plotdata = plotdata.loc[(tds, slice(None)),:]

    # default reordering
    if reorder_elec is None:
        reorder_elec = elec_order_graphs
    # reorder the columns for the plot
    plotdata = plotdata[reorder_elec]
    # Grouping some tech for plot readability
        # Public mobility
    plotdata.loc[:,'TRAMWAY_TROLLEY'] = plotdata.loc[:,['TRAMWAY_TROLLEY', 'TRAIN_PUB']].sum(axis=1)
    plotdata.rename(columns={'TRAMWAY_TROLLEY': 'Public mobility'}, inplace=True)
    plotdata.drop(columns=['TRAIN_PUB'], inplace=True)
        # Freight mobility
    plotdata.loc[:,'TRAIN_FREIGHT'] = plotdata.loc[:,['TRAIN_FREIGHT', 'TRUCK_ELEC']].sum(axis=1)
    plotdata.rename(columns={'TRAIN_FREIGHT': 'Freight'}, inplace=True)
    plotdata.drop(columns=['TRUCK_ELEC'], inplace=True)

        # sum CAR_BEV and BEV_BATT_Pout into 1 column for easier reading of the impact of BEV on the grid
    plotdata.loc[:, 'BEV_BATT_Pout'] = plotdata.loc[:, 'BEV_BATT_Pout'] + plotdata.loc[:, 'CAR_BEV']
    plotdata.drop(columns=['CAR_BEV'], inplace=True)
        # same for PHEV
    plotdata.loc[:, 'PHEV_BATT_Pout'] = plotdata.loc[:, 'PHEV_BATT_Pout'] + plotdata.loc[:, 'CAR_PHEV']
    plotdata.drop(columns=['CAR_PHEV'], inplace=True)
        # treshold to group other tech
    treshold = 0.02*plotdata.abs().max().max()
        # Other prod. -> the ones with max<treshold
    other_prods = list(plotdata.loc[:,(plotdata.max()>0.0) & (plotdata.max()<treshold)].columns)
    if other_prods:
        plotdata.loc[:,other_prods[0]] = plotdata.loc[:,other_prods].sum(axis=1)
        plotdata.rename(columns={other_prods[0]: 'Other prod.'}, inplace=True)
        plotdata.drop(columns=other_prods[1:], inplace=True)
        # Other cons. -> the ones with abs(max)<treshold
    other_cons = list(plotdata.loc[:,(plotdata.min()<0.0) & (plotdata.min()>-treshold)].columns)
    if other_cons:
        plotdata.loc[:,other_cons[0]] = plotdata.loc[:,other_cons].sum(axis=1)
        plotdata.rename(columns={other_cons[0]: 'Other cons.'}, inplace=True)
        plotdata.drop(columns=other_cons[1:], inplace=True)

    # Change names before plotting
    plotdata.rename(columns=plotting_names, inplace=True)
    plotdata.rename(columns=lambda x: rename_storage_power(x) if x.endswith('Pin') or x.endswith('Pout') else x, inplace=True)
    print(plotdata)
    fig, ax = hourly_plot(plotdata=plotdata, title=title, xticks=xticks, figsize=figsize, colors=None,#colors=colors_elec,
                          nbr_tds=tds[-1], show=True)
    plotdata2 = plotdata2.reset_index()
    plotdata2[' Time'] = plotdata2[' Time'] + 24 * plotdata2['Td ']
    plotdata2 = plotdata2.fillna(0)
    print(plotdata, plotdata2)
    all_names = ['ELECTRICITY', 'GASOLINE', 'DIESEL', 'BIOETHANOL', 'BIODIESEL', 'LFO', 'GAS', 'JETFUEL_RE', 'JETFUEL', 'GAS_RE', 'WOOD', 'WET_BIOMASS', 'COAL', 'URANIUM', 'WASTE', 'H2', 'H2_RE', 'AMMONIA', 'METHANOL', 'AMMONIA_RE', 'METHANOL_RE', 'ELEC_EXPORT', 'CO2_EMISSIONS', 'RES_WIND', 'RES_SOLAR', 'RES_HYDRO', 'RES_GEO', 'CO2_ATMOSPHERE', 'CO2_CENTRALISED', 'CO2_CAPTURED', 'CO2_DECENTRALISED', 'OTHER_GHG', 'NUCLEAR', 'CCGT', 'CCGT_AMMONIA', 'COAL_US', 'COAL_IGCC', 'PV', 'WIND_ONSHORE', 'WIND_OFFSHORE', 'HYDRO_RIVER', 'GEOTHERMAL', 'IND_COGEN_GAS', 'IND_COGEN_WOOD', 'IND_COGEN_WASTE', 'IND_BOILER_GAS', 'IND_BOILER_WOOD', 'IND_BOILER_OIL', 'IND_BOILER_COAL', 'IND_BOILER_WASTE', 'IND_DIRECT_ELEC', 'DHN_HP_ELEC', 'DHN_COGEN_GAS', 'DHN_COGEN_WOOD', 'DHN_COGEN_WASTE', 'DHN_COGEN_WET_BIOMASS', 'DHN_COGEN_BIO_HYDROLYSIS', 'DHN_BOILER_GAS', 'DHN_BOILER_WOOD', 'DHN_BOILER_OIL', 'DHN_DEEP_GEO', 'DHN_SOLAR', 'DEC_HP_ELEC', 'DEC_THHP_GAS', 'DEC_COGEN_GAS', 'DEC_COGEN_OIL', 'DEC_ADVCOGEN_GAS', 'DEC_ADVCOGEN_H2', 'DEC_BOILER_GAS', 'DEC_BOILER_WOOD', 'DEC_BOILER_OIL', 'DEC_SOLAR', 'DEC_DIRECT_ELEC', 'TRAMWAY_TROLLEY', 'BUS_COACH_DIESEL', 'BUS_COACH_HYDIESEL', 'BUS_COACH_CNG_STOICH', 'BUS_COACH_FC_HYBRIDH2', 'TRAIN_PUB', 'CAR_GASOLINE', 'CAR_DIESEL', 'CAR_NG', 'CAR_METHANOL', 'CAR_HEV', 'CAR_PHEV', 'CAR_BEV', 'CAR_FUEL_CELL', 'PLANE', 'BOAT_FREIGHT_DIESEL', 'BOAT_FREIGHT_NG', 'BOAT_FREIGHT_METHANOL', 'TRAIN_FREIGHT', 'TRUCK_DIESEL', 'TRUCK_METHANOL', 'TRUCK_FUEL_CELL', 'TRUCK_ELEC', 'TRUCK_NG', 'HABER_BOSCH', 'SYN_METHANOLATION', 'METHANE_TO_METHANOL', 'BIOMASS_TO_METHANOL', 'OIL_TO_HVC', 'GAS_TO_HVC', 'BIOMASS_TO_HVC', 'METHANOL_TO_HVC', 'EFFICIENCY', 'DHN', 'GRID', 'H2_ELECTROLYSIS', 'SMR', 'H2_BIOMASS', 'GASIFICATION_SNG', 'SYN_METHANATION', 'BIOMETHANATION', 'BIO_HYDROLYSIS', 'PYROLYSIS_TO_LFO', 'PYROLYSIS_TO_FUELS', 'ATM_CCS', 'INDUSTRY_CCS', 'AMMONIA_TO_H2', 'WOOD_TO_JETFUELS', 'CO2_TO_JETFUELS', 'DAC_HT', 'DAC_LT', 'WOOD_GROWTH', 'SEQUESTRATION', 'GHG_EMISSIONS', 'PHS_Pin', 'PHS_Pout', 'BATT_LI_Pin', 'BATT_LI_Pout', 'BEV_BATT_Pin', 'BEV_BATT_Pout', 'PHEV_BATT_Pin', 'PHEV_BATT_Pout', 'TS_DEC_DIRECT_ELEC_Pin', 'TS_DEC_DIRECT_ELEC_Pout', 'TS_DEC_HP_ELEC_Pin', 'TS_DEC_HP_ELEC_Pout', 'TS_DEC_THHP_GAS_Pin', 'TS_DEC_THHP_GAS_Pout', 'TS_DEC_COGEN_GAS_Pin', 'TS_DEC_COGEN_GAS_Pout', 'TS_DEC_COGEN_OIL_Pin', 'TS_DEC_COGEN_OIL_Pout', 'TS_DEC_ADVCOGEN_GAS_Pin', 'TS_DEC_ADVCOGEN_GAS_Pout', 'TS_DEC_ADVCOGEN_H2_Pin', 'TS_DEC_ADVCOGEN_H2_Pout', 'TS_DEC_BOILER_GAS_Pin', 'TS_DEC_BOILER_GAS_Pout', 'TS_DEC_BOILER_WOOD_Pin', 'TS_DEC_BOILER_WOOD_Pout', 'TS_DEC_BOILER_OIL_Pin', 'TS_DEC_BOILER_OIL_Pout', 'TS_DHN_DAILY_Pin', 'TS_DHN_DAILY_Pout', 'TS_DHN_SEASONAL_Pin', 'TS_DHN_SEASONAL_Pout', 'TS_HIGH_TEMP_Pin', 'TS_HIGH_TEMP_Pout', 'GAS_STORAGE_Pin', 'GAS_STORAGE_Pout', 'H2_STORAGE_Pin', 'H2_STORAGE_Pout', 'DIESEL_STORAGE_Pin', 'DIESEL_STORAGE_Pout', 'GASOLINE_STORAGE_Pin', 'GASOLINE_STORAGE_Pout', 'LFO_STORAGE_Pin', 'LFO_STORAGE_Pout', 'AMMONIA_STORAGE_Pin', 'AMMONIA_STORAGE_Pout', 'METHANOL_STORAGE_Pin', 'METHANOL_STORAGE_Pout', 'CO2_STORAGE_Pin', 'CO2_STORAGE_Pout', 'JETFUEL_STORAGE_Pin', 'JETFUEL_STORAGE_Pout', 'END_USE']
    fig2 = px.bar(plotdata2, x=' Time' , y=all_names)#['ELECTRICITY', 'GASOLINE', 'DIESEL', 'BIOETHANOL', 'BIODIESEL', 'LFO', 'GAS', 'JETFUEL_RE', 'JETFUEL', 'GAS_RE', 'WOOD', 'WET_BIOMASS', 'COAL', 'URANIUM', 'WASTE', 'H2', 'H2_RE', 'AMMONIA', 'METHANOL', 'AMMONIA_RE', 'METHANOL_RE', 'ELEC_EXPORT', 'CO2_EMISSIONS', 'RES_WIND', 'RES_SOLAR', 'RES_HYDRO', 'RES_GEO', 'CO2_ATM', 'CO2_INDUSTRY', 'CO2_CAPTURED', 'NUCLEAR', 'CCGT', 'CCGT_AMMONIA', 'COAL_US', 'COAL_IGCC', 'PV', 'WIND_ONSHORE', 'WIND_OFFSHORE', 'HYDRO_RIVER', 'GEOTHERMAL', 'IND_COGEN_GAS', 'IND_COGEN_WOOD', 'IND_COGEN_WASTE', 'IND_BOILER_GAS', 'IND_BOILER_WOOD', 'IND_BOILER_OIL', 'IND_BOILER_COAL', 'IND_BOILER_WASTE', 'IND_DIRECT_ELEC', 'DHN_HP_ELEC', 'DHN_COGEN_GAS', 'DHN_COGEN_WOOD', 'DHN_COGEN_WASTE', 'DHN_COGEN_WET_BIOMASS', 'DHN_COGEN_BIO_HYDROLYSIS', 'DHN_BOILER_GAS', 'DHN_BOILER_WOOD', 'DHN_BOILER_OIL', 'DHN_DEEP_GEO', 'DHN_SOLAR', 'DEC_HP_ELEC', 'DEC_THHP_GAS', 'DEC_COGEN_GAS', 'DEC_COGEN_OIL', 'DEC_ADVCOGEN_GAS', 'DEC_ADVCOGEN_H2', 'DEC_BOILER_GAS', 'DEC_BOILER_WOOD', 'DEC_BOILER_OIL', 'DEC_SOLAR', 'DEC_DIRECT_ELEC', 'TRAMWAY_TROLLEY', 'BUS_COACH_DIESEL', 'BUS_COACH_HYDIESEL', 'BUS_COACH_CNG_STOICH', 'BUS_COACH_FC_HYBRIDH2', 'TRAIN_PUB', 'CAR_GASOLINE', 'CAR_DIESEL', 'CAR_NG', 'CAR_METHANOL', 'CAR_HEV', 'CAR_PHEV', 'CAR_BEV', 'CAR_FUEL_CELL', 'PLANE', 'BOAT_FREIGHT_DIESEL', 'BOAT_FREIGHT_NG', 'BOAT_FREIGHT_METHANOL', 'TRAIN_FREIGHT', 'TRUCK_DIESEL', 'TRUCK_METHANOL', 'TRUCK_FUEL_CELL', 'TRUCK_ELEC', 'TRUCK_NG', 'HABER_BOSCH', 'SYN_METHANOLATION', 'METHANE_TO_METHANOL', 'BIOMASS_TO_METHANOL', 'OIL_TO_HVC', 'GAS_TO_HVC', 'BIOMASS_TO_HVC', 'METHANOL_TO_HVC', 'EFFICIENCY', 'DHN', 'GRID', 'H2_ELECTROLYSIS', 'SMR', 'H2_BIOMASS', 'GASIFICATION_SNG', 'SYN_METHANATION', 'BIOMETHANATION', 'BIO_HYDROLYSIS', 'PYROLYSIS_TO_LFO', 'PYROLYSIS_TO_FUELS', 'ATM_CCS', 'INDUSTRY_CCS', 'AMMONIA_TO_H2', 'PHS_Pin', 'PHS_Pout', 'BATT_LI_Pin', 'BATT_LI_Pout', 'BEV_BATT_Pin', 'BEV_BATT_Pout', 'PHEV_BATT_Pin', 'PHEV_BATT_Pout', 'TS_DEC_DIRECT_ELEC_Pin', 'TS_DEC_DIRECT_ELEC_Pout', 'TS_DEC_HP_ELEC_Pin', 'TS_DEC_HP_ELEC_Pout', 'TS_DEC_THHP_GAS_Pin', 'TS_DEC_THHP_GAS_Pout', 'TS_DEC_COGEN_GAS_Pin', 'TS_DEC_COGEN_GAS_Pout', 'TS_DEC_COGEN_OIL_Pin', 'TS_DEC_COGEN_OIL_Pout', 'TS_DEC_ADVCOGEN_GAS_Pin', 'TS_DEC_ADVCOGEN_GAS_Pout', 'TS_DEC_ADVCOGEN_H2_Pin', 'TS_DEC_ADVCOGEN_H2_Pout', 'TS_DEC_BOILER_GAS_Pin', 'TS_DEC_BOILER_GAS_Pout', 'TS_DEC_BOILER_WOOD_Pin', 'TS_DEC_BOILER_WOOD_Pout', 'TS_DEC_BOILER_OIL_Pin', 'TS_DEC_BOILER_OIL_Pout', 'TS_DHN_DAILY_Pin', 'TS_DHN_DAILY_Pout', 'TS_DHN_SEASONAL_Pin', 'TS_DHN_SEASONAL_Pout', 'TS_HIGH_TEMP_Pin', 'TS_HIGH_TEMP_Pout', 'GAS_STORAGE_Pin', 'GAS_STORAGE_Pout', 'H2_STORAGE_Pin', 'H2_STORAGE_Pout', 'DIESEL_STORAGE_Pin', 'DIESEL_STORAGE_Pout', 'GASOLINE_STORAGE_Pin', 'GASOLINE_STORAGE_Pout', 'LFO_STORAGE_Pin', 'LFO_STORAGE_Pout', 'AMMONIA_STORAGE_Pin', 'AMMONIA_STORAGE_Pout', 'METHANOL_STORAGE_Pin', 'METHANOL_STORAGE_Pout', 'CO2_STORAGE_Pin', 'CO2_STORAGE_Pout', 'JETFUEL_STORAGE_Pin', 'JETFUEL_STORAGE_Pout', 'END_USE'])
    #fig2 = px.bar(plotdata, x=' Time' , y=['Ind. cogen. gas', 'Ind. cogen. wood', 'Ind. cogen. waste', 'DHN cogen. gas', 'DHN cogen. wood', 'DHN cogen. waste', 'DHN cogen. wet biomass', 'DHN cogen. bio hydrolysis', 'Dec. cogen. gas', 'Dec. cogen. oil', 'Dec. advcogen. gas', 'Dec. advcogen. h2', 'CCGT', 'Other prod.', 'Wind onshore', 'Wind offshore', 'Hydro river', 'Biomass to methanol', 'Pyrolysis to oil', 'Pyrolysis to fuels', 'Lithium batt. Pout', 'Electric vehicle batt. Pout', 'Plug-in hybrid batt. Pout', 'End use', 'Public mobility', 'Other cons.', 'Synthetic methanolation', 'Gas to HVC', 'Atmospheric CCS', 'Industry CCS', 'DHN HP elec.', 'Dec. HP elec.', 'Ind. direct elec.', 'H2 elec.trolysis', 'Lithium batt. Pin', 'Electric vehicle batt. Pin', 'Plug-in hybrid batt. Pin', 'Elec export'])
    return {'fig': fig, 'ax': ax, 'other_prods': other_prods, 'other_cons': other_cons, 'fig2' : fig2}


def plot_barh(plotdata: pd.DataFrame, treshold=0.15, title='', x_label='', y_label='', xlim=None, legend=None, figsize=(13,7), show_plot=True):
    """Cleans and plot the plotdata into a barh ordered plot
    Drops the rows with maximum value below the treshold in plotdata, sort them according to the last column
    and plots them in a barh plot

    Parameters
    ----------
    plotdata: pandas.DataFrame
    Dataframe to plot

    treshold: float (default=0.15)
    Treshold to determine rows to keep or not

    x_label: str
    Label of the x axis for the plot

    y_label: str
    Label of the y axis for the plot

    xlim: tuple
    xlim for the plot

    legend: boolean
    Show or not the legend for the plot

    figsize: tuple
    Figure size for the plot

    show_plot: Boolean
    Show or not the graph

    Returns
    -------
     fig: matplotlib.figure.Figure
    Figure object of the plot

    ax: matplotlib.axes._subplots.AxesSubplot
    Ax object of the plot

    """

    # plotting elec assets
    fig, ax = plt.subplots(figsize=figsize)
    plotdata = plotdata.loc[plotdata.max(axis=1) > treshold, :].sort_values(by=plotdata.columns[-1])
    plotdata.rename(index=plotting_names).plot(kind='barh', width=0.8, colormap='tab20', ax=ax)

    # legend options
    if legend is None:
        ax.get_legend().remove()
    else:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], legend['labels'], loc='lower right', frameon=False)
    # add title
    ax.set_title(title)
    # adding label and lim to x axis
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if xlim is not None:
        ax.set_xlim(xlim)

    fig.tight_layout()
    if show_plot:
        fig.show()

    return fig,ax


def plot_layer_year(layer_elec: pd.DataFrame, title='Layer electricity', tds = np.arange(1,13), reorder_elec=None, figsize=(13,7), xticks=None):
    """
    """
    plotdata = layer_elec.copy()
    plotdata = plotdata.fillna(0)
    # Vérifier si chaque colonne ne contient que des zéros
    colonnes_zeros = plotdata.columns[plotdata.eq(0).all()]
    print(plotdata)
# Supprimer les colonnes ne contenant que des zéros
    plotdata = plotdata.drop(colonnes_zeros, axis=1)
    names_column = plotdata.columns
    plotdata = plotdata.reset_index()
    #plotdata[' Time'] = plotdata[' Time'] + 24 * plotdata['Td ']
    column_storage_out = plotdata.columns[plotdata.columns.str.endswith('_Pout')]
    column_storage_in = plotdata.columns[plotdata.columns.str.endswith('_Pin')]
    prefix = column_storage_out.str.split('_Pout').str[0].tolist()

    dfin = pd.DataFrame()
    dfin[prefix] = plotdata[column_storage_in]
    dfout = pd.DataFrame()
    dfout[prefix] = plotdata[column_storage_out]
    plotdata[prefix] = dfin + dfout

    names_column = names_column.difference(column_storage_in).difference(column_storage_out).insert(0, prefix).difference(['ELECTRICITY'])
    data2 = pd.DataFrame()   
    for j in names_column:
        sum = []
        for i in range(0, 8760, 24):
            sum.append(plotdata[j][i:i+24].sum())
        data2[j] = sum
    data2['Periods'] = [i for i in range(0, 365)]
    techno_color = pd.read_excel(os.path.join(os.getcwd(), 'energyscope', 'postprocessing',"techno_color.xlsx"),   index_col=False)
    COLOR_node = [techno_color[techno_color['Name']==i.replace(' ', '')]['Color_vector'].item() for i in names_column]
    print(data2, data2['Periods'], data2[names_column])
    fig = px.bar(data2, x='Periods' ,y=names_column)#, color= COLOR_node)
    return(fig)

def plot_layer_year_energy_stored(layer_elec: pd.DataFrame, energy_stored, title='Layer electricity', tds = np.arange(1,13), reorder_elec=None, figsize=(13,7), xticks=None):
    """
    """

    #Traitement de la layer
    plotdata = layer_elec.copy()
    plotdata = plotdata.fillna(0)
    # Vérifier si chaque colonne ne contient que des zéros
    colonnes_zeros = plotdata.columns[plotdata.eq(0).all()]

# Supprimer les colonnes ne contenant que des zéros
    plotdata = plotdata.drop(colonnes_zeros, axis=1)
    names_column = plotdata.columns
    plotdata = plotdata.reset_index()
    plotdata[' Time'] = plotdata[' Time'] + 24 * plotdata['Td ']
    column_storage_out = plotdata.columns[plotdata.columns.str.endswith('_Pout')]
    column_storage_in = plotdata.columns[plotdata.columns.str.endswith('_Pin')]
    prefix = column_storage_out.str.split('_Pout').str[0].tolist()

    dfin = pd.DataFrame()
    dfin[prefix] = plotdata[column_storage_in]
    dfout = pd.DataFrame()
    dfout[prefix] = plotdata[column_storage_out]
    plotdata[prefix] = dfin + dfout

    names_column = names_column.difference(column_storage_in).difference(column_storage_out).insert(0, prefix)
    data2 = pd.DataFrame()   
    for j in names_column:
        sum = []
        for i in range(0, 8760, 24):
            sum.append(plotdata[j][i:i+24].sum())
        data2[j] = sum
    data2['Periods'] = [i for i in range(0, 365)]

    #############Energy Stored##############


    energy_stored = energy_stored.fillna(0)
    # Vérifier si chaque colonne ne contient que des zéros
    colonnes_zeros = energy_stored.columns[energy_stored.eq(0).all()]

# Supprimer les colonnes ne contenant que des zéros
    energy_stored = energy_stored.drop(colonnes_zeros, axis=1)
    names_column2 = energy_stored.columns.difference(['Periods'])
    energy_stored = energy_stored.reset_index()
    energy_stored= energy_stored[::24]
    energy_stored['Periods']= [i for i in range(0, 365)]#(energy_stored['Periods']-1)/24
    energy_stored['Total Energy'] = energy_stored[names_column2].sum(axis=1)
    print(energy_stored)
    print(data2)
    print(names_column, names_column2)
    fig = go.Figure()
    for j in names_column:
        fig.add_trace(go.Bar( x=data2['Periods'] ,y=data2[j], name=j,  yaxis='y1'))

    #fig.add_trace(go.Scatter( x=energy_stored['Periods'] ,y=energy_stored['Total Energy'], name='Total Energy',  yaxis='y2'))
    fig.update_layout(barmode="stack",yaxis=dict(title='Y1'))
    fig.update_layout(barmode="stack",yaxis2=dict(title='Y2', side='right'))
    return(fig)