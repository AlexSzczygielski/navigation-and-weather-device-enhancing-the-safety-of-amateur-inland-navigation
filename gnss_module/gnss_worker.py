#gnss_worker.py
"""This module contains the GnssWorker class, responsible for starting the managing QThreads - main task: fetching GPS data."""
from PyQt5.QtCore import QThread, pyqtSignal
import platform
from gnss_module.gnss_data import GnssData

class GnssWorker(QThread):
    def __init__(self, gnss_data):
        super().__init__()
        self.gnss_data = gnss_data
        self._running = True

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
                self.gnss_data.runningStatus = True

                if report['class'] =='TPV':
                    if hasattr(report,'lat'):
                        self.gnss_data.latitude = float(report.lat)
                        
                    if hasattr(report,'lon'):
                        self.gnss_data.longitude=float(report.lon)

                    if hasattr(report,'alt'):
                        self.gnss_data.altitude=float(report.alt)
                    
                    if hasattr(report,'speed'):
                        self.gnss_data.speed=float(report.speed)

                    if hasattr(report, 'mode'):
                        self.gnss_data.gpsFix=str(report.mode)
                    
                    if hasattr(report, 'track'):
                        self.gnss_data.heading=float(report.track)
                
                if report['class'] == 'SKY':
                    if hasattr(report, 'satellites'):
                        self.gnss_data.satellitesNumber=len(report.satellites)
                        print("sats: ", report.satellites)

        except Exception as e:
            print(f"GnssWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self.gnss_data.runningStatus=False
        self._running = False