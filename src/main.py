from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from weather_service import WeatherService

load_dotenv()

app = FastAPI()
client = MongoClient(os.getenv("MONGODB_URL"))
db = client.weather_db
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
weather_service = WeatherService(db, openweather_api_key)

@app.get("/forecast/{city}")
def get_forecast(city: str):
    return weather_service.get_forecast(city)
