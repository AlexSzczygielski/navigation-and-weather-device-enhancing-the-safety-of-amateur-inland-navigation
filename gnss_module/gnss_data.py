#gnss_data.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
import math

class GnssData(QObject):
    def __init__(self):
        super().__init__()
        self._latitude = float('nan')
    
    # Update signals - notify QML frontend about new data
    latitudeChanged = pyqtSignal(float)

    # Getters used by QML frontend
    @pyqtProperty(float, notify=latitudeChanged)
    def latitude(self):
        return self._latitude
    
    #Setters - emit update signals for QML frontend
    @latitude.setter
    def latitude(self, newValue):
        if self._latitude != newValue:
            self._latitude = newValue
            self.latitudeChanged.emit(newValue)