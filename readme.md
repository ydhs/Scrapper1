# Scraper1
Проект для сбора, хранения и анализа данных о текущей и прогнозной температуре в указанных городах.
## Функции
- **main.py**: инициализация базы данных, чтение списка городов из settings.json, сбор текущей температуры и прогноза на завтра с помощью Selenium и BeautifulSoup.
- **db.py**: управление SQLite-базой weather.db (создание таблиц, добавление и удаление записей).
- **parser.py**: парсинг HTML-страниц с сайта Gismeteo для получения текущей и прогнозной температуры.
- **analize.py**: визуализация собранных данных по дате (формат dd.mm.yyyy) с помощью Pandas и Matplotlib.
## Структура проекта
├── main.py                # Точка входа для сбора данных\
├── parser.py	# Логика парсинга текущей и прогнозной температуры\
├── db.py                  # Работа с локальной SQLite-базой\
├── analize.py             # Скрипт для визуализации данных за выбранную дату\
├── settings.json          # Настройки: список городов и URL для парсинга\
├── weather.db             # SQLite-база (создаётся автоматически)\
└── requirements.txt       # Список зависимостей для pip
## Установка и запуск
1. **Клонирование репозитория**

   `        `git clone https://github.com/ydhs/Scrapper1.git\
   cd Scraper1
2. **Создайте и активируйте виртуальное окружение**

   python -m venv .venv\
   # Windows PowerShell\
   .\.venv\Scripts\Activate.ps1\
   # Linux/macOS\
   source .venv/bin/activate
3. **Установка зависимостей**

   pip install -r requirements.txt
4. **Настройка settings.json**\
   В файле settings.json укажите список городов и соответствующие URL для текущей температуры и страницы с прогнозами.
4. **Запуск сбора данных**

   python main.py

   После этого в корне появится база weather.db с таблицами.
6. **Визуализация данных**

   python analize.py 21.05.2025

   Скрипт отобразит график текущей и прогнозной температур за указанную дату.
## Описание базы данных
Используется простая SQLite-база weather.db, состоит из трёх таблиц:

- cities:
  - id — уникальный идентификатор города
  - name — название города
  - url — URL для парсинга данных
- current\_temperature:
  - id — уникальный идентификатор записи
  - city\_id — ссылка на cities.id
  - temperature — значение текущей температуры
  - timestamp — время сбора
- forecast\_temperature:
  - id — уникальный идентификатор записи
  - city\_id — ссылка на cities.id
  - timestamp — время прогноза
  - temperature — прогнозная температура

Каждая запись в таблицах current\_temperature и forecast\_temperature связана с городом из таблицы cities.
## Зависимости
- Python 3.x
- selenium
- beautifulsoup4
- pandas
- matplotlib
