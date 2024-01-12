import unittest
from unittest.mock import MagicMock
from unittest import mock
from datetime import datetime, timedelta
from src.weather_service import WeatherService

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.openweather_api_key = "your_api_key"
        self.weather_service = WeatherService(self.db, self.openweather_api_key)

    def test_get_forecast_existing_data(self):
        city = "London"
        start_date, end_date = self.weather_service.get_date_range()

        self.weather_service.fetch_forecast_from_db = MagicMock(return_value=[{"dt": datetime.now().timestamp()}])

        forecast = self.weather_service.get_forecast(city)

        self.assertEqual(str(forecast["daily"][0]["dt"]).split(".")[0], str(datetime.now().timestamp()).split(".")[0])
        self.weather_service.fetch_forecast_from_db.assert_called_once_with(city, start_date, end_date)

    def test_get_forecast_new_data(self):
        city = "London"
        start_date, end_date = self.weather_service.get_date_range()
        timestamp = datetime.now().timestamp()

        self.weather_service.get_lat_lon = MagicMock(return_value=(51.5074, -0.1278))
        self.weather_service.fetch_forecast_from_db = MagicMock(return_value=None)
        self.weather_service.fetch_and_update_forecast = MagicMock(return_value=[{"dt": timestamp}])

        forecast = self.weather_service.get_forecast(city)

        self.assertEqual(forecast["daily"], [{"dt": timestamp}])
        self.weather_service.fetch_and_update_forecast.assert_called_once_with(city, 51.5074, -0.1278, start_date, end_date)

if __name__ == "__main__":
    unittest.main()