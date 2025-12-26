#gnss_worker.py
"""This module contains the GnssWorker class, responsible for starting the managing QThreads - main task: fetching GPS data."""
from PyQt5.QtCore import QThread, pyqtSignal
import platform
class GnssWorker(QThread):
    def __init__(self):
        super().__init__()
        self._running = True

    runningStatus = pyqtSignal(bool)
    latitude = pyqtSignal(float)
    longitude = pyqtSignal(float)
    altitude = pyqtSignal(str)
    gpsFix = pyqtSignal(str)
    satelitesNumber = pyqtSignal(str)
    speed = pyqtSignal(str)
    heading = pyqtSignal(str)

    error = pyqtSignal(str)

    def run(self):
        print("GPS_WORKER STARTED")
        if not platform.system() == 'Linux':
            return
        
        # Import this only on linux, fixes tests issues
        from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE

        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

        try:
            while self._running:
                report = session.next()
                self.runningStatus.emit(True)

                if report['class'] =='TPV':
                    if hasattr(report,'lat'):
                        self.latitude.emit(float(report.lat))
                        
                    if hasattr(report,'lon'):
                        self.longitude.emit(float(report.lon))

                    if hasattr(report,'alt'):
                        self.altitude.emit(f"{report.alt:.6f}")
                    
                    if hasattr(report,'speed'):
                        self.speed.emit(f"{report.speed:.6f}")

                    if hasattr(report, 'mode'):
                        self.gpsFix.emit(str(report.mode))
                    
                    if hasattr(report, 'track'):
                        self.heading.emit(f"{report.track:.2f}")
                
                if report['class'] == 'SKY':
                    if hasattr(report, 'satellites'):
                        self.satelitesNumber.emit(str(len(report.satellites)))

        except Exception as e:
            print(f"GnssWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self.runningStatus.emit(False)
        self._running = False