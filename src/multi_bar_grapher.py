import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def __get_percentage_columns(df):
    """
    isolates percent columns
    """
    new_cols = ' '.join(list(df.columns.str.replace(' ', ''))).split()
    new_df = df.loc[:, [i for i in df if not i.replace(' ', '')]]
    new_df.columns = new_cols
    return new_df


def __percentage_to_int(df):
    """
    All elements must be a str
    removes all % from every element
    """
    new_df = df.copy()
    for i in new_df: 
        new_df[i] = new_df[i].str.replace('%', '').astype(int)
    return new_df


def graph_compare_percents_rows(table_list, name_list, x_label):
    """
    The tables must have a percent column for each column
    tables must have the same column header and indicies
    BUT it does allow for as many tables as you want!

    Parameters
    ----------
    table_list: List of tables that will be compared. Each row on from a table will be put on the same graph as like rows from other tables
    name_list: List of names for each table passed in. This will be the legend
    x_label: This will be the overall label for al the x-axes. Since they are categorical this is needed

    Returns
    -------
    axes of all the graphs
    """
    table_list_percentage = []
    for table in table_list:
        table_list_percentage.append(__percentage_to_int(__get_percentage_columns(table)).drop('Total'))
    return multi_bar_graph(table_list_percentage, name_list, x_label)


def graph_compare_percents_cols(table_list, name_list, x_label):
    """
    The tables must have a percent column for each column
    tables must have the same column header and indicies
    BUT it does allow for as many tables as you want!

    Parameters
    ----------
    table_list: List of tables that will be compared. Each column on from a table will be put on the same graph as like columns from other tables
    name_list: List of names for each table passed in. This will be the legend
    x_label: This will be the overall label for al the x-axes. Since they are categorical this is needed

    Returns
    -------
    Axes of all the graphs
    """
    table_list_percentage = []
    for table in table_list:
        table_list_percentage.append(__percentage_to_int(__get_percentage_columns(table)).drop('Total').transpose())
    return multi_bar_graph(table_list_percentage, name_list, x_label)


def multi_bar_graph(table_list, name_list, x_label):
    """
    Tables must have the same column header and indicies

    Parameters
    ----------
    table_list: List of tables that will be compared. Each row on from a table will be put on the same graph as like row from other tables
    name_list: List of names for each table passed in. This will be the legend
    x_label: This will be the overall label for al the x-axes. Since they are categorical this is needed

    Returns
    -------
    Axes of all the graphs
    """
    plt.style.use('seaborn')
    rows = len(table_list[0])
    fig, axes = plt.subplots(nrows = rows, ncols = 1, figsize = (15, rows * 10))
    x = np.arange(len(table_list[0].columns))
    bar_count = (len(table_list) * len(table_list[0].columns))
    width = 3 / max(bar_count, 8)
    counter = 0
    for table in table_list:
        row_num  = 0
        for index, row in table.iterrows():
            ax = axes[row_num]
            ax.bar(x + counter * width,
                   list(row),
                   width = width,
                   #color = ['b','g','r','y','k'][counter % 5],
                   align = 'center',
                   label = name_list[counter], edgecolor = 'black', linewidth = 1)
            ax.set_title(index, fontsize = 50)
            ax.set_ylabel('Percentage', fontsize = 35)
            ax.set_xlabel(x_label, fontsize = 35)
            ax.set_ylim(0, 115)
            ax.set_yticklabels([str(i * 20) for i in range(6)], fontsize = 30)
            ax.set_xticklabels(tuple(table.columns), fontsize = 30)
            ax.set_xticks(x + width / 2)
            ax.legend(loc = 'upper left', fontsize = 35)
            row_num += 1
        counter += 1
    fig.tight_layout()
    return fig, axes

def display_one_axis(fig, axes, index, title = '', save_name = ''):
    """
    If save name empty the graph will be displayed. If named it will save the image
    """
    for i in range(len(axes)):
        if i != index:
            axes[i].remove()
    x = axes[index]
    if title: x.set_title(title, fontsize  = 40)
    if save_name:
        x.remove()
        fig2 = plt.figure(figsize = (15, 13))
        x.figure=fig2
        fig2.axes.append(x)
        fig2.add_axes(x)
        
        dummy = fig2.add_subplot(111)
        x.set_position(dummy.get_position())
        dummy.remove()
        fig2.subplots_adjust()

        fig2.savefig(save_name)
    else: plt.show()
    plt.ioff()
    return fig