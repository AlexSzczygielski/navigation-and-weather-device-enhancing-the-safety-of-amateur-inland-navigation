#gnss_data.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

import config

class GnssData(QObject):
    def __init__(self):
        super().__init__()
        # gnss_worker
        self._latitude = float('nan')
        self._longitude = float('nan')
        self._altitude = float('nan')
        self._speed = float('nan')
        self._heading = float('nan')
        
        self._satellitesNumber = "None"
        self._runningStatus = False
        self._gpsFix = "None"

        # map_worker
        self._newMap = ""
        self._zoom = config.MAP_STANDARD_ZOOM
    
    # --- Update signals - notify QML frontend about new data ---
    # gnss_worker
    latitudeChanged = pyqtSignal(float)
    longitudeChanged = pyqtSignal(float)
    altitudeChanged = pyqtSignal(float)
    speedChanged = pyqtSignal(float)
    headingChanged = pyqtSignal(float)

    runningStatusChanged = pyqtSignal(bool)
    satellitesNumberChanged = pyqtSignal(str)
    gpsFixChanged = pyqtSignal(str)

    # map_worker
    newMapChanged = pyqtSignal(str)
    zoomChanged = pyqtSignal(int)

    # Possible signals Map Configuration
    mapWidthChanged = pyqtSignal()
    mapHeightChanged = pyqtSignal()

    
    # ---

    # --- Properties - getters and setters used by QML frontend
    # gnss_worker
    @pyqtProperty(float, notify=latitudeChanged)
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if self._latitude != value:
            self._latitude = value
            self.latitudeChanged.emit(self._latitude)

    @pyqtProperty(float, notify=longitudeChanged)
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if self._longitude != value:
            self._longitude = value
            self.longitudeChanged.emit(self._longitude)

    @pyqtProperty(float, notify=altitudeChanged)
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        if self._altitude != value:
            self._altitude = value
            self.altitudeChanged.emit(self._altitude)

    @pyqtProperty(float, notify=speedChanged)
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if self._speed != value:
            self._speed = value
            self.speedChanged.emit(self._speed)

    @pyqtProperty(float, notify=headingChanged)
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        if self._heading != value:
            self._heading = value
            self.headingChanged.emit(self._heading)

    @pyqtProperty(bool, notify=runningStatusChanged)
    def runningStatus(self):
        return self._runningStatus

    @runningStatus.setter
    def runningStatus(self, value):
        if self._runningStatus != value:
            self._runningStatus = value
            self.runningStatusChanged.emit(self._runningStatus)

    @pyqtProperty(str, notify=gpsFixChanged)
    def gpsFix(self):
        return self._gpsFix

    @gpsFix.setter
    def gpsFix(self, value):
        if self._gpsFix != value:
            self._gpsFix = value
            self.gpsFixChanged.emit(self._gpsFix)

    @pyqtProperty(str, notify=satellitesNumberChanged)
    def satellitesNumber(self):
        return self._satellitesNumber

    @satellitesNumber.setter
    def satellitesNumber(self, value):
        if self._satellitesNumber != value:
            self._satellitesNumber = value
            self.satellitesNumberChanged.emit(self._satellitesNumber)
    
    # map_worker
    @pyqtProperty(str, notify=newMapChanged)
    def newMap(self):
        return self._newMap
    
    @newMap.setter
    def newMap(self,value):
        if self._newMap != value:
            self._newMap = value
            self.newMapChanged.emit(self._newMap)

    @pyqtProperty(int, notify=zoomChanged)
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self,value):
        if self._zoom != value:
            self._zoom = value
            self.zoomChanged.emit(self._zoom)

    ### MAP CONFIG ###
    @pyqtProperty(int, notify=mapWidthChanged)
    def map_width(self):
        return config.MAP_WIDTH
    
    @pyqtProperty(int, notify=mapHeightChanged)
    def map_height(self):
        return config.MAP_HEIGHT