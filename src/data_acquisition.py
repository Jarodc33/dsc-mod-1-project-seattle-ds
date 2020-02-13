import pandas as pd
import psycopg2
"""
Notes for making use of these methods

Types of methods
Split Method:     Splits a dataframe into multiple data frames with certain conditions. Returns a dictionary of these splits
Filter Method:    Filters a dataframe to follow a certain trait.
Breakdown Method: Takes a dataframe and breaks up the data into their respective categories and sums up the weighted population
                  This is like a split method but sums up the weights.

!!!
Breakdown must make a total key if you want a table with percentage
!!!

All these methods are also usefull outside the breakdow_by_split method

breakdown_by_split will split a given dataframe, filter it (optional), and break it down
"""

def breakdown_by_split(df, split, breakdown, optional_filter = None):
    """
    Gives the oy breakdown by race for hispanic, black, white, and other

    Parameters
    ----------
    df: dataframe to be broken into race and then oportunity youth stats
    split: function that with split the tables into multiple tables
    breakdown: function that will break the tables into subcategories an get the sums
    optional_filter: if a function is given, this will filter each table after being split

    Returns
    -------
    Dictionary of dictionarys where the keys are the race and the values are the breakdown sums
    """
    dct = {}
    groups = split(df)
    for group in groups.keys():
        if optional_filter:
            dct[group] = breakdown(optional_filter(groups[group]))
        else:
            dct[group] = breakdown(groups[group])
    return dct

def filter_oy(df):
    """
    Gets OY from df
    """
    return df[(df['sch'] == '1') & ((df['esr'] == '3') | (df['esr'] == '6'))]

def split_by4_race(df):
    """
    Breaks the dataframe into hispanic, black, white, and other

    Parameters
    ----------
    df: data frame to be split up

    Returns
    -------
    dictionary of daraframes split by race
    """
    dct = {}
    dct['total']            = df.copy()
    dct['hispanic']         = df[(df['hisp'] != '01')]
    dct['african american'] = df[(df['rac1p'] == '2') & (df['hisp'] == '01')]
    dct['white']            = df[(df['rac1p'] == '1') & (df['hisp'] == '01')]
    dct['other']            = df[(df['rac1p'] != '1') & (df['rac1p'] != '2') & (df['hisp'] == '01')]
    return dct

def split_by_age(df):
    """
    Breaks the dataframe into 16-18, 19-21, 22-24

    Parameters
    ----------
    df: data frame to be split up

    Returns
    -------
    dictionary of daraframes split by age
    """
    dct = {}
    dct['total'] = df.copy()
    dct['16-18'] = df[((df['agep'] >= 16) & (df['agep'] <= 18))]
    dct['19-21'] = df[((df['agep'] >= 19) & (df['agep'] <= 21))]
    dct['22-24'] = df[((df['agep'] >= 22) & (df['agep'] <= 24))]
    return dct


def split_by_all_race(df):
    """
    Breaks the dataframe into many races

    Parameters
    ----------
    df: data frame to be split up

    Returns
    -------
    dictionary of daraframes split by race
    """
    dct = {}
    dct['total']                                = df.copy()
    dct['native american']                      = df[(df['rac1p'].isin(['3', '4', '5']) & (df['hisp'] == '01'))]
    dct['pacific islander and native hawaiian'] = df[(df['rac1p'].isin(['7']) & (df['hisp'] == '01'))]
    dct['african american']                     = df[(df['rac1p'].isin(['2']) & (df['hisp'] == '01'))]
    dct['hispanic']                             = df[((df['hisp'] != '01') & (df['rac1p'].isin(['8'])))] 
    dct['asian']                                = df[(df['rac1p'].isin(['6']) & (df['hisp'] == '01'))]
    dct['white']                                = df[(df['rac1p'].isin(['1']) & (df['hisp'] == '01'))]
    dct['two or more']                          = df[(df['rac1p'].isin(['9']) & (df['hisp'] == '01'))]
    dct['other']                                = df[(df['rac1p'].isin(['8']))]
    return dct

def oy_breakdown(df):
    """
    Breaks the dataframe into 4 dataframes and gives the number of people in that data frame the 4 dataframes are total, oy, working without diploma, not oy

    Parameters
    ----------
    df: dataframe to be brokendown

    Returns
    -------
    dictionary of the specified dataframe totals
    """
    dct = {}
    dct['total'] =      df['pwgtp'].sum() # total sum
    dct['oy'] =         filter_oy(df)['pwgtp'].sum() # not working and not in school
    dct['working without a diploma'] = df[(df['sch'] == '1')
                            & (df['schl'].isin(['15', '14', '13', '12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '01']))
                            & ((df['esr'] != '3') & (df['esr'] != '6'))]['pwgtp'].sum() # working with no GED
    dct['not oy'] =     df[((~df['schl'].isin(['15', '14', '13', '12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '01']) & ((df['esr'] != '3') & (df['esr'] != '6')))
                            | (df['sch'] != '1'))]['pwgtp'].sum() # either in school or working with a GED
    return dct

def education_breakdown(df):
    """
    Breaks the dataframe into education acheivment totals

    Parameters
    ----------
    df: dataframe to be broken into education achievement

    Returns
    -------
    Dictionary of the total number of people with education achievement level
    """
    dct = {}
    dct['total']        = df.copy()['pwgtp'].sum()
    dct['no diploma']   = df[df['schl'].isin(['15', '14', '13', '12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '02', '01'])]['pwgtp'].sum()
    dct['diploma']      = df[df['schl'].isin(['16', '17'])]['pwgtp'].sum()
    dct['some college'] = df[df['schl'].isin(['18', '19'])]['pwgtp'].sum()
    dct['degree']       = df[df['schl'].isin(['20', '21', '22', '23', '24'])]['pwgtp'].sum()

    return dct



def get_youth_by_puma(start_puma = 11610, end_puma = 11615, dbname = 'opportunity_youth'):
    """
    Gives a table of youth from a given PUMA Range based on a given database name.
    Defaults are set for each parameter
    """
    conn = psycopg2.connect(dbname = dbname)
    df = pd.read_sql(f"SELECT * FROM pums_2017 WHERE (puma between '{start_puma}' and '{end_puma}') and (agep between '16' and '24')", conn)
    conn.close()
    return df


def get_oy_by_puma(start_puma = 11610, end_puma = 11615, dbname = 'opportunity_youth'):
    """
    Will Give a table of the OY for each PUMA in a range of pumas given from a given database
    Defaults are set for each parameter
    """
    sql_str = f"""SELECT pwgtp, SCH, ESR, puma, agep
                  FROM pums_2017
                  WHERE SCH = '1' and (ESR = '3' or ESR = '6') and (puma between '{start_puma}' and '{end_puma}') and (agep between '16' and '24')"""
    conn = psycopg2.connect(dbname = dbname)
    oy_by_puma = pd.read_sql(f"""SELECT puma, SUM(pwgtp) AS TotalPeople FROM ({sql_str}) AS a GROUP BY puma""", conn)
    conn.close()
    return oy_by_puma
