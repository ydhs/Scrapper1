from flow import weather_collection_flow

if __name__ == '__main__':
    weather_collection_flow.serve(name="weather-deployment")


from flow import weather_collection_flow

if __name__ == "__main__":
    # Регистрирует и запускает поток
    weather_collection_flow.serve(
        name="weather-flow",
        cron="0 */1 * * *",  # запуск каждые час (UTC)
    )