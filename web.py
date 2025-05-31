from flask import Blueprint, render_template, request
import requests
import matplotlib
matplotlib.use("Agg")  # Используем без GUI
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime
from flask_login import login_required

web_blueprint = Blueprint("web", __name__, template_folder="templates")
graph_path = os.path.join("static", "graph.png")

@web_blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    error = None
    graph_url = None

    # Получение списка городов с API
    try:
        response = requests.get("http://localhost:5000/api/cities")
        cities = response.json().get("cities", [])
    except Exception as e:
        error = f"Ошибка при получении списка городов: {e}"
        cities = []

    if request.method == "POST" and not error:
        city = request.form.get("city")
        day_input = request.form.get("day")
        month_input = request.form.get("month")
        year_input = request.form.get("year")

        if not city:
            error = "Город обязателен."
        elif day_input:
            try:
                datetime.strptime(day_input, "%d.%m.%Y")
                api_url = f"http://localhost:5000/api/temperature?city={city}&day={day_input}"
                date_str = day_input
            except ValueError:
                error = "Неверный формат даты. Используйте дд.мм.гггг"
        elif month_input:
            try:
                datetime.strptime("01." + month_input, "%d.%m.%Y")
                api_url = f"http://localhost:5000/api/temperature?city={city}&month={month_input}"
                date_str = month_input
            except ValueError:
                error = "Неверный формат месяца. Используйте мм.гггг"
        elif year_input:
            if not (year_input.isdigit() and len(year_input) == 4):
                error = "Неверный формат года. Используйте гггг"
            else:
                api_url = f"http://localhost:5000/api/temperature?city={city}&year={year_input}"
                date_str = year_input
        else:
            if day_input:
                api_url = f"http://localhost:5000/api/temperature?city={city}&day={day_input}"
                date_str = day_input
            elif month_input:
                api_url = f"http://localhost:5000/api/temperature?city={city}&month={month_input}"
                date_str = month_input
            elif year_input:
                api_url = f"http://localhost:5000/api/temperature?city={city}&year={year_input}"
                date_str = year_input
            else:
                error = "Укажите хотя бы один параметр даты: день, месяц или год."

        if not error:
            try:
                temp_response = requests.get(api_url)
                temp_data = temp_response.json().get("data", [])

                forecast_url = api_url.replace("/temperature", "/forecast")
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json().get("data", [])

                if not temp_data and not forecast_data:
                    error = "Нет данных для отображения."
                else:
                    plt.figure(figsize=(10, 4))

                    if temp_data:
                        df = pd.DataFrame(temp_data)
                        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                        df = df.sort_values("timestamp")
                        plt.plot(df["timestamp"], df["temperature"], marker="o", label="Текущая")

                    if forecast_data:
                        df2 = pd.DataFrame(forecast_data)
                        df2["timestamp"] = pd.to_datetime(df2["timestamp"], utc=True)
                        df2 = df2.sort_values("timestamp")
                        plt.plot(df2["timestamp"], df2["temperature"], marker="x", linestyle="--", label="Прогноз")

                    plt.title(f"Температура в {city} ({date_str})")
                    plt.xlabel("Время")
                    plt.ylabel("Температура, °C")
                    plt.grid(True)
                    plt.legend()
                    plt.tight_layout()
                    graph_path = os.path.join("static", "graph.png")
                    plt.savefig(graph_path)
                    plt.close()
                    graph_url = "/static/graph.png"
            except Exception as e:
                error = f"Ошибка при запросе или построении графика: {e}"

    return render_template("web.html", error=error, graph_url=graph_url, cities=cities)
