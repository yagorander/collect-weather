import json
import requests
from rq import Retry
from weather_api.app import settings
from weather_api.app.db import WeatherData
from redis import Redis
from rq import Queue
from pony.orm import db_session, select
from logging import getLogger
import sys


# sys.tracebacklimit = 0


logger = getLogger(__name__)
redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
queue = Queue(connection=redis_conn)


def get_city_ids():
    with open(settings.CITIES_FILE) as f:
        return json.load(f)["cities"]


ALL_CITY_IDS = get_city_ids()
# ALL_CITY_IDS = [3439525, 3439781, 3440645]


@db_session
def call_weather_api(city_id, request_id):
    query_params = {
        "id": city_id,
        "appid": settings.API_KEY,
        "units": "metric",
    }
    r = requests.get(settings.OPEN_WEATHER_BASE_URL, params=query_params)
    r.raise_for_status()
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
    city_ids = ALL_CITY_IDS
    for city_id in city_ids:
        queue.enqueue(
            call_weather_api,
            city_id,
            request_id,
            retry=Retry(max=3, interval=10),
        )


@db_session
def request_id_exists(request_id):
    return request_id in select(wd.request_id for wd in WeatherData)

@db_session
def get_percentage_done(request_id):
    cities_done = select(wd for wd in WeatherData if wd.request_id == request_id).count()
    percentage = 100 * cities_done / len(ALL_CITY_IDS)
    return percentage
