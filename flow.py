from prefect import flow, task
import json
from selenium import webdriver
from db import initialize_database, insert_city_if_not_exists
from parser import fetch_current_temperature, fetch_forecast_for_tomorrow

@task
def setup_database():
    initialize_database()

@task
def load_config():
    with open('settings.json', encoding='utf-8') as f:
        return json.load(f)

@task
def process_city(city, browser):
    name = city['name']
    now = city['now_url']
    forecast = city['forecast_url']
    insert_city_if_not_exists(name, now)
    fetch_current_temperature(browser, now)
    fetch_forecast_for_tomorrow(browser, forecast, now)

@flow
def weather_collection_flow():
    setup_database()
    config = load_config()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    try:
        for city in config['cities']:
            process_city(city, browser)
    finally:
        browser.quit()

if __name__ == '__main__':
    weather_collection_flow()
