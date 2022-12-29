from pony.orm import Required, Json, PrimaryKey

from datetime import datetime
from pony.orm import Database


db = Database()

class WeatherData(db.Entity):
    request_id = Required(int)
    city_id = Required(int)
    timestamp = Required(datetime, default=datetime.utcnow)
    data = Required(Json)
    PrimaryKey(request_id, city_id)

db.bind(provider="postgres", user="postgres", password="postgres", host="postgres", database="weather", port=5432)
db.generate_mapping(create_tables=True)