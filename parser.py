import time
from bs4 import BeautifulSoup
from db import store_current_temperature, store_forecast_temperatures_with_timestamps
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def fetch_current_temperature(browser, url):
    browser.get(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    wrapper = soup.find('div', class_='now-weather')
    if wrapper:
        tag = wrapper.find('temperature-value')
        if tag and tag.has_attr('value'):
            try:
                temp = float(tag['value'].replace('−', '-'))
                #timestamp = datetime.now(ZoneInfo("Asia/Novosibirsk")).isoformat()
                timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                print(f"Сохраняем: {temp}°C, {timestamp}")
                store_current_temperature(url, temp)
            except Exception as e:
                print("Ошибка при сохранении температуры:", e)
        else:
            print("Тег <temperature-value> не найден или не содержит атрибута 'value'.")
    else:
        print("Температурный тег не найден на странице.")

def fetch_forecast_for_tomorrow(browser, forecast_url, now_url):
    browser.get(forecast_url)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Чтение температур
    temps = []
    temp_row = soup.find('div', class_='widget-row widget-row-chart widget-row-chart-temperature-air row-with-caption')
    if temp_row:
        values = temp_row.find_all('div', class_='value')
        for el in values[:8]:
            try:
                t = float(el.get_text(strip=True)
                              .replace('−', '-')
                              .replace('\xa0', '')
                              .replace('°', ''))
                temps.append(t)
            except:
                pass

    # Чтение времени
    timestamps = []
    time_row = soup.find('div', class_='widget-row widget-row-datetime-time')
    if time_row:
        spans = time_row.find_all('span')
        for el in spans[:8]:
            try:
                hour = int(el.get_text(strip=True).replace(':00', ''))
                tomorrow = datetime.now() + timedelta(days=1)
                # здесь — чистая строка без +07:00
                ts = datetime(
                    tomorrow.year, tomorrow.month, tomorrow.day,
                    hour, 0, 0
                ).strftime("%Y-%m-%dT%H:%M:%S")
                timestamps.append(ts)
            except:
                pass

    if len(temps) == 8 and len(timestamps) == 8:
        store_forecast_temperatures_with_timestamps(now_url, temps, timestamps)

