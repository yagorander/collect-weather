from fastapi.testclient import TestClient
from weather_api.app.main import app


client = TestClient(app)


def test_all_cities(open_weather_response):
    response = client.post("/all_cities", json={"request_id": 0})
    assert response.status_code == 200


def test_progress(open_weather_response):
    _ = client.post("/all_cities", json={"request_id": 0})
    response = client.get("/progress/0")
    assert response.status_code == 200
    assert response.json() == {"percentage": "100.00%"}
