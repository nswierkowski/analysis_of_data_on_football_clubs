"""
Script created to create a csv file containing the names of the leagues from "repaired_finances.csv"
and the corresponding names from "club_results.csv"
"""

import pandas as pd


def get_clubs_names(finance_file, results_file):
    """This function is going to get all clubs names from both file"""
    finance_table = pd.read_csv(finance_file)
    results_table = pd.read_csv(results_file)

    # We have to remove duplicates from both files
    clubs_name_from_finance_table = finance_table.loc[:, ['Klub', 'Rozgrywki']].drop_duplicates()
    clubs_name_from_results_table = results_table.loc[:, ['Klub', 'Rozgrywki']].drop_duplicates()

    return pd.merge(clubs_name_from_finance_table,
                    clubs_name_from_results_table.rename(lambda x: x + '2', axis='columns'),
                    left_on=['Klub', 'Rozgrywki'],
                    right_on=['Klub2', 'Rozgrywki2'], how='outer').drop_duplicates()


def divide_table(table):
    """
    The function splits the dataframe into three dataframe objects:
    - The first one which does not contain a NaN in any pore,
    - The second one for which there is a NaN in either of the last two columns
    (data from a file related to club finances)
    - The third one which has a NaN in one of the first two columns
    (data from a file related to club results).
    :param table: pd.DataFrame
    :return: Tuple[Dataframe, DataFrame, DataFrame]
    """

    # Data already in place
    finished_table = table.dropna(subset=['Klub', 'Rozgrywki', 'Klub2', 'Rozgrywki2']).iloc[:, :3]

    # Data that appear in the finance table but have no counterpart in the results table
    finance_table = table[table['Klub2'].isna()].iloc[:, :2]

    # Data that appear in the results table but have no counterpart in the finance table
    results_table = table[table['Klub'].isna()].iloc[:, 2:]

    return finished_table, finance_table, results_table


def remove_records_from_list(records, df):
    """
    The function removes all dataframe records that occur in the list.
    :param records: List[str]
    :param df: pd.DataFrame
    :return df: pd.DataFrame
    """
    return df[~df.iloc[:, 0].isin(records)]


def find_similar_names(finance_table, results_table):
    """
    The function is designed to find similar data
    that differs slightly but is most likely to be a different name
    of a particular club e.g. FC Arsenal and Arsenal.
    Returns a tuple consisting of a:
    -dataframe of concatenated records from the input dataframes,
    -first dataframe with no elements in the new dataframe
    -second dataframe with no elements in the new dataframe
    :param finance_table:
    :param results_table:
    :return Tuple[pd.Dataframe, pd.Dataframe, pd.Dataframe]:
    """

    new_first_column = []
    new_second_column = []
    leagues = []
    for index2, row2 in results_table.iterrows():
        for index1, row1 in finance_table.iterrows():
            club2 = row2['Klub2']
            league2 = row2['Rozgrywki2']
            club1 = row1['Klub']
            league1 = row1['Rozgrywki']
            if league1 == league2 and club2 in club1:
                new_first_column.append(club1)
                new_second_column.append(club2)
                leagues.append(league1)

    return (pd.DataFrame({'Klub': new_first_column, 'Klub2': new_second_column, 'Rozgrywki': leagues}),
            remove_records_from_list(new_first_column, finance_table),
            remove_records_from_list(new_second_column, results_table))


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)

    finished_table, first_column, second_column = divide_table(
        get_clubs_names("../data/csv/repaired_finances.csv",
                        "../data/csv/club_results.csv"))

    similar_club_names_table, first_column, second_column = find_similar_names(first_column,
                                                                               second_column)

    corresponding_club_names = pd.concat([finished_table, similar_club_names_table, first_column])

    print(corresponding_club_names)


    # corresponding_club_names.to_csv(
    #     "/home/nikodem/PycharmProjects/scrapping_data/Driver/csv/corresponding_club_names.csv")
