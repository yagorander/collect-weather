import pytest

from fastapi.testclient import TestClient
from weather_api.app import utils
from pony.orm import db_session
from aiohttp_retry import RetryClient
from weather_api.app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def open_weather_response(monkeypatch):
    class Response:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args, **kwargs):
            pass

        @staticmethod
        async def json():
            return {"main": {"temp": 10, "humidity": 20}}

    monkeypatch.setattr(RetryClient, "get", Response)


@pytest.fixture(autouse=True)
def clean_db():
    with db_session:
        utils.WeatherData.select().delete()
