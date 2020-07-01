import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import requests
import math
from bs4 import BeautifulSoup
import re


# acquisition functions


# Function to charge the database tables
def create_csv_from_sql(sql_table=['country_info', 'career_info', 'personal_info', 'poll_info']):
    # Create the conection
    path = './data/raw_data_project_m1.db'
    engine = create_engine(f'sqlite:///{path}')

    # tables to csv
    for table in sql_table:
        try:
            df = pd.read_sql_query(f'SELECT * FROM {table}', engine)
            print(f'Loading the table {table}')
            df.to_csv(f'./data/raw/{table}.csv', index=False)
        except ValueError:
            print(f'The database {table} does not exist...')


# Function to charge the API
def create_csv_from_api(url= 'http://api.dataatwork.org/v1/jobs', csv='career_info'):
    # Get the data from the csv
    try:
        career = pd.read_csv(f'./data/raw/{csv}.csv')
        normalized_code = career['normalized_job_code']
        codes = normalized_code.unique()
    except ValueError:
        print(f'The csv is incorrect')

    # Connect to API
    api_data = []

    print('Calling API, take a coffee...')
    for i in codes:
        if type(i) == float:
            pass
        else:
            response = requests.get(f'{url}/{i}')
            json_data = response.json()
            API_data = pd.DataFrame(json_data, index=[0, 1, 2, 3])
            api_data.append(API_data)
    print('End API...')

    # Create the csv
    df_apis = pd.concat(api_data, ignore_index=True)
    df_apis.drop_duplicates(inplace=True, ignore_index=True)
    df_apis.to_csv(f'./data/raw/API.csv', index=False)


# Web scraping
def web_to_csv(url='https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'):
    # Connect to the web
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


# Generate the tables
def acquisition():
    create_csv_from_sql()
    create_csv_from_api()
