import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir, os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
    
import pandas as pd

from src.data_acquisition import *


def make_table_with_percentage(dct): # TODO Comment on this
    """
    Makes a table with percentage with the top row being the total of entries bellow
    """
    df = __get_as_df(dct)
    return __add_percentage_column(df)


def make_table_without_percentage(dct):
    """
    Makes a table from a dictionary of dictionarys
    """
    return __get_as_df(dct)


def __get_as_df(dct):
    """
    Helper for make_table_with_percentage
    """
    df = pd.DataFrame(dct)
    df.columns = df.columns.str.title()
    cols = list(df.columns)
    if 'Total' in cols:
        cols.remove('Total')
        df = df[cols + ['Total']]
    df.index = df.index.str.title()
    return df


def __add_percentage_column(df):
    """
    Helper for make_table_with_percentage
    Adds a new column with the precentage preceding the each column
    Column names for the new columns are spaces
    """
    new_frame = df.copy()
    for index, column in enumerate(new_frame):
        new_frame[column] = new_frame[column].astype(int)
        new_frame.insert(index * 2, ' ' * index, (df[column] / df[column]['Total'] * 100).round().astype(int).astype(str) + '%')
    return new_frame


def __add_percentage_integrated(df):
    """
    Helper for make_table_with_percentage
    Addds the percentage to the columns
    """
    new_frame = df.copy()
    for column in new_frame:
        new_column = [str(int(round(100 * element / new_frame[column][0])))
                      + '% ' + str(int(element)) for element in new_frame[column]]
        new_frame[column] = new_column
    return new_frame


def page_2_dicts(df): # TODO Better comments!
    # Makes dictionarys for all the tables on page 2
    four_races     = breakdown_by_split(df, split_by4_race,    oy_breakdown)
    age            = breakdown_by_split(df, split_by_age,      oy_breakdown)
    edu_and_age    = breakdown_by_split(df, split_by_age,      education_breakdown, filter_oy)
    oy_by_all_race = breakdown_by_split(df, split_by_all_race, oy_breakdown)
    
    pop_by_race = {i : oy_by_all_race[i]['total'] for i in oy_by_all_race}  #  
    oy_by_race = {i : oy_by_all_race[i]['oy'] for i in oy_by_all_race}      # This transposes the dictionary
    race = {'Population Total' : pop_by_race, 'OY Total' : oy_by_race}      # 

    return four_races, age, edu_and_age, race


def page_2_tables(df, save = False): # TODO COMMENT MORE
    """
    df: dataframe of region and age range
    returns 4 dataframes that match the table on page 2 of the reference 2016 document
    """
    four_race_dict, age_dict, edu_dict, races_dict = page_2_dicts(df)

    four_race = make_table_with_percentage(four_race_dict)
    age       = make_table_with_percentage(age_dict)
    education = make_table_with_percentage(edu_dict)
    all_races = __fix_all_race_table(pd.DataFrame(races_dict))

    if save:
        save_tables({'2017_four_race' : four_race, '2017_age' : age, '2017_education' : education, '2017_all_races' : all_races}, '../../reports/figures/')
    
    return four_race, age, education, all_races


def __fix_all_race_table(all_races): # TODO COMMENT!!!!
    """
    Helper method to add percentages to the all race table
    """
    new_col = ['100% ' + str(int(all_races['Population Total'][0]))]
    for index, element in enumerate(all_races['Population Total'][1:]):
        ratio = all_races['OY Total'][index + 1] / element
        new_col.append(str(int(round(100 * ratio))) + '% ' + str(int(element)))
    all_races['Population Total'] = new_col

    all_races['OY Total'] = [str(int(round(100 * element / all_races['OY Total'][0]))) + '% ' + str(int(element)) for element in all_races['OY Total']]
    all_races.index = all_races.index.str.title()
    return all_races

def save_tables(dct, path):
    """
    Saves tables into a path with a given title.
    keys are the title and values are the table
    """
    for name, table in dct.items():
        table.to_csv(f'{path}{name}.csv')