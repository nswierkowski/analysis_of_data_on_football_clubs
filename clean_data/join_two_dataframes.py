"""
This python file has the task, using the dictionary created in the file "Repair_clubs_names.py", of unifying the
names of football clubs and then, with the help of left join, assigning to the teams expenses in a given season the
corresponding final result in the league table
"""

import pandas as pd


def change_clubs_names(dictionary, table):
    """
    The function with the help of the "dictionary" changes the names of the clubs from the results to alternative ones
    :param dictionary: pd.DataFrame
    :param table: pd.DataFrame
    :return: pd.DataFrame
    """

    new_table = table.copy()
    for index, row in dictionary.iterrows():
        club2 = row['Klub2']
        league = row['Rozgrywki']
        club = row['Klub']
        new_table.loc[(new_table['Klub'] == club2) & (new_table['Rozgrywki'] == league), 'Klub'] = club

    return new_table


def merge(result, finances) -> pd.DataFrame:
    """
    The function performs left join on the two input dataframes
    :param result: pd.DataFrame
    :param finances: pd.DataFrame
    :return: pd.DataFrame
    """
    return pd.merge(finances, result, how="left", on=["Klub", "Rozgrywki", "Sezon"])


def save(merged_file, file_name) -> None:
    """
    The function saves the dataframe to a csv file with the specified name
    :param merged_file: pd.DataFrame
    :param file_name: pd.DataFrame
    :return: None
    """
    merged_file.to_csv(file_name)


if __name__ == "__main__":
    dic = pd.read_csv("../data/csv/corresponding_club_names.csv")
    finances = pd.read_csv("../data/csv/repaired_finances.csv")
    results = pd.read_csv("../data/csv/club_results.csv")

    new_finances = change_clubs_names(dic, finances)
    new_results = change_clubs_names(dic, results)

    print(res := merge(new_results, new_finances))
    print(res.isnull().any(axis=1).sum())

    #save(res, "../data/csv/main_table.csv")
