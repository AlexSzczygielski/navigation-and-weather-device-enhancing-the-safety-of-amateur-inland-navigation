#map_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
import logging

from gnss_module.map_service import MapService
from gnss_module.gnss_data import GnssData
import config

logger = logging.getLogger(__name__)

class MapWorker(QThread):
    def __init__(self, gnss_data: GnssData, new_latitude, new_longitude, zoom=config.MAP_STANDARD_ZOOM):
        super().__init__()
        self._running = True
        self._gnss_data = gnss_data
        self._new_latitude = new_latitude
        self._new_longitude = new_longitude
        self._zoom = zoom

    
    error = pyqtSignal(str)

    def run(self):
        logger.info("MAP_WORKER Started")
        try:
            map_service = MapService(
                zoom=self._zoom,
                latitude=self._new_latitude,
                longitude=self._new_longitude
            )

            ready_map = "data:image/png;base64," + map_service.render_map()

            if ready_map:
                self._gnss_data.newMap = ready_map
                self._gnss_data.zoom = self._zoom

        except Exception as e:
            logger.error(f"MapWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self._running = False