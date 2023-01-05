# collect-weather
Simple API that collects weather data from Open Weather API asynchronously

## How to run
First build with `docker-compose build` and then simply run `docker-compose up` and the Swagger UI will be available at `http://localhost:8000/docs`. This will start two containers:
- `weather_api` - The API
- `postgres` - The database


The API has two endpoints:

- POST `/all_cities`

    Request body:
    ```json
    {"request_id": 1}   
    ``` 
    Collects current weather data for all city IDs listed in `weather_api/data/all_city_ids.json` and saves it to the database. The request ID is used to track the progress of the data collection.


- GET `/progress/<request_id:int>`:

    Returns the progress of the data collection

## How to run tests
Run `docker-compose exec bash run_tests.sh`


## About the project
The project is built using FastAPI and aiohttp-retry. FastAPI provides easy input validation, swagger UI and background tasks out of the box. aiohttp-retry is used to make concurrent requests to the Open Weather API and retry on failure. The database is Postgres and is managed by PonyORM.

There are two other branches in this repo with different approaches to the problem:
- `using-rq`: Uses Redis and RQ (Redis Queue) to enqueue the requests to the Open Weather API. The requests are retried on failure using RQ's built-in retry mechanism.
- `just-requests`: Using FastAPI background tasks and plain requests. (This one is more for comparison with the other two branches)