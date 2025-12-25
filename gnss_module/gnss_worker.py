#gps_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
import platform
class GpsWorker(QThread):
    def __init__(self):
        super().__init__()
        self._running = True

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

        session = gps(mode=gps.WATCH_ENABLE | WATCH_NEWSTYLE)

        try:
            while self._running:
                report = session.next()

                if report['class'] =='TPV':
                    if hasattr(report,'lat'):
                        print("Lat:", report.lat)
                        self.latitude.emit(f"{report.lat:.6f}")

        except Exception as e:
            print(f"GpsWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self._running = False