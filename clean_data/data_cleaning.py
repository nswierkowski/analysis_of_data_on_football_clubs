"""
Script created to change the values in the amount column to integers and add the other columns necessary for the model
"""

from typing import List
import pandas as pd


def change_amounts(amount) -> float:
    """
    The function takes a string representing an amount and converts it into a value
    "-" = 0
    "x.yz mld euro" = x.yz * 10^9
    "x.yz mln euro" = x.yz * 10^6
    "x.yz tys euro" = x.yz * 10^3
    """

    if amount == "-":
        return 0

    [value, power_str, currency] = amount.split()

    power = 1
    if power_str == "mld":
        power = 9
    elif power_str == "mln":
        power = 6
    elif power_str == "tys.":
        power = 3
    else:
        print("ERROR")

    value = value.replace(".", "")
    minus = 1
    if value[0] == "-":
        minus = -1
        value = value[1:]

    return minus * float(value.replace(",", ".")) * (10 ** power)


def change_all_amounts_in_col(table, index) -> pd.DataFrame:
    """
    Function using the change_amounts function changes all values in the list of column indices to integers
    :param table: pd.DataFrame
    :param index: List[int]
    :return: pd.DataFrame
    """
    new_table = table.copy()

    for i in index:
        new_table.iloc[:, i] = new_table.iloc[:, i].apply(change_amounts)

    return new_table


def add_column_change_of_players(table, index_incoming=5, index_outcoming=7) -> List[int]:
    """
    The function adds a column about the total of incoming and outgoing players
    :param table: pd.DataFrame
    :param index_incoming: int
    :param index_outcoming: int
    :return: List[int]
    """
    all_change_of_players = []
    for i, row in table.iterrows():
        all_change_of_players.append(row[index_incoming] + row[index_outcoming])

    return all_change_of_players


def add_column_point_per_game(table) -> List[int]:
    """
    Function adds a column for average points per game
    :param table: pd.DataFrame
    :return: List[int]
    """
    all_points_per_game = []
    for i, row in table.iterrows():
        all_points_per_game.append(row['Pkt'] / row['M'])

    return all_points_per_game


def club_to_league(main_table, league_stats):
    """
    The function adds columns that are calculated as:
    attribute value per club / sum of attribute values for all clubs in the league that season
    :param main_table: pd.DataFrame
    :param league_stats: pd.DataFrame
    """
    all_clubs_income_to_league = []
    all_clubs_outcome_to_league = []
    all_clubs_points_to_league = []
    all_clubs_players_income_to_league = []
    all_clubs_players_outcome_to_league = []
    for i, row in main_table.iterrows():
        leg_row = league_stats[(league_stats['Rozgrywki'] == row['Rozgrywki']) & (league_stats['Sezon'] == row['Sezon'])]

        all_clubs_income_to_league.append(row['Wpływy'] / leg_row.iloc[0]['Wpływy'])
        all_clubs_outcome_to_league.append(row['Wydatki'] / leg_row.iloc[0]['Wydatki'])
        all_clubs_points_to_league.append(row['Pkt'] / leg_row.iloc[0]['Pkt'])
        all_clubs_players_income_to_league.append(
                    row['Zawodnicy przychodzący'] / leg_row.iloc[0]['Zawodnicy przychodzący'])
        all_clubs_players_outcome_to_league.append(
                    row['Zawodnicy odchodzący'] / leg_row.iloc[0]['Zawodnicy odchodzący'])

    return {
        "Wpływy do wpływów ligi": all_clubs_income_to_league,
        "Wydatki do wydatków ligi": all_clubs_outcome_to_league,
        "Punkty do sumy punktów ligi": all_clubs_points_to_league,
        "Liczba przychodzących zawodników do zawodników przychodzących w całej lidze":
            all_clubs_players_income_to_league,
        "Liczba odchodzących zawodników do zawodników odchodzących w całej lidze":
            all_clubs_players_outcome_to_league
    }

if __name__ == "__main__":
    table = pd.read_csv("../data/csv/main_table.csv")
    new_table = change_all_amounts_in_col(table, [4, 6, 8])
    pd.set_option('display.max_columns', None)

    new_table['Suma zawodników przychodzących i odchodzących'] = add_column_change_of_players(new_table)
    new_table['Średnia punktów na mecz'] = add_column_point_per_game(new_table)

    leg_stats = pd.read_csv("../data/csv/league_statistics.csv")
    columns_comparing_club_to_league = club_to_league(new_table, leg_stats)

    for title, row in columns_comparing_club_to_league.items():
        new_table[title] = row

    print(new_table)
   # new_table.iloc[:, 2:].to_csv("/home/nikodem/PycharmProjects/scrapping_data/data/csv/main_table3.csv", index=False)