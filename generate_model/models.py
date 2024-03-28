"""The script splits the data into test (0.25) and training (0.75) then trains and tests the models: linear
regression, random forest and SVR, and then generates a graph of the results """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def split_dataframe(table):
    """
    The function divides the data into training and test data and then normalises the data
    """

    X = table[['Saldo', 'Wpływy do wpływów ligi', 'Wydatki do wydatków ligi']]
    Y = table['Średnia punktów na mecz']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

    sc = StandardScaler()

    sc.fit(X_train)

    X_train_sc = sc.transform(X_train)

    X_test_sc = sc.transform(X_test)

    return X_train_sc, X_test_sc, Y_train, Y_test


def svr_multi_argument_regression(X_train, X_test, Y_train, Y_test):
    """
    The function trains the SVR model on the test data and returns the mean absolute error
    """
    model = SVR()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    return mean_absolute_error(Y_test, predictions)


def random_forest_multi_argument_regression(X_train, X_test, Y_train, Y_test):
    """
    The function trains the random forest model on the test data and returns the mean absolute error
    """
    model = RandomForestRegressor()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    return mean_absolute_error(Y_test, predictions)


def multi_argument_regression(X_train, X_test, Y_train, Y_test):
    """
    The function trains the linear regression model on the test data and returns the mean absolute error
    """
    model = LinearRegression()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    return mean_absolute_error(Y_test, predictions)


def draw_models_results(results):
    """
    The function draws the results of the models
    """
    x = np.arange(len(results[0]))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, results[1], width, label='Modele bez argumentu "saldo"')
    bars2 = ax.bar(x + width / 2, results[2], width, label='Modele z argumentem "saldo"')

    ax.set_ylim(0.28, max(max(results[1]), max(results[2])) * 1.1)
    ax.set_ylabel('Średni błąd bezwzględny')
    ax.set_xlabel('Modele')
    ax.set_title('Wyniki modeli')
    ax.set_xticks(x)
    ax.set_xticklabels(results[0])
    ax.legend()

    plt.show()
    #plt.savefig("Wyniki modeli.png")


if __name__ == "__main__":
    table = pd.read_csv("../data/csv/main_table3.csv")
    X_train, X_test, Y_train, Y_test = split_dataframe(
        table)

    x = ['Saldo', 'Wydatki do wydatków ligi', 'Wpływy do wpływów ligi']
    y = ['Średnia punktów na mecz']


    X_train_no_balance = X_train[1:]
    Y_train_no_balance = Y_train[1:]
    X_test_no_balance = X_test[1:]
    Y_test_no_balance = Y_test[1:]

    regression = multi_argument_regression(X_train_no_balance, X_test_no_balance, Y_train_no_balance, Y_test_no_balance)
    random_forest = random_forest_multi_argument_regression(X_train_no_balance, X_test_no_balance, Y_train_no_balance,
                                                            Y_test_no_balance)
    svr = svr_multi_argument_regression(X_train_no_balance, X_test_no_balance, Y_train_no_balance, Y_test_no_balance)

    print("MODEL NA PODSTAWIE WYDATKÓW I WPŁYWÓW")
    print("---------------------------------------------------------------------------------------")
    print("Multi_argument regression: " + str(regression))
    print("Random forest: " + str(random_forest))
    print("SVR: " + str(svr))
    print("---------------------------------------------------------------------------------------")

    regression_with_balance = multi_argument_regression(X_train, X_test, Y_train, Y_test)
    random_forest_with_balance = random_forest_multi_argument_regression(X_train, X_test, Y_train, Y_test)
    svr_with_balance = svr_multi_argument_regression(X_train, X_test, Y_train, Y_test)

    print("MODEL NA PODSTAWIE WYDATKÓW, WPŁYWÓW I SALDA TRANSFEROWEGO")
    print("---------------------------------------------------------------------------------------")
    print("Multi_argument regression: " + str(regression_with_balance))
    print("Random forest: " + str(random_forest_with_balance))
    print("SVR: " + str(svr_with_balance))
    print("---------------------------------------------------------------------------------------")

    results = [["Regresja liniowa", "Random forest", "SVR"],
               [regression, random_forest, svr],
               [regression_with_balance, random_forest_with_balance, svr_with_balance]]

    draw_models_results(results)
