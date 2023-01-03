from os import getenv

CITIES_FILE = getenv("CITIES_FILE", "weather_api/data/all_city_ids.json")
API_KEY = getenv("API_KEY", "80908a3187dec5ccda923e7d9b1463dd")
OPEN_WEATHER_BASE_URL = getenv("OPEN_WEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5/weather")
CHUNK_SIZE = int(getenv("CHUNK_SIZE", 10))
