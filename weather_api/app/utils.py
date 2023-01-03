import json
from weather_api.app import settings
from weather_api.app.db import WeatherData
from logging import getLogger
import requests
from pony.orm import db_session, select


logger = getLogger(__name__)


def get_city_ids():
    with open(settings.CITIES_FILE) as f:
        return json.load(f)["cities"]


ALL_CITY_IDS = get_city_ids()
# ALL_CITY_IDS = [3439525, 3439781, 3440645]


@db_session
def call_weather_api(session, city_id, request_id):
    query_params = {
        "id": city_id,
        "appid": settings.API_KEY,
        "units": "metric",
    }
    with session.get(settings.OPEN_WEATHER_BASE_URL, params=query_params) as r:
        r = r.json()
        data = {
            "city_id": city_id,
            "temp": r["main"]["temp"],
            "humidity": r["main"]["humidity"],
        }
        WeatherData(
            request_id=request_id,
            city_id=city_id,
            data=data,
        )


def collect_weather_data(request_id):
    with requests.Session() as session:
        retries = requests.adapters.Retry(total=4, backoff_factor=5)
        session.mount("https://", requests.adapters.HTTPAdapter(max_retries=retries))
        for city_id in ALL_CITY_IDS:
            call_weather_api(session, city_id, request_id)


@db_session
def request_id_exists(request_id):
    return request_id in select(wd.request_id for wd in WeatherData)


@db_session
def get_percentage_done(request_id):
    cities_done = select(wd for wd in WeatherData if wd.request_id == request_id).count()
    percentage = 100 * cities_done / len(ALL_CITY_IDS)
    return percentage
