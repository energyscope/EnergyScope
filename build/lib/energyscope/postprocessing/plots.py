import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from energyscope import elec_order_graphs, plotting_names, rename_storage_power, colors_elec


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

    fig, ax = hourly_plot(plotdata=plotdata, title=title, xticks=xticks, figsize=figsize, colors=colors_elec,
                          nbr_tds=tds[-1], show=True)

    return {'fig': fig, 'ax': ax, 'other_prods': other_prods, 'other_cons': other_cons}


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