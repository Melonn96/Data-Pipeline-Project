import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# reporting functions


def final_data_to_csv(final_data):
    final_data.to_csv(f'./data/results/reporting.csv', index=False)


def plotting(df, country):

    # Group the data in urban and rural
    figure_1 = df.groupby('Rural').sum()
    figure_1.reset_index(inplace=True)

    # Create the chart
    plt.figure(figsize=(14, 8))
    chart = sns.barplot(data=figure_1, x=figure_1['Rural'], y=figure_1['Quantity'])

    if country == None:
        plt.title('Rural Data Jobs VS Urban Data Jobs worldwide' + '\n', fontsize=16)
    else:
        plt.title(f'Rural Data Jobs VS Urban Data Jobs in {country}' + '\n', fontsize=16)

    save_viz(chart, 'rural')

    return chart

def plotting_top_jobs(df, country):

    # Group the data by job title
    figure_2 = df.groupby('title').sum()
    figure_2.reset_index(inplace=True)
    figure_2.sort_values(by='Quantity', inplace=True, ascending=False)
    top_jobs = figure_2.nlargest(10, ['Quantity'])

    # Create the chart
    plt.figure(figsize=(22, 8))
    chart = sns.barplot(data=top_jobs, x=top_jobs['Quantity'], y=top_jobs['title'])

    if country == None:
        plt.title('Top jobs worldwide' + '\n', fontsize=16)
    else:
        plt.title(f'Top jobs {country}' + '\n', fontsize=16)

    save_viz(chart, 'title')

    return chart


def save_viz(chart, title):
    fig = chart.get_figure()
    fig.savefig(f'./data/results/{title}.png')


def reporting(df_final, country):
    final_data_to_csv(df_final)

    chart = plotting(df_final, country)
    chart_2 = plotting_top_jobs(df_final, country)

    save_viz(chart, 'rural')
    save_viz(chart_2, 'title')
