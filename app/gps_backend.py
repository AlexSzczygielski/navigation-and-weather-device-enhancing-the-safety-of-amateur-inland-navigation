#gps_backend.py
"""This module contains the GpsBackend class responsible for managing backend of the GPS components."""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl

class GpsBackend(QObject):
    def __init__(self):
        super().__init__()
        self._worker = None

    def shutdown(self):
        "Terminate all GpsWorkers at appliaction close triggered by GUI."
        if self._worker:
            self._worker.stop()
            self._worker.quit()
            self._worker.wait()
            print("shutdown called")
        self._worker = None

    #Possible signals
    latitudeUpdated = pyqtSignal(str)
    longitudeUpdated = pyqtSignal(str)
    altitudeUpdated = pyqtSignal(str)
    gpsFixUpdated = pyqtSignal(str)
    satelitesNumberUpdated = pyqtSignal(str)
    speedUpdated = pyqtSignal(str)
    headingUpdated = pyqtSignal(str)