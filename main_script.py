import argparse
from p_acquisition import m_acquisition
from p_wrangling import m_wrangling
from p_analysis import m_analysis
from p_reporting import m_reporting


def argument_parser():
    parser = argparse.ArgumentParser(description='Set chart type')
    parser.add_argument('-c', '--country', type=str, dest='country', required=False,
                        help='Introduce the country to study...')
    args = parser.parse_args()
    return args


def main(country):
    print('Starting pipeline...')

    # Acquisition
    m_acquisition.acquisition()

    # Wrangling
    df = m_wrangling.wrangling()

    # Analysis
    final_data = m_analysis.analyze(df, country)

    # Reporting
    m_reporting.reporting(final_data, country)

    print('pipeline finished...')


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments.country)
