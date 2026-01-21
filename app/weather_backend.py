#weather_backend.py
""""""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
import logging

from weather_module.weather_data import WeatherData
from weather_module.weather_worker import WeatherWorker
from app.gnss_backend import GnssBackend

logger = logging.getLogger(__name__)

class WeatherBackend(QObject):
    def __init__(self, gnss_backend: GnssBackend):
        super().__init__()
        self._weather_worker = None
        self._weather_data = WeatherData()
        self._gnss_backend = gnss_backend # Reference to GNSS Backend

    def shutdown(self):
        "Terminate all workers at appliaction close triggered by GUI."
        if self._weather_worker:
            self._weather_worker.stop()
            self._weather_worker.quit()
            self._weather_worker.wait()
            logger.info("shutdown called")
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
                logger.warning("Previous worker still running")
                return
            lat, lon = self._gnss_backend.get_last_position()
            self._weather_worker = WeatherWorker(weather_data=self.weather_data,lat=lat,lon=lon)
            self._weather_worker.error.connect(self._on_weather_worker_error)
            self._weather_worker.finished.connect(self._on_weather_worker_finished)
            self._weather_worker.finished.connect(self._weather_worker.deleteLater)
            self._weather_worker.start()
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.start_weather_worker error: {e}")
        
    
    def _on_weather_worker_finished(self):
        self._weather_worker = None

    def _on_weather_worker_error(self, msg):
        logger.error("WeatherWorker error:", msg)