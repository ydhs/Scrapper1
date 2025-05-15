import time
from bs4 import BeautifulSoup
from selenium import webdriver
from db import store_current_temperature, store_forecast_temperatures

def fetch_current_temperature(browser, url):
    browser.get(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    tag = soup.find('temperature-value')
    if tag:
        try:
            temp = float(tag.text.replace('−', '-').replace('\xa0', '').replace('°', ''))
            store_current_temperature(url, temp)
        except:
            pass

def fetch_forecast_for_tomorrow(browser, forecast_url, now_url):
    browser.get(forecast_url)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    temps = []
    row = soup.find('div', class_='widget-row widget-row-chart widget-row-chart-temperature-air row-with-caption')
    if row:
        values = row.find_all('div', class_='value')
        for el in values[:8]:
            try:
                t = float(el.get_text(strip=True).replace('−', '-').replace('\xa0', '').replace('°', ''))
                temps.append(t)
            except:
                pass
    if len(temps) == 8:
        store_forecast_temperatures(now_url, temps)
