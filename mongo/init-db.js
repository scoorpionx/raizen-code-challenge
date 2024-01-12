// init-db.js
db = db.getSiblingDB('weather_db');
db.createCollection('forecasts');
