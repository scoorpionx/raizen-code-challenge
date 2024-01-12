import requests
from datetime import datetime, timedelta
from pymongo import UpdateOne

class WeatherService:
    def __init__(self, db, openweather_api_key):
        self.db = db
        self.openweather_api_key = openweather_api_key
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.onecall_url = "https://api.openweathermap.org/data/3.0/onecall"

    def get_lat_lon(self, city):
        """
        Obtém latitude e longitude para uma cidade usando a API de geocodificação.
        """
        response = requests.get(f"{self.geocoding_url}?q={city}&limit=1&appid={self.openweather_api_key}")
        geocode_data = response.json()
        print(geocode_data)
        if not geocode_data:
            return None, None
        return geocode_data[0]["lat"], geocode_data[0]["lon"]

    def get_forecast(self, city):
        """
        Obtém a previsão do tempo para os próximos 5 dias para a cidade especificada.
        """
        start_date, end_date = self.get_date_range()
        forecasts = self.fetch_forecast_from_db(city, start_date, end_date)

        if not forecasts:
            lat, lon = self.get_lat_lon(city)
            # lat, lon = 51.5156177, -0.0919983
            if lat is None or lon is None:
                return {"error": "Localização não encontrada"}

            forecasts = self.fetch_and_update_forecast(city, lat, lon, start_date, end_date)

        return {"daily": forecasts}

    def get_date_range(self):
        current_time = datetime.now()
        start_date = current_time.date()
        end_date = start_date + timedelta(days=5)
        return start_date, end_date

    def fetch_forecast_from_db(self, city, start_date, end_date):
        """
        Busca previsões existentes no banco de dados.
        """
        current_time = datetime.now()
        forecasts = self.db.forecasts.find_one({"city": city})

        if not forecasts:
            self.db.forecasts.insert_one({"city": city, "data": [], "last_updated": datetime.now()})
            return []
        
        if forecasts:
            start_timestamp = datetime.combine(start_date, datetime.min.time()).timestamp()
            end_timestamp = datetime.combine(end_date, datetime.min.time()).timestamp()

            filtered_data = [forecast for forecast in forecasts['data'] if start_timestamp <= forecast['dt'] < end_timestamp]
            return filtered_data
        
        return []

    def fetch_and_update_forecast(self, city, lat, lon, start_date, end_date):
        """
        Busca a previsão do tempo da API e atualiza o banco de dados.
        """
        response = requests.get(f"{self.onecall_url}?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={self.openweather_api_key}")
        if response.status_code != 200:
            return {"error": "Erro ao acessar a API do OpenWeatherMap"}

        data = response.json()
        return self.update_forecast_in_db(city, data, start_date, end_date)

    def update_forecast_in_db(self, city, data, start_date, end_date):
        """
        Atualiza o banco de dados com a nova previsão e retorna os dados filtrados.
        """
        filtered_data = []

        for day_forecast in data['daily']:
            forecast_date = datetime.fromtimestamp(day_forecast['dt']).date()

            if start_date <= forecast_date < end_date:
                filtered_data.append(day_forecast)

        if data['daily']:
            self.db.forecasts.update_one({"city": city}, {"$set": {"data": data['daily'], "last_updated": datetime.now()}})


        return filtered_data
