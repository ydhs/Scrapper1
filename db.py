import sqlite3
from datetime import datetime, timezone

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
            hour INTEGER,
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
        timestamp = datetime.now(timezone.utc).isoformat()
        connection = sqlite3.connect('weather.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO current_temperature (city_id, temperature, timestamp) VALUES (?, ?, ?)', (city_id, temperature, timestamp))
        connection.commit()
        connection.close()

def store_forecast_temperatures(city_url, temperature_list):
    city_id = get_city_id(city_url)
    if city_id is not None and len(temperature_list) == 8:
        timestamp = datetime.now(timezone.utc).isoformat()
        connection = sqlite3.connect('weather.db')
        cursor = connection.cursor()
        for index, temperature in enumerate(temperature_list):
            hour = 1 + index * 3
            cursor.execute('INSERT INTO forecast_temperature (city_id, timestamp, hour, temperature) VALUES (?, ?, ?, ?)', (city_id, timestamp, hour, temperature))
        connection.commit()
        connection.close()
