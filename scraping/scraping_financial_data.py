"""
Script created to scrape financial data on football clubs from transfermarkt website
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os.path
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def configure_chrome_option() -> Options:
    """
    The function to set parameters without which webdriver for Google Chrome does not work
    :return: Options
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return chrome_options


def configure_driver(page):
    """
    Using the driver to connect to the website
    :param page: str
    """
    ser = Service(executable_path="/home/nikodem/PycharmProjects/analysis_of_data_on_football_clubs/scraping/chromedriver_linux64(1)/chromedriver")
    driver = webdriver.Chrome(service=ser, options=configure_chrome_option())
    driver.get("".join([url, f'&page={page}']))

    return driver


def find(driver, data):
    """
    The function, with the help of the BeutifulSoup library, finds tables on the page and collects data from them
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find("table", {"class": "items"})
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')
    for row in rows:
        column = row.find_all('td')
        column = [elem.text.strip() for elem in column]
        if column:
            data.append(column)
    driver.close()

    return data, headers


def scrap(file, url):
    if os.path.isfile(file):
        raise Exception("Hey, this file already exist!")

    number_of_pages = [x for x in range(1, 11)]
    data = []
    for page in number_of_pages:
        time.sleep(5)

        driver = configure_driver(page)
        data, headers = find(driver, data)

    driver.quit()

    pd_table = pd.DataFrame(data, columns=headers)
    pd_table.to_csv(file, index=False)


if __name__ == "__main__":
    url = 'https://www.transfermarkt.pl/transfers/einnahmenausgaben/statistik/plus/1?ids=a&sa=&saison_id=2020&saison_id_bis=2020&land_id=&nat=&kontinent_id=&pos=&altersklasse=&w_s=&leihe=&intern=0&plus=1'
    file = r'clubs_finances21.csv'
    scrap(file, url)
    # time.sleep(20)
    #
    # url = 'https://www.transfermarkt.pl/transfers/einnahmenausgaben/statistik/plus/1?ids=a&sa=&saison_id=2019&saison_id_bis=2019&land_id=&nat=&kontinent_id=&pos=&altersklasse=&w_s=&leihe=&intern=0&plus=1'
    # file = r'clubs_finances20.csv'
    # scrap(file, url)
    # time.sleep(20)
    #
    # url = 'https://www.transfermarkt.pl/transfers/einnahmenausgaben/statistik/plus/1?ids=a&sa=&saison_id=2018&saison_id_bis=2018&land_id=&nat=&kontinent_id=&pos=&altersklasse=&w_s=&leihe=&intern=0&plus=1'
    # file = r'clubs_finances19.csv'
    # scrap(file, url)
    # time.sleep(20)
    #
    # url = 'https://www.transfermarkt.pl/transfers/einnahmenausgaben/statistik/plus/1?ids=a&sa=&saison_id=2017&saison_id_bis=2017&land_id=&nat=&kontinent_id=&pos=&altersklasse=&w_s=&leihe=&intern=0&plus=1'
    # file = r'clubs_finances18.csv'
    # scrap(file, url)
    # time.sleep(20)
    #
    # url = 'https://www.transfermarkt.pl/transfers/einnahmenausgaben/statistik/plus/1?ids=a&sa=&saison_id=2016&saison_id_bis=2016&land_id=&nat=&kontinent_id=&pos=&altersklasse=&w_s=&leihe=&intern=0&plus=1'
    # file = r'clubs_finances17.csv'
    # scrap(file, url)
    # time.sleep(20)
    #
    # url = 'https://www.transfermarkt.pl/transfers/einnahmenausgaben/statistik/plus/1?ids=a&sa=&saison_id=2015&saison_id_bis=2015&land_id=&nat=&kontinent_id=&pos=&altersklasse=&w_s=&leihe=&intern=0&plus=1'
    # file = r'clubs_finances16.csv'
    # scrap(file, url)
