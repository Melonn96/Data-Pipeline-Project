import pandas as pd
import numpy as np


# analysis functions
def rural_analysis(final_df):
    urban_data = final_df['rural'].tolist()

    # Categorize the different names of rural
    rural_list = []
    value = ''
    for i in urban_data:
        if (i == 'rural' or i == 'countryside' or i == 'Country'):
            value = 'rural'
            rural_list.append(value)
        else:
            value = 'urban'
            rural_list.append(value)

    # Drop the excess column
    final_df['Rural'] = rural_list
    final_df.drop(columns='rural', inplace=True)

    return final_df


def groupby_analysis(final):
    print('Start grouping variable...')
    data = final.groupby(['Country', 'title', 'Rural']).agg(Quantity=('title', 'count'))
    data.reset_index(inplace=True)

    return data


def percentage_calculations(data_frame):
    print('Calculating the percentages...')
    quantities = []
    numero = ''
    for i in data_frame['Country'].unique():
        quantities.append(data_frame[data_frame['Country'] == i]['Quantity'].tolist())

    percentage = 0
    percentage_list = []

    for i in quantities:
        for j in i:
            percentage = str(round((j / sum(i)) * 100, 1)) + '%'
            percentage_list.append(percentage)

    # Create the column percentage
    data_frame['Percentage'] = percentage_list
    data_frame.rename(columns={'title': 'Job Title'})

    return data_frame


def df_filter(data_frame, country):
    print(country)
    if country == None:
        print('Preparing Data...')
        return data_frame
    else:
        print('Filtering by country...')
        final_df_filtered = data_frame[data_frame['Country'] == country]
        final_df_filtered.reset_index(drop=True)

        return final_df_filtered


def analyze(df, country):
    df_final = rural_analysis(df)
    data_frame = groupby_analysis(df_final)
    final_data = percentage_calculations(data_frame)
    filtered_df = df_filter(final_data, country)

    return filtered_df
