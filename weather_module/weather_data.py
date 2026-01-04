#weather_module.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class WeatherData(QObject):
    def __init__(self):
        super().__init__()
        self.runningStatus = False
        # weather_worker