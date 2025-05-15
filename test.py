from prefect import flow

@flow
def weather_collection_flow():
    print("Поток запущен и работает!")