from fastapi import FastAPI
from weather_api.app.utils import request_id_exists, collect_weather_data, get_percentage_done
from pydantic import BaseModel, validator


app = FastAPI()


class PostPayload(BaseModel):
    request_id: int

    @validator("request_id")
    def is_request_id_unique(cls, v):
        if request_id_exists(v):
            raise ValueError("request_id already exists")
        return v

@app.post("/all_cities")
def get_all_cities(payload: PostPayload):
    collect_weather_data(payload.request_id)
    return {"message": "request accepted"}

@app.get("/progress/{request_id}")
def get_progress(request_id: int):
    if not request_id_exists(request_id):
        return {"message": "request_id not found"}
    percentage = get_percentage_done(request_id)
    return {"percentage": f"{percentage:.2f}%"}