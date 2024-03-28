"""
The script was used to process, clean and input some of the league statistics used in the report
"""

import pandas as pd
from data_cleaning import change_all_amounts_in_col
import numpy as np
from data_cleaning import add_column_change_of_players
from typing import List, Dict


def merge_cells(table, first_cell_index, second_cell_index) -> List[int]:
    """
    In the original acquired file on league statistics, the columns for expenditure and revenue were structured as
    follows: the first cell contained the values before the decimal point, the second the number after the decimal
    point and with an annotation indicating the size of the amount (billion, million or thousand) and the currency.
    The function takes the indexes of these columns and returns a list consisting of consecutive records written
    together, e.g. 1.32 million euro
    :param table: pd.DataFrame
    :param first_cell_index: int
    :param second_cell_index: int
    :return: List[Int]
    """
    new_cells = []
    for i, row in table.iterrows():
        new_cells.append(f"{row[first_cell_index]},{row[second_cell_index]}")

    return new_cells


def get_all_values_from_mx_league(main_table) -> Dict[int, any]:
    """
    In the original file on club finances, the Mexican MX league is missing. To get it, the function takes a main
    table that contains the finances of all clubs and their results, and then counts in each season how much
    inclusive the clubs in that league spent, how much they earned, how many players came to the clubs from that
    league, how many were sold from the clubs in that league and the financial balance
    :param main_table: pd.Dataframe
    :return: Dict[int, np.array[float]]
    """
    mx_league_statistics = {
        2016: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2017: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2018: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2019: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2020: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2021: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2022: np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        2023: np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    }
    for i, row in main_table.iterrows():
        if row['Rozgrywki'] == "Liga MX Clausura":
            mx_league_statistics[row['Sezon']] += np.array(
                [row['Wydatki'], row['Zawodnicy przychodzący'], row['Wpływy'], row['Zawodnicy odchodzący'],
                 row['Saldo']])

    return mx_league_statistics


def get_table_for_mx_league(main_table) -> pd.DataFrame:
    """
    The function uses the data collected in the get_all_values_from_mx_league function
    and converts it into a dataframe object describing the Mexican league
    :param main_table: pd.DataFrame
    :return: pd.DataFrame
    """
    dict_of_values_in_mx_league = get_all_values_from_mx_league(main_table)
    rows = {
        'Rozgrywki': [],
        'Zawodnicy przychodzący': [],
        'Zawodnicy odchodzący': [],
        'Sezon': [],
        'Wydatki': [],
        'Wpływy': [],
        'Saldo': [],
        'Suma zawodników przychodzących i odchodzących': []
    }
    for k, v in dict_of_values_in_mx_league.items():
        rows['Rozgrywki'].append("Liga MX Clausura")
        rows['Zawodnicy przychodzący'].append(v[1])
        rows['Zawodnicy odchodzący'].append(v[3])
        rows['Sezon'].append(k)
        rows['Wydatki'].append(v[0])
        rows['Wpływy'].append(v[2])
        rows['Saldo'].append(v[4])
        rows['Suma zawodników przychodzących i odchodzących'].append(v[1] + v[3])

    return pd.DataFrame(rows)


def add_column_sum_each_team_points(result_table):
    """
    This function collects data on the total number of points scored by a team in a given league in a given season.
    :param result_table:
    :return:
    """
    all_leagues = result_table.loc[:, 'Rozgrywki'].drop_duplicates()
    list_of_points_in_season_for_each_league = []
    for league in all_leagues:
        league_statistics = {
            2016: 0,
            2017: 0,
            2018: 0,
            2019: 0,
            2020: 0,
            2021: 0,
            2022: 0,
            2023: 0
        }
        for i, row in result_table.iterrows():
            if row['Rozgrywki'] == league:
                league_statistics[row['Sezon']] += row['Pkt']
        league_stat_and_name = league_statistics, league
        list_of_points_in_season_for_each_league.append(league_stat_and_name)

    return list_of_points_in_season_for_each_league


def return_table_sum_points_for_league(results_table):
    list_of_points = add_column_sum_each_team_points(results_table)

    rows = {
        'Rozgrywki': [],
        'Sezon': [],
        'Pkt': []
    }
    for league in list_of_points:
        stat, name = league
        for season, pkt in stat.items():
            rows['Rozgrywki'].append(name)
            rows['Sezon'].append(season)
            rows['Pkt'].append(pkt)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    main_table = pd.read_csv("../data/csv/main_table2.csv")
    pd.set_option('display.max_columns', None)
    mx_league_values = get_table_for_mx_league(main_table)
    table = pd.read_csv("../data/csv/leagues_finances.csv")

    new_table = table.loc[:, ['Rozgrywki', 'Zawodnicy przychodzący', 'Zawodnicy odchodzący', 'Sezon']]
    new_table['Wydatki'] = merge_cells(table, 3, 4)
    new_table['Wpływy'] = merge_cells(table, 6, 7)
    new_table['Saldo'] = merge_cells(table, 9, 10)
    new_table['Suma zawodników przychodzących i odchodzących'] = add_column_change_of_players(new_table,
                                                                                              index_incoming=1,
                                                                                              index_outcoming=2)
    new_table = change_all_amounts_in_col(new_table, [4, 5, 6])
    results_table = pd.read_csv("../data/csv/club_results.csv")
    leagues_results = return_table_sum_points_for_league(results_table)

    new_table = new_table._append(mx_league_values, ignore_index=True)

    print(pd.merge(new_table, leagues_results, how="left", on=['Rozgrywki', 'Sezon']))
    # pd.merge(new_table, leagues_results, how="left", on=['Rozgrywki', 'Sezon']).to_csv(
    #     "../data/csv/league_statistics.csv"
    # )
