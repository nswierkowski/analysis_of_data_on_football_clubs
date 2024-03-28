"""
Script created to save the created diagrams
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def return_the_mean_value(table, x_col, y_col):
    grouped_df = table.groupby(x_col)[y_col].mean().reset_index()
    grouped_df.drop_duplicates(subset=x_col, inplace=True)

    return grouped_df


def draw_points_to_matches(main_table):
    points = 'Pkt'
    number_of_matches = 'M'

    grouped_df = return_the_mean_value(main_table, number_of_matches, points)
    x = grouped_df[number_of_matches]
    y = grouped_df[points]

    plt.scatter(x, y)
    plt.xlabel('Liczba rozegranych meczy')
    plt.ylabel('Średnia liczba punktów zdobyta w ciągu sezonu')
    plt.title("Średnia liczby punktów zdobyta dla liczby rozegranych meczów")

    # plt.show()
    plt.savefig("punkt_od_meczy.jpg")


def draw_mean_points_per_match_to_matches(main_table):
    points_per_match = 'Średnia punktów na mecz'
    number_of_matches = 'M'

    grouped_df = return_the_mean_value(main_table, number_of_matches, points_per_match)
    x = grouped_df[number_of_matches]
    y = grouped_df[points_per_match]

    plt.scatter(x, y)
    plt.xlabel('Liczba rozegranych meczy')
    plt.ylabel('Średnia liczba punktów na mecz')
    plt.title("Zależność średniej liczby punktów na mecz od liczby rozegranych meczy")

    # plt.show()
    plt.savefig("Srednia_punktu_na_mecz_od_liczby_meczy.jpg")


def draw_clubs_points_per_leagues_points_to_matches(main_table):
    points_to_all_points = 'Punkty do sumy punktów ligi'
    number_of_matches = 'M'

    grouped_df = return_the_mean_value(main_table, number_of_matches, points_to_all_points)
    x = grouped_df[number_of_matches]
    y = grouped_df[points_to_all_points]

    plt.scatter(x, y)
    plt.xlabel('Liczba rozegranych meczy')
    plt.ylabel('Punkty klubów przez liczbe wszystkich punktów w lidze')
    plt.title("Stosunku liczby punktów klubu do ligi od liczby rozegranych meczy")

    # plt.show()
    plt.savefig("Stosunek_liczby_punktow_w_lidze_od_liczby_meczy.jpg")

def draw_clubs_points_per_leagues_points_to_mean_points_per_match(main_table):
    points_to_all_points = 'Punkty do sumy punktów ligi'
    points_per_match = 'Średnia punktów na mecz'

    plt.scatter(main_table[points_per_match], main_table[points_to_all_points])
    plt.xlabel('Średnia punktów na mecz')
    plt.ylabel('Punkty do sumy punktów ligi')
    plt.title("Stosunku liczby punktów klubu do ligi od średniej punktów na mecz")

    #plt.show()
    plt.savefig("Stosunek_liczby_punktow_w_lidze_od_punktow_na_mecz.jpg")


def draw_bar_for_leagues(x_col, y_col, xlabel, ylabel, title, filename, color='blue'):
    fig, ax = plt.subplots(figsize=(27, 8))
    bar_width = 0.8
    plt.bar(x_col, y_col, color=color, width=bar_width)
    x_ticks = ax.get_xticks()
    ax.set_xlim(x_ticks[0] - bar_width, x_ticks[-1] + bar_width)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    #plt.show()
    plt.savefig(filename, dpi=400)

def draw_leagues_outcome(main_table):
    league_name = 'Rozgrywki'
    outcome = 'Wydatki'

    grouped_df_leg = return_the_mean_value(main_table, league_name, outcome)
    draw_bar_for_leagues(grouped_df_leg[league_name], grouped_df_leg[outcome], 'Ligi',
                         'Średnia wydatków w setkach milionów na przestrzeni 8 sezonów', "Wydatki lig",
                         "Średnie wydatki klubu z danej ligi",
                         'red')

    outcome_to_all = 'Wydatki do wydatków ligi'
    grouped_df = return_the_mean_value(main_table, league_name, outcome_to_all)
    draw_bar_for_leagues(grouped_df[league_name], grouped_df[outcome_to_all], 'Ligi',
                         'Średnia wydatki w setkach milionów pojedyńczego klubu na przestrzeni 8 sezonów',
                         "Średnie stosunki wydatków klubów z lig do wszystkich wydatków ligi", "Wydatki klubów",
                         'red')

def draw_leagues_income(main_table):
    income = 'Wpływy'
    league_name = 'Rozgrywki'

    grouped_df_leg_income = return_the_mean_value(main_table, league_name, income)
    draw_bar_for_leagues(grouped_df_leg_income[league_name], grouped_df_leg_income[income], 'Ligi',
                         'Średnia wpływy w dziesiątkach milionów na przestrzeni 8 sezonów', "Zarobki lig",
                         "Średnie wpływy klubu z danej ligi")

    income_to_all = 'Wpływy do wpływów ligi'
    grouped_df_leg_income_2 = return_the_mean_value(main_table, league_name, income_to_all)
    draw_bar_for_leagues(grouped_df_leg_income_2[league_name], grouped_df_leg_income_2[income_to_all], 'Ligi',
                         'Średnia wpływów pojedyńczego klubu do sumy wpływów klubów z ligi',
                         "Zarobki lig",
                         'Średnie wpływy klubu do wpływów całej ligi')

def draw_incoming_players(main_table):
    number_of_incoming_players = 'Zawodnicy przychodzący'
    league_name = 'Rozgrywki'
    grouped_df_incoming_players = return_the_mean_value(main_table, league_name, number_of_incoming_players)
    draw_bar_for_leagues(grouped_df_incoming_players[league_name],
                         grouped_df_incoming_players[number_of_incoming_players], 'Ligi',
                         'Średnia liczba przychodzących nowych zawodników do klubu',
                         "Średnia liczba przychodzących nowych zawodników",
                         "Średnia liczba przychodzących zawodników do klubu ligi",
                         'green')

    ratio_of_incoming_players_to_all = 'Liczba przychodzących zawodników do zawodników przychodzących w całej lidze'
    grouped_df_incoming_players_ratio = return_the_mean_value(main_table, league_name, ratio_of_incoming_players_to_all)
    draw_bar_for_leagues(grouped_df_incoming_players_ratio[league_name],
                         grouped_df_incoming_players_ratio[ratio_of_incoming_players_to_all], 'Ligi',
                         'Średnia stosunku liczby przychodzących nowych zawodników do liczby przychodzących zawodników do ligi',
                         "Średnia liczba przychodzących nowych zawodników",
                         "Stosunek liczby nowych zawodników klubu przez wszystkich nowych zawodników ligi",
                         'green')

def draw_outcoming_players(main_table):
    number_of_outcoming_players = 'Zawodnicy odchodzący'
    league_name = 'Rozgrywki'

    grouped_df_incoming_players = return_the_mean_value(main_table, league_name, number_of_outcoming_players)
    draw_bar_for_leagues(grouped_df_incoming_players[league_name],
                         grouped_df_incoming_players[number_of_outcoming_players], 'Ligi',
                         'Średnia liczba odchodzących do nowych zawodników do klubu',
                         'Średnia liczba odchodzących zawodników z ligi',
                         'Średnia liczba odchodzących zawodników z ligi',
                         'orange')

    ratio_of_outcoming_players_to_all = 'Liczba odchodzących zawodników do zawodników odchodzących w całej lidze'
    grouped_df_outcoming_players_ratio = return_the_mean_value(main_table, league_name,
                                                               ratio_of_outcoming_players_to_all)
    draw_bar_for_leagues(grouped_df_outcoming_players_ratio[league_name],
                         grouped_df_outcoming_players_ratio[ratio_of_outcoming_players_to_all], 'Ligi',
                         'Średnia stosunku liczba odchodzących zawodników do liczby odchodzących zawodników z ligi',
                         'Średnia liczba odchodzących zawodników z klubu do liczby wszystkich zawodników odchodzących z ligi',
                         'Średnia liczba odchodzących zawodników z klubu do liczby wszystkich zawodników odchodzących z ligi',
                         'orange')

def draw_balance_bar(main_table):
    balance = 'Saldo'
    league_name = 'Rozgrywki'
    grouped_balance = return_the_mean_value(main_table, league_name, balance)
    draw_bar_for_leagues(grouped_balance[league_name], grouped_balance[balance], 'Ligi',
                         "Średnie saldo w dziesiątkach milionów",
                         "Średnie saldo klubu każdej z lig na przestrzeni ostatnich 8 sezonów",
                         'Średnie saldo transferowe klubu z danej ligi',
                         "purple")


def draw_scatter(table, x, y, xlabel, ylabel, title, color='blue'):
    plt.scatter(table[x], table[y], color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    #plt.show()
    print("filename = " + title)
    plt.savefig(f'{title}.jpg')

def draw_outcome_to_points_per_match(main_table):
    draw_scatter(main_table, 'Wydatki do wydatków ligi', 'Średnia punktów na mecz',
                 'Wydatków klubu do sumy wydatków ligi',
                 'Liczba punktów na mecz', 'Średnia punktów na mecz przez cały sezon od wydatków klubu',
                 'red')

def draw_income_to_points_per_match(main_table):
    draw_scatter(main_table, 'Wpływy do wpływów ligi', 'Średnia punktów na mecz',
                 'Wpływy klubu do sumy wpływów ligi',
                 'Liczba punktów na mecz', 'Średnia punktów na mecz od wpływów do klubu')


def scatter_log(table, x, y, title, filename, color='blue'):
    plt.scatter(table[x], table[y], color=color)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xscale('log')
    # plt.yscale('log')
    plt.title(title)

    #plt.show()
    plt.savefig(f'{filename}.jpg')

def draw_outcome_to_pointes_per_match_log(main_table):
    scatter_log(main_table, 'Wydatki do wydatków ligi', 'Średnia punktów na mecz',
                'Średnia punktów na mecz przez cały sezon od wydatków klubu',
                'Średnia punktów na mecz przez cały sezon od wydatków klubu (log)',
                'red')

def draw_income_to_pointes_per_match_log(main_table):
    scatter_log(main_table, 'Wpływy do wpływów ligi', 'Średnia punktów na mecz',
                'Średnia punktów na mecz przez cały sezon od wpływów klubu',
                'Średnia punktów na mecz przez cały sezon od wpływów klubu (log)',)


def plot(df, x_column, y_column, bin_width, title, filename, color='blue'):
    bins = np.arange(df[x_column].min(), df[x_column].max() + bin_width, bin_width)
    labels = bins[:-1] + bin_width / 2

    df['Bucket'] = pd.cut(df[x_column], bins=bins, labels=labels, include_lowest=True)

    grouped_df = df.groupby('Bucket')[y_column].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(grouped_df.index, grouped_df.values, color=color)
    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)

    #plt.show()
    plt.savefig(f"{filename}.jpg")

def draw_outcome_plot(main_table):
    plot(main_table,
         'Wydatki do wydatków ligi',
         'Średnia punktów na mecz',
         0.02,
         'Liczba punktów na mecz od wydatków klubu względem ligi',
         'Liczba punktów na mecz od wydatków klubu względem ligi (plot)',
         color='red')

def draw_income_plot(main_table):
    plot(main_table,
         'Wpływy do wpływów ligi',
         'Średnia punktów na mecz',
         0.02,
         'Liczba punktów na mecz od wpływów klubu względem ligi',
         'Liczba punktów na mecz od wpływów klubu względem ligi (plot)')

def draw_incoming_players(main_table):
    draw_scatter(main_table, 'Zawodnicy przychodzący',
                 'Średnia punktów na mecz',
                 'Zawodnicy przychodzący',
                 'Liczba punktów na mecz',
                 'Liczba punktów na mecz od liczby zawodników przychodzących',
                 'green')
    plot(main_table, 'Zawodnicy przychodzący', 'Średnia punktów na mecz', 5,
         'Liczba punktów na mecz od liczby przychodzących zawodników',
         'Liczba punktów na mecz od liczby przychodzących zawodników (plot)',
         color='green')

def draw_outcoming_players(main_table):
    draw_scatter(main_table, 'Zawodnicy odchodzący',
                 'Średnia punktów na mecz',
                 'Liczba zawodników odchodzących',
                 'Liczba punktów na mecz',
                 'Liczba punktów na mecz od liczby zawodników odchodzących',
                 'orange')
    plot(main_table, 'Zawodnicy odchodzący', 'Średnia punktów na mecz', 5,
         'Liczba punktów na mecz od liczby zawodników odchodzących',
         'Liczba punktów na mecz od liczby zawodników odchodzących (plot)',
         color='orange')

def draw_sum_incoming_and_outgoing_players(main_table):
    draw_scatter(main_table, 'Suma zawodników przychodzących i odchodzących',
                 'Średnia punktów na mecz',
                 'Suma zawodników przychodzących i odchodzących',
                 'Liczba punktów na mecz',
                 'Liczba punktów na mecz od łącznej liczby zmian kadrowych',
                 'black')

    plot(main_table, 'Suma zawodników przychodzących i odchodzących', 'Średnia punktów na mecz', 5,
         'Liczba punktów na mecz od łącznej liczby zmian kadrowych',
         'Liczba punktów na mecz od sumy zawodników przychodzących i odchodzących (plot)',
         color='black')

def draw_balance(main_table):
    draw_scatter(main_table, 'Saldo',
                 'Średnia punktów na mecz',
                 'Saldo transferowe klubu',
                 'Liczba punktów na mecz',
                 'Średnia punktów na mecz od salda transferowego',
                 'purple')
    plot(main_table, 'Saldo', 'Średnia punktów na mecz', 0.5 * 10 ** 8,
         'Średnia punktów na mecz od salda transferowego',
         'Średnia punktów na mecz od salda transferowego (plot)',
         color='purple')

if __name__ == "__main__":
    main_table = pd.read_csv("../data/csv/main_table3.csv")
    league_table = pd.read_csv('../data/csv/league_statistics.csv')
    # draw_leagues_outcome(main_table)
    # draw_leagues_income(main_table)
    # draw_incoming_players(main_table)
    # draw_outcoming_players(main_table)
    # draw_balance_bar(main_table)