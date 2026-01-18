#weather_backend.py
""""""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
import logging

from weather_module.weather_data import WeatherData
from weather_module.weather_worker import WeatherWorker

logger = logging.getLogger(__name__)

class WeatherBackend(QObject):
    def __init__(self):
        super().__init__()
        self._weather_worker = None
        self._weather_data = WeatherData()

    def shutdown(self):
        "Terminate all workers at appliaction close triggered by GUI."
        if self._weather_worker:
            self._weather_worker.stop()
            self._weather_worker.quit()
            self._weather_worker.wait()
            print("shutdown called")
        self._weather_worker = None

    #Possible signals
    @pyqtProperty(QObject, constant=True)
    def weather_data(self):
        return self._weather_data
    
    @pyqtSlot()
    def start_weather_worker(self):
        try:
            #Ensure old worker is cleaned up
            if self._weather_worker and self._weather_worker.isRunning():
                print("Previous worker still running")
                return
            
            self._weather_worker = WeatherWorker(weather_data=self.weather_data)
            self._weather_worker.error.connect(self._on_weather_worker_error)
            self._weather_worker.finished.connect(self._on_weather_worker_finished)
            self._weather_worker.finished.connect(self._weather_worker.deleteLater)
            self._weather_worker.start()
        
        except Exception as e:
            print(f"{self.__class__.__name__}.start_weather_worker error: {e}")
        
    
    def _on_weather_worker_finished(self):
        self._weather_worker = None

    def _on_weather_worker_error(self, msg):
        print("WeatherWorker error:", msg)