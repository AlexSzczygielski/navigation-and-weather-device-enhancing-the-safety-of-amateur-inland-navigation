#gps_backend.py
"""This module contains the GpsBackend class responsible for managing backend of the GPS components."""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl
from gps_module.gps_worker import GpsWorker

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

    error = pyqtSignal(str)

    @pyqtSlot()
    def start_gps_worker(self):
        try:
            #Ensure old worker is cleaned up
            if self._worker and self._worker.isRunning():
                print("Previous worker still running")
                return
            
            self._worker = GpsWorker()
            self._worker.latitude.connect(self.latitudeUpdated)
            self._worker.finished.connect(self._on_start_gps_worker_finished)
            self._worker.error.connect(self._on_run_cv_roi_pipe_error)
            self._worker.finished.connect(self._worker.deleteLater)
            self._worker.start()

        except Exception as e:
            print(f"{self.__class__.__name__}.start_gps_worker error: {e}")

    def _on_start_gps_worker_finished(self):
        """Handles end of the task."""
        self._worker = None #Release the reference

    def _on_start_gps_worker_error(self):
        """Emits error GUI."""
        print("error")