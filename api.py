from flask import Blueprint, request, Response
import sqlite3
import json
from datetime import datetime

api_blueprint = Blueprint("api", __name__)


def make_json(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json"
    ), status


def parse_date_params(args):
    #Извлекает day, month, year и возвращает диапазон дат (start, end)
    fmt_day = "%d.%m.%Y"
    fmt_month = "%m.%Y"
    fmt_year = "%Y"

    try:
        if "day" in args:
            d = datetime.strptime(args["day"], fmt_day)
            start = d.replace(hour=0, minute=0, second=0, microsecond=0)
            end = d.replace(hour=23, minute=59, second=59, microsecond=999999)
            return start.isoformat(), end.isoformat()
        elif "month" in args:
            d = datetime.strptime(args["month"], fmt_month)
            start = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if d.month == 12:
                end = d.replace(year=d.year + 1, month=1, day=1)
            else:
                end = d.replace(month=d.month + 1, day=1)
            end = end.replace(hour=0, minute=0, second=0)
            return start.isoformat(), end.isoformat()
        elif "year" in args:
            d = datetime.strptime(args["year"], fmt_year)
            start = datetime(d.year, 1, 1)
            end = datetime(d.year + 1, 1, 1)
            return start.isoformat(), end.isoformat()
    except ValueError:
        return None, None

    return None, None


@api_blueprint.route("/", methods=["GET"])
def api_root():
    return make_json({"message": "API работает. Используйте /api/temperature?city=..."}, 200)


@api_blueprint.route("/temperature")
def temperature():
    city = request.args.get("city")
    if not city:
        return make_json({"error": "нужно указать параметр ?city=..."}, 400)

    start, end = parse_date_params(request.args)
    sort_order = request.args.get("sort", "asc").lower()
    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    conn = sqlite3.connect("weather.db")
    cur = conn.cursor()

    if start and end:
        query = f"""
            SELECT temperature, timestamp FROM current_temperature
            JOIN cities ON current_temperature.city_id = cities.id
            WHERE cities.name = ? AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp {sort_order}
        """
        rows = cur.execute(query, (city, start, end)).fetchall()
        conn.close()
        if rows:
            data = [{"temperature": r[0], "timestamp": r[1]} for r in rows]
            return make_json({"city": city, "data": data})
        return make_json({"error": "нет данных за указанный период"}, 404)
    else:
        query = """
            SELECT temperature, timestamp FROM current_temperature
            JOIN cities ON current_temperature.city_id = cities.id
            WHERE cities.name = ?
            ORDER BY timestamp DESC LIMIT 1
        """
        result = cur.execute(query, (city,)).fetchone()
        conn.close()
        if result:
            return make_json({
                "city": city,
                "temperature": result[0],
                "timestamp": result[1]
            })
        return make_json({"error": "нет данных по городу"}, 404)


@api_blueprint.route("/forecast")
def forecast():
    city = request.args.get("city")
    if not city:
        return make_json({"error": "нужно указать параметр ?city=..."}, 400)

    start, end = parse_date_params(request.args)
    sort_order = request.args.get("sort", "asc").lower()
    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    conn = sqlite3.connect("weather.db")
    cur = conn.cursor()

    if start and end:
        query = f"""
            SELECT temperature, timestamp FROM forecast_temperature
            JOIN cities ON forecast_temperature.city_id = cities.id
            WHERE cities.name = ? AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp {sort_order}
        """
        rows = cur.execute(query, (city, start, end)).fetchall()
        conn.close()
        if rows:
            data = [{"temperature": r[0], "timestamp": r[1]} for r in rows]
            return make_json({"city": city, "data": data})
        return make_json({"error": "нет прогноза за указанный период"}, 404)
    else:
        query = """
            SELECT temperature, timestamp FROM forecast_temperature
            JOIN cities ON forecast_temperature.city_id = cities.id
            WHERE cities.name = ?
            ORDER BY timestamp DESC LIMIT 1
        """
        result = cur.execute(query, (city,)).fetchone()
        conn.close()
        if result:
            return make_json({
                "city": city,
                "temperature": result[0],
                "timestamp": result[1]
            })
        return make_json({"error": "нет прогноза по городу"}, 404)
