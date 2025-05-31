import sqlite3
from datetime import datetime


def initialize_database():
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_temperature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            temperature REAL,
            timestamp TEXT,
            FOREIGN KEY(city_id) REFERENCES cities(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forecast_temperature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            timestamp TEXT,
            temperature REAL,
            FOREIGN KEY(city_id) REFERENCES cities(id)
        )
    ''')

    connection.commit()
    connection.close()


def insert_city_if_not_exists(city_name, city_url):
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO cities (name, url) VALUES (?, ?)', (city_name, city_url))
        connection.commit()
    except sqlite3.IntegrityError:
        pass
    connection.close()


def get_city_id(city_url):
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM cities WHERE url = ?', (city_url,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return row[0]
    return None


def store_current_temperature(city_url, temperature):
    city_id = get_city_id(city_url)
    if city_id is not None:
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        connection = sqlite3.connect('weather.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO current_temperature (city_id, temperature, timestamp) VALUES (?, ?, ?)', (city_id, temperature, timestamp))
        connection.commit()
        connection.close()


def store_forecast_temperatures_with_timestamps(city_url, temperature_list, timestamp_list):
    city_id = get_city_id(city_url)
    if city_id is not None and len(temperature_list) == len(timestamp_list):
        connection = sqlite3.connect('weather.db')
        cursor = connection.cursor()
        for temp, timestamp in zip(temperature_list, timestamp_list):
            # Проверка наличия записи
            cursor.execute('''
                SELECT id FROM forecast_temperature
                WHERE city_id = ? AND timestamp = ?
            ''', (city_id, timestamp))
            if cursor.fetchone():
                continue  # Пропускаем, если уже есть запись

            cursor.execute('''
                INSERT INTO forecast_temperature (city_id, timestamp, temperature)
                VALUES (?, ?, ?)
            ''', (city_id, timestamp, temp))
        connection.commit()
        connection.close()

def get_all_city_urls():
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()
    cursor.execute('SELECT url FROM cities')
    urls = [row[0] for row in cursor.fetchall()]
    connection.close()
    return urls

def delete_city_if_not_in_config(city_url):
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()
    # Получить id города
    cursor.execute('SELECT id FROM cities WHERE url = ?', (city_url,))
    row = cursor.fetchone()
    if row:
        city_id = row[0]
        # Удалить данные из зависимых таблиц
        cursor.execute('DELETE FROM current_temperature WHERE city_id = ?', (city_id,))
        cursor.execute('DELETE FROM forecast_temperature WHERE city_id = ?', (city_id,))
        cursor.execute('DELETE FROM cities WHERE id = ?', (city_id,))
        connection.commit()
    connection.close()