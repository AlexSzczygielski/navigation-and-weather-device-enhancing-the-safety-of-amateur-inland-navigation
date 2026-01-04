#gnss_worker.py
""""""
from PyQt5.QtCore import QThread, pyqtSignal

from weather_module.weather_data import WeatherData

class WeatherWorker(QThread):
    def __init__(self, weather_data: WeatherData):
        super().__init__()
        self.weather_data = weather_data
        self._running = True

    error = pyqtSignal(str)

    def run(self):
        try:
            print("WEATHER_WORKER STARTED")
        
        except Exception as e:
            print(f"WeatherWorker failure: {e}")
            self.error.emit(str(e))
    
    
    def stop(self):
        self.weather_data.runningStatus=False
        self._running = False