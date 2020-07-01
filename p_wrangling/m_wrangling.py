import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import requests
import math
from bs4 import BeautifulSoup
import re

# wrangling functions

# Web scraping
def web_to_csv(url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'):

    # Connect to the web
    print('Starting web scraping...')
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table', {'width': '80%', 'border': '1', 'cellpadding': '2', 'cellspacing': '0'})

    # Create a list from the web data
    table_1 = str(table).split('</td>')

    # Cleaning '\n<td>'
    table_2 = []
    clean = ''

    for i in table_1:
        clean = re.sub('\n<td>', '', i)
        table_2.append(clean)

    # Cleaning long strings
    table_3 = []
    clean_1 = ''

    for i in table_2:
        if '[<table border="1"' in i:
            clean_1 = 'Belgium'
            table_3.append(clean_1)
        elif '</tr></table>,' in i:
            clean_1 = 'Argentina'
            table_3.append(clean_1)
        else:
            table_3.append(i)

    # Cleaning \n
    table_4 = []
    clean_2 = ''

    for i in table_3:
        clean_2 = re.sub('\n', '', i)
        table_4.append(clean_2)

    # Cleaning </tr><tr>
    table_5 = []
    clean_3 = ''

    for i in table_4:
        clean_3 = re.sub('</tr><tr>', '', i)
        table_5.append(clean_3)

    # Cleaning ''
    table_6 = []
    for i in table_5:
        if i == '':
            pass
        else:
            table_6.append(i)

    # Cleaning ()
    table_7 = []
    code = ''
    for i in table_6:
        code = re.sub('[()]', '', i)
        table_7.append(code)

    # Deleting last row
    i = len(table_7)
    table_7.pop(i - 1)

    # Create the DataFrame
    keys = [table_7[i] for i in range(0, len(table_7), 2)]
    values = [table_7[i] for i in range(1, len(table_7), 2)]

    DataFrame = pd.DataFrame({'Country': keys, 'Codes': values})

    # Export to CSV
    DataFrame.to_csv(f'./data/raw/countrys_codes.csv', index=False)

def df_api(api = 'API.csv'):
    return pd.read_csv(f'./data/raw/{api}')


def df_career(career = 'career_info.csv'):
    return pd.read_csv(f'./data/raw/{career}')


def df_country(country = 'country_info.csv'):
    return pd.read_csv(f'./data/raw/{country}')


def df_code(codes = 'countrys_codes.csv'):
    return pd.read_csv(f'./data/raw/{codes}')


def df_personal(personal = 'personal_info.csv'):
    return pd.read_csv(f'./data/raw/{personal}')


def df_poll(poll = 'poll_info.csv'):
    return pd.read_csv(f'./data/raw/{poll }')


def merging_api_career(api_df, career_df):

    print('Merging Data Frames...')
    api_df['normalized_job_code'] = api_df['uuid']
    api_df.drop(columns=['uuid'], inplace=True)

    #Merge api DF and career DF
    api_career = api_df.merge(career_df, on = 'normalized_job_code')
    return api_career

def merging_country_codes(country_df, code_df):

    # Cleaning code and merging country and code
    code_df['country_code'] = code_df['Codes']
    code_df.drop(columns=['Codes'], inplace=True)
    country_code = code_df.merge(country_df, on='country_code')
    return country_code


def merging_country_code_api_career(country_codes, api_careers):

    print('Preparing final DataFrame...')
    country_code_api_career = country_codes.merge(api_careers, on='uuid')

    # Delete the excess columns
    country_code_api_career.drop(columns=['country_code', 'uuid', 'normalized_job_title', 'parent_uuid', 'normalized_job_code',
                                          'dem_education_level', 'dem_full_time_job'], inplace=True)
    country_code_api_career.to_csv('./data/processed/processed.csv', index=False)

    return country_code_api_career

def wrangling():

    # Charge the pipeline
    print('Wranling Data...')
    web_to_csv()
    api_df = df_api()
    career_df = df_career()
    country_df = df_country()
    code_df = df_code()
    personal_df = df_personal
    poll_df = df_poll
    api_careers = merging_api_career(api_df, career_df)
    country_codes = merging_country_codes(country_df, code_df)
    final_df = merging_country_code_api_career(country_codes, api_careers)

    return final_df


