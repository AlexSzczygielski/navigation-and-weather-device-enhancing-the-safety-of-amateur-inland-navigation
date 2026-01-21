#gnss_worker.py
""""""
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import logging
import time
from datetime import datetime

from weather_module.weather_data import WeatherData
import config
from app import json_manager

logger = logging.getLogger(__name__)

class WeatherWorker(QThread):
    def __init__(self, weather_data: WeatherData, lat:float, lon:float):
        super().__init__()
        self.weather_data = weather_data
        self._running = True
        self._lat = lat
        self._lon = lon

    error = pyqtSignal(str)

    def run(self):
        logger.info("WEATHER_WORKER STARTED")
        try:
            if self._lat is None:
                data = json_manager.load_json(config.LAST_SESSION_POSITION_PATH)
                self._lat = data["latitude"]

            if self._lon is None:
                data = json_manager.load_json(config.LAST_SESSION_POSITION_PATH)
                self._lon = data["longitude"]

            if self._lat is None or self._lon is None:
                raise ValueError("WeatherWorker: latitude or longitude is None")
             
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={self._lat}&lon={self._lon}&units=metric&appid={config.OPEN_WEATHER_API_KEY}"
            response = requests.get(url, timeout=10)

            #Get timestamp
            fetch_timestamp = time.time()
            fetch_timestamp = round(fetch_timestamp, 0)
            self.weather_data.fetch_timestamp = str(datetime.fromtimestamp(fetch_timestamp))
            
            data = response.json()
            self.weather_data.message = str(data["message"])

            city = data["city"]
            self.weather_data.city_name = city["name"]
            self.weather_data.country = city["country"]
            self.weather_data.lat = city["coord"]["lat"]
            self.weather_data.lon = city["coord"]["lon"]
            self.weather_data.timezone = city["timezone"]

            current = data["list"][0]

            self.weather_data.current_temp = current["main"]["temp"]
            self.weather_data.current_feels_like = current["main"]["feels_like"]
            self.weather_data.current_humidity = current["main"]["humidity"]
            self.weather_data.current_condition = current["weather"][0]["description"]
            self.weather_data.current_wind = current["wind"]["speed"]

            forecast_list = []

            for entry in data["list"]:
                forecast_list.append({
                    "dt": entry["dt"],
                    "dt_txt": entry["dt_txt"],
                    "temp": entry["main"]["temp"],
                    "feels_like": entry["main"]["feels_like"],
                    "humidity": entry["main"]["humidity"],
                    "condition": entry["weather"][0]["description"],
                    "wind": entry["wind"]["speed"],
                    "wind_deg": entry["wind"]["deg"],
                    "wind_gust": entry["wind"]["gust"]
                })

            self.weather_data.forecast = forecast_list

        except Exception as e:
            logger.error(f"WeatherWorker failure: {e}")
            self.error.emit(str(e))
    
    
    def stop(self):
        self.weather_data.runningStatus=False
        self._running = False
        logging.info("WEATHER WORKER STOPPED")