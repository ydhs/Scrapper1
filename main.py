import json
from selenium import webdriver
from db import (
    initialize_database,
    insert_city_if_not_exists,
    delete_city_if_not_in_config,
    get_all_city_urls
)
from parser import fetch_current_temperature, fetch_forecast_for_tomorrow

if __name__ == '__main__':
    initialize_database()
    with open('settings.json', encoding='utf-8') as f:
        config = json.load(f)

    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    try:
        config_urls = []
        for city in config['cities']:
            name = city['name']
            now = city['now_url']
            forecast = city['forecast_url']
            insert_city_if_not_exists(name, now)
            config_urls.append(now)
            fetch_current_temperature(browser, now)
            fetch_forecast_for_tomorrow(browser, forecast, now)

        # Удаление городов, которых нет в settings.json
        existing_urls = get_all_city_urls()
        for url in existing_urls:
            if url not in config_urls:
                delete_city_if_not_in_config(url)
    finally:
        browser.quit()
