from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def scroll_to_the_bottom(height_to_scroll_to,driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_height = total_height - height_to_scroll_to
    driver.execute_script(f"window.scrollTo(0, {scroll_height});")


def click_on_button_to_show_more(driver):
    button = driver.find_element(By.XPATH, '//a[contains(@class, "button__button___fo2tk") and contains(text(), "More") and contains(text(), "Gas Prices")]')
    button.click()


def run_loop_to_get_page_data(driver):
    while(True):
        scroll_to_the_bottom(1264.25,driver)
        try:
            click_on_button_to_show_more(driver)
        except:
            break

        time.sleep(1)


def extract_page_values_with_beautiful_soup(driver):
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')


def get_titles_addresses_prices(soup):
    column_of_values = soup.find("div", class_ = "grid__column___nhz7X grid__tablet7___WBfn5 grid__desktop8___38Y4U")
    extract_titles = column_of_values.find_all("h3", class_="header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8")
    titles = [title.text.strip() for title in extract_titles]

    extract_address = column_of_values.find_all("div", class_ = "StationDisplay-module__address___2_c7v")
    addresses = [address.get_text(separator=" ").strip() for address in extract_address]

    extract_price = column_of_values.find_all("span", class_ ="text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL")
    prices = [price.text.replace('¢','') for price in extract_price]

    return titles, addresses, prices


def put_values_in_dictionary(titles, addresses, prices):
    array_of_dictionaries = []
    n = len(addresses)

    for i in range(n):
        try:
            array_of_dictionaries.append({'address': addresses[i], 'name': titles[i], 'price': float(prices[i].strip())})
        except:
            pass
    return array_of_dictionaries


def clean_up_array_from_errors(locations_array):
    cleaned_array = [entry for entry in locations_array if "distance" in entry and "duration" in entry]
    return cleaned_array
