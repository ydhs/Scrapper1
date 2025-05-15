# analyze.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка текущей температуры
def plot_current_temperatures():
    connection = sqlite3.connect('weather.db')
    query = '''
        SELECT cities.name, current_temperature.temperature
        FROM current_temperature
        JOIN cities ON current_temperature.city_id = cities.id
    '''
    df = pd.read_sql_query(query, connection)
    connection.close()

    if not df.empty:
        df.groupby('name')['temperature'].mean().plot(kind='bar', title='Текущая температура по городам')
        plt.ylabel('Температура (°C)')
        plt.show()
    else:
        print("Нет данных о текущей температуре.")

# Загрузка прогнозов на завтра
def plot_forecast_temperatures():
    connection = sqlite3.connect('weather.db')
    query = '''
        SELECT cities.name, forecast_temperature.hour, forecast_temperature.temperature
        FROM forecast_temperature
        JOIN cities ON forecast_temperature.city_id = cities.id
    '''
    df = pd.read_sql_query(query, connection)
    connection.close()

    if not df.empty:
        for city in df['name'].unique():
            city_data = df[df['name'] == city]
            city_data = city_data.sort_values(by='hour')
            plt.bar(city_data['hour'], city_data['temperature'])
            plt.title(f'Прогноз температуры на завтра — {city}')
            plt.xlabel('Часы')
            plt.ylabel('Температура (°C)')
            plt.xticks(city_data['hour'])
            plt.show()
    else:
        print("Нет данных о прогнозе температуры.")

if __name__ == '__main__':
    plot_current_temperatures()
    plot_forecast_temperatures()
