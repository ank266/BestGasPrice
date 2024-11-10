from selenium.webdriver.firefox.options import Options
from google_api_for_distance_and_duration import get_distances_and_times
import time
from filters import *
from scrape_from_gasbuddy import *
from apply_credit_card_rewards import apply_points
from selenium.webdriver.firefox.service import Service

import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
api_key = GOOGLE_API_KEY

city = ""
origin = ""
weight_price = 0.5
weight_distance = 0.0
weight_time = 0.5


def scrape_values():
    options = Options()
    options.add_argument("-headless")
    service = Service()
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(f"https://www.gasbuddy.com/home?search={city}%2C+canada&fuel=1&method=all&maxAge=24") 
    time.sleep(1.5)
    run_loop_to_get_page_data(driver)
    soup = extract_page_values_with_beautiful_soup(driver)
    driver.quit()
    return soup

def extract_values_from_page_into_dictionary(soup):
    dictionary_with_values = put_values_in_dictionary(get_titles_addresses_prices(soup)[0], get_titles_addresses_prices(soup)[1], get_titles_addresses_prices(soup)[2])
    destinations = [entry['address'] for entry in dictionary_with_values]
    return destinations, dictionary_with_values


def get_distance_and_duration_values(destinations, dictionary_with_values):
    locations, errors = get_distances_and_times(origin, destinations, api_key, dictionary_with_values)
    locations = clean_up_array_from_errors(locations)
    return locations


def filter_the_data_for_best_results(locations):
    sorted_data = sorted(locations, key=lambda x: x['duration'])
    best_locations = filter_get_best_locations_by_duration(sorted_data)
    best_locations = apply_points(best_locations)
    best_locations = filter_eliminate_high_price_repeats_that_are_far_away(best_locations)
    best_locations = filter_sort_based_on_weights(weight_price, weight_distance, weight_time, best_locations)
    best_locations = filter_by_quartile_values(best_locations, 40, 'price')
    return best_locations


def main():
    print("Scraping the values...")
    soup = scrape_values()
    destinations, dictionary_with_values = extract_values_from_page_into_dictionary(soup)
    print("Done scraping, now getting the distances and travel time from google maps...")
    locations = get_distance_and_duration_values(destinations, dictionary_with_values)
    print("Done getting maps value, now filtering...")
    best_locations = filter_the_data_for_best_results(locations)
    print(best_locations)


if __name__ == “__main__”:
         main()