"""
The script is used to scrape the results of football clubs in leagues from Wikipedia
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os.path
from selenium.webdriver.chrome.options import Options
from scraping_financial_data import configure_chrome_option
from selenium.webdriver.chrome.service import Service


def index_of_table(headers):
    """
    The function returns the index of a table that contains columns such as: ["Drużyna", "M", "R", "P"]
    :param headers: List[List[str]]
    :return: int
    """
    header_we_are_looking_for = ["Drużyna", "M", "R", "P"]
    for i, h in enumerate(headers):
        if all(elem in h for elem in header_we_are_looking_for):
            return i

    raise Exception("Not a table with such headings")
    return -1


def configure_driver(url):
    """
    Using the driver to connect to the website
    :param url: str
    """
    ser = Service(executable_path="/home/nikodem/PycharmProjects/analysis_of_data_on_football_clubs/scraping"
                                  "/chromedriver_linux64(1)/chromedriver")
    driver = webdriver.Chrome(service=ser, options=configure_chrome_option())
    driver.get(url)

    return driver


def scrap(file, url):
    if os.path.isfile(file):
        raise Exception("Hey, this file already exist!")

    data = []
    driver = configure_driver(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tables = soup.find_all("table", {"class": "wikitable"})

    all_headers = []
    for t in tables:
        all_headers += [[header.text.strip() for header in t.find_all('th')]]
    index_of_table_we_are_looking_for = index_of_table(all_headers)

    table = tables[index_of_table_we_are_looking_for]
    rows = table.find_all('tr')
    for row in rows:
        column = row.find_all('td')
        column = [elem.text.strip() for elem in column]
        if column:
            data.append(column[:10])
    driver.close()
    driver.quit()

    pd_table = pd.DataFrame(data, columns=all_headers[index_of_table_we_are_looking_for][:10])
    pd_table.to_csv(file, index=False)


def all_data_for_league(league_name, start=2015, end=2023) -> None:
    """
    Function created to scrape all tables for a given league name from the given years [start, end].
    :param league_name: str
    :param start: int
    :param end: int
    :return: None
    """
    time.sleep(20)
    url_basic = "https://pl.wikipedia.org/wiki/"
    for year in range(start, end):
        scrap("".join([league_name, f"{year+1}", '.csv']),
              "".join([url_basic, league_name, f"_({year}/{year + 1})"]))


if __name__ == "__main__":
    all_data_for_league("Bundesliga_niemiecka_w_piłce_nożnej", start=2017, end=2018)

