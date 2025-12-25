#gnss_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
import platform
class GpsWorker(QThread):
    def __init__(self):
        super().__init__()
        self._running = True

    runningStatus = pyqtSignal(bool)
    latitude = pyqtSignal(str)
    longitude = pyqtSignal(str)
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
                        self.latitude.emit(f"{report.lat:.6f}")
                        
                    if hasattr(report,'lon'):
                        self.longitude.emit(f"{report.lon:.6f}")

                    if hasattr(report,'alt'):
                        self.altitude.emit(f"{report.alt:.6f}")
                    
                    if hasattr(report,'speed'):
                        self.speed.emit(f"{report.speed:.6f}")

                    if hasattr(report, 'mode'):
                        self.gpsFix.emit(str(report.mode))
                    
                    if hasattr(report, 'satellites'):
                        self.satelitesNumber.emit(str(len(report.satellites)))
                    
                    if hasattr(report, 'track'):
                        self.heading.emit(f"{report.track:.2f}")

        except Exception as e:
            print(f"GnssWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self.runningStatus.emit(False)
        self._running = False