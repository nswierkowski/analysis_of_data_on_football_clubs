"""
A file created to review the number of data and make a preliminary determination of their suitability
"""

import pandas as pd


def add_every_league(finances):
    """
    The function returns a dictionary which assigns the number of related records to the league name
    :param finances: pd.DataFrame
    :return: Dict[str, int]
    """
    leagues = finances["Rozgrywki"]
    leagues_appearances = {}
    for league in leagues:
        if league in leagues_appearances:
            leagues_appearances[league] += 1
        else:
            leagues_appearances.update({league: 1})
    return leagues_appearances


def seasons_to_league(finances, new_leagues):
    """
    The function assigns to the name of the league a list of all the seasons it is associated with.
    :param finances: pd.DataFrame
    :param new_leagues: List[str]
    :return: Dict[str, List[int]]
    """
    leagues = finances['Rozgrywki']
    seasons = finances['Sezon']
    sea_to_league = {}
    for league, season in zip(leagues, seasons):
        if league in new_leagues:
            if league in sea_to_league:
                sea_to_league[league] += [season]
            else:
                sea_to_league.update({league: [season]})
    return {k: list(set(v)) for k, v in sea_to_league.items()}


def create_new_leagues(finances, leagues):
    """
    The function leaves only those records in the table whose league names are in the set "leagues"
    :param finances: pd.DataFrame
    :param leagues: set
    :return:
    """
    return finances[finances['Rozgrywki'].isin(leagues)]


if __name__ == '__main__':
    file = "../data/csv/clubs_finances.csv"
    finances = pd.read_csv(file)
    leagues = add_every_league(finances)
    print(dict(sorted(leagues.items(), key=lambda x: x[1],
                      reverse=True)))
    print(f"Number of leagues in table: {len(leagues)}")
    print(f"Number of records: {sum([x[1] for x in leagues.items()])}")
    print(seasons_to_league(finances, leagues))

    print("--------------------------------------------------------------------------------")

    new_leagues = dict(filter(lambda x: x[1] >= 40, leagues.items()))
    new_leagues = dict(sorted(new_leagues.items(), key=lambda x: x[1], reverse=True))
    print(new_leagues)
    print(len(new_leagues))
    print(f"Number of records: {sum([x[1] for x in new_leagues.items()])}")

    print(seasons_to_league(finances, new_leagues))

    print(new_leagues.keys())

    print(create_new_leagues(finances, new_leagues.keys()))
    #create_new_leagues(finances, new_leagues.keys()).to_csv("/home/nikodem/PycharmProjects/scrapping_data/data/csv/repaired_finances.csv")
