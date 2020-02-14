from data_acquisition import *
from data_formating import *
from make_2016_tables import *
from multi_bar_grapher import *

import pandas as pd
import matplotlib.pyplot as plt


def make_all_figures():
    """
    df must be all youth and unweighted
    """
    total_youth_unweighted = get_youth_by_puma(start_puma = 11610, end_puma = 11615, dbname = 'opportunity_youth')
    oy_by_puma = get_oy_by_puma(start_puma = 11610, end_puma = 11615, dbname = 'opportunity_youth')
    
    four_race, age, education, all_races = page_2_tables(total_youth_unweighted, save = True) # all breakups as df
    four_race_2016, age_2016, edu_2016 = get_2016_tables(save = True)

    plt.style.use('seaborn')
    
    fig, axes = graph_compare_percents_cols([age_2016, age], ['2016', '2017'], 'OY Status')
    display_one_axis(fig, axes, 3,
                     title = 'Change in Opportunity Youth From 2016 to 2017',
                     save_name = '../reports/figures/oy_change_2016_2017.png')

    fig, axes = graph_compare_percents_cols([edu_2016, education], ['2016', '2017'], 'Education Status')
    display_one_axis(fig, axes, 3,
                     title = 'Change in Education Attainment From 2016 to 2017',
                     save_name = '../reports/figures/education_change_2016_2017.png')

    fig, axes = graph_compare_percents_rows([four_race_2016, four_race], ['2016', '2017'], 'Race')
    fig.savefig("../reports/figures/oy_by_race_2016_2017.png")
    plt.close()
    None;