import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir, os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)

import pandas as pd
from tabula import read_pdf

from src.data_formating import *


def get_2016_tables(save = False):
    """
    Gets the tables from 2016 pdf and formats them properly
    """
    df = __get_frame_from_pdf()
    df.columns = ['16-18','19-21','22-24','Total']
    age_2016 = make_table_with_percentage(__remove_commas(__get_age_table(df)))
    edu_2016 = make_table_with_percentage(__remove_commas(__get_edu_table(df)))
    four_race = make_table_with_percentage(__remove_commas(__four_races()))
    
    if save:
        save_tables({'2016_four_race' : four_race, '2016_age' : age_2016, '2016_education' : edu_2016}, '../../reports/figures/')
        
    return four_race, age_2016, edu_2016


def __remove_commas(df):
    """
    This will remove the commas from the tables from the pdf
    """
    new_df = df.copy()
    for col in new_df:
        new_df[col] = new_df[col].str.replace(',', '').astype(int)
    return new_df


def __get_frame_from_pdf():
    """
    Gets the dataframe of the tables from 2016 from the pdf
    """
    #module_path = os.path.abspath(os.path.join(os.pardir, os.pardir))
    #if module_path not in sys.path: sys.path.append(module_path)
    return read_pdf("../../references/Opportunity-Youth-2016-Data-Brief-v2.pdf", pages = 9)[0]


def __get_age_table(df):
    """
    Parses out the age group table from the overall dataframe and adds the total values to it
    """
    age = df.iloc[[0,1,2]]
    age = pd.concat([pd.DataFrame([['50053', '41651', '48043', '139735']], columns = age.columns), age])
    age.index = ['Total', 'Oy', 'Working Without A Diploma', 'Not Oy']
    return age


def __get_edu_table(df):
    """
    Parses out the education level table from the overall dataframe and adds the total values to it
    """
    edu = df.iloc[[6,7,8,9]]
    edu = pd.concat([pd.DataFrame([['2805', '7284', '8728', '18817']], columns = edu.columns), edu])
    edu.index = ['Total', 'No diploma', 'diploma', 'some college', 'Degree']
    return edu


def __four_races():
    table_list = [['20864', '13997', '35824', '69050', '139735'],
                  ['3552', '2747', '3871', '8547', '18817'],
                  ['2841', '355', '809', '1508', '5513'],
                  ['14471', '10895', '31044', '58995', '115405']]
    df = pd.DataFrame(table_list, columns = ['Hispanic', 'African American', 'White', 'Other', 'Total'], index = ['Total', 'Oy', 'Working', 'Not Oy'])
    return df