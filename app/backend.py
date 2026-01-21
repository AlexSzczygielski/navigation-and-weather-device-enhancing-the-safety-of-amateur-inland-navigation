#backend.py
"""This module contains Backend class - wrapper of all backends used in this app."""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl
import logging

from app.cv_backend import CvBackend
from app.gnss_backend import GnssBackend
from app.weather_backend import WeatherBackend

logger = logging.getLogger(__name__)

class Backend(QObject):
    """
    Backend - a wrapper class composed of all service backends used in an app.

    It is created by passing ready to use backend objects.
    There is a file factories.py containing construction functions
    for all service backends as well as this backend."
    """
    def __init__(self, CvBackend: CvBackend, GnssBackend: GnssBackend, WeatherBackend: WeatherBackend):
        super().__init__()
        self.cv = CvBackend
        self.gps = GnssBackend
        self.weather_backend = WeatherBackend

    @pyqtSlot()
    def shutdown_all(self):
        logger.info("Shutting down application...")
        self.cv.shutdown()
        self.gps.shutdown()
        self.weather_backend.shutdown()