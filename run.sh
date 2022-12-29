{ 
    uvicorn weather_api.app.main:app --reload --host 0.0.0.0 --port 8000 & \
    rq worker --with-scheduler -u redis://redis:6379; 
}
