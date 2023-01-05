import pytest
from weather_api.app import utils
from weather_api.app.db import WeatherData
from pony.orm import db_session
from aiohttp_retry import RetryClient


def test_get_city_ids():
    assert utils.get_city_ids() == [3439525, 3439781, 3440645]


@pytest.mark.asyncio
async def test_call_weather_api(open_weather_response):
    async with RetryClient() as session:
        await utils.call_weather_api(session, 3439525, 0)
    with db_session:
        assert WeatherData.select(request_id=0).count() == 1


@pytest.mark.asyncio
async def test_collect_weather_data(open_weather_response):
    await utils.collect_weather_data(1)
    with db_session:
        assert WeatherData.select(request_id=1).count() == 3
        stored_city_ids = [wd.city_id for wd in WeatherData.select(request_id=1)]
        assert stored_city_ids == [3439525, 3439781, 3440645]


@pytest.mark.asyncio
async def test_request_id_exists(open_weather_response):
    await utils.collect_weather_data(2)
    assert utils.request_id_exists(2) is True
    assert utils.request_id_exists(3) is False


@pytest.mark.asyncio
async def test_get_percentage_done(open_weather_response):
    await utils.collect_weather_data(4)
    assert utils.get_percentage_done(4) == 100
