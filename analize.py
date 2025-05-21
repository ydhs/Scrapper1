import sys
import argparse
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def main():
    parser = argparse.ArgumentParser(
        description="Visualize forecast and current temperatures for a given date."
    )
    parser.add_argument(
        "date",
        help="Date in format dd.mm.yyyy",
    )
    args = parser.parse_args()

    # Парсинг даты
    try:
        date = datetime.strptime(args.date, "%d.%m.%Y").date()
    except ValueError:
        print("Ошибка: дата должна быть в формате dd.mm.yyyy")
        sys.exit(1)

    # границы для SQL-запроса
    date_start = datetime.combine(date, datetime.min.time())
    date_end = date_start + timedelta(days=1)

    conn = sqlite3.connect("weather.db")

    # Получаем прогнозные данные
    forecast_df = pd.read_sql_query(
        """
        SELECT timestamp, temperature
        FROM forecast_temperature
        WHERE timestamp >= ? AND timestamp < ?
        """,
        conn,
        params=[
            date_start.strftime("%Y-%m-%dT%H:%M:%S"),
            date_end.strftime("%Y-%m-%dT%H:%M:%S"),
        ],
    )

    # Получаем реальные данные
    current_df = pd.read_sql_query(
        """
        SELECT timestamp, temperature
        FROM current_temperature
        WHERE timestamp >= ? AND timestamp < ?
        """,
        conn,
        params=[
            date_start.strftime("%Y-%m-%dT%H:%M:%S"),
            date_end.strftime("%Y-%m-%dT%H:%M:%S"),
        ],
    )
    conn.close()

    if forecast_df.empty and current_df.empty:
        print(f"Нет данных за дату {args.date}")
        sys.exit(0)

    # Конвертация строковых timestamp в datetime
    if not forecast_df.empty:
        forecast_df["timestamp"] = pd.to_datetime(forecast_df["timestamp"])
    if not current_df.empty:
        current_df["timestamp"] = pd.to_datetime(current_df["timestamp"])

    # Построение графика
    plt.figure(figsize=(10, 6))
    if not forecast_df.empty:
        plt.plot(
            forecast_df["timestamp"],
            forecast_df["temperature"],
            marker='o',
            linestyle='--',
            label='Forecast',
        )
    if not current_df.empty:
        plt.plot(
            current_df["timestamp"],
            current_df["temperature"],
            marker='o',
            linestyle='-',
            label='Current',
        )

    plt.xlabel("Time")
    plt.ylabel("Temperature, °C")
    plt.title(f"Temperatures on {args.date}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
