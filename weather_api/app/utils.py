import json
from weather_api.app import settings
from weather_api.app.db import WeatherData
from logging import getLogger
import asyncio
import aiohttp_retry
from pony.orm import db_session, select
from time import sleep


logger = getLogger(__name__)


def get_city_ids():
    with open(settings.CITIES_FILE) as f:
        return json.load(f)["cities"]


ALL_CITY_IDS = get_city_ids()
# ALL_CITY_IDS = [3439525, 3439781, 3440645]


@db_session
async def call_weather_api(retry_client, city_id, request_id):
    query_params = {
        "id": city_id,
        "appid": settings.API_KEY,
        "units": "metric",
    }
    async with retry_client.get(settings.OPEN_WEATHER_BASE_URL, params=query_params) as r:
        r = await r.json()
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


async def collect_weather_data(request_id):
    retry_options = aiohttp_retry.ListRetry([10, 20, 30])
    async with aiohttp_retry.RetryClient(retry_options=retry_options) as retry_client:
        for city_id in ALL_CITY_IDS:
            await call_weather_api(retry_client, city_id, request_id)


@db_session
def request_id_exists(request_id):
    return request_id in select(wd.request_id for wd in WeatherData)


@db_session
def get_percentage_done(request_id):
    cities_done = select(wd for wd in WeatherData if wd.request_id == request_id).count()
    percentage = 100 * cities_done / len(ALL_CITY_IDS)
    return percentage