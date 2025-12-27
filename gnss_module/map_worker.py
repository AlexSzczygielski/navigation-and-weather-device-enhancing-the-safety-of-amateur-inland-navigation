#map_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
from gnss_module.map_service import MapService

import config

class MapWorker(QThread):
    def __init__(self, new_latitude, new_longitude, zoom=config.MAP_STANDARD_ZOOM):
        super().__init__()
        self._running = True
        self._new_latitude = new_latitude
        self._new_longitude = new_longitude
        self._map_tile_path = "data/map_tiles/temp_map.png"
        self._zoom = zoom

    mapReady = pyqtSignal(str)
    error = pyqtSignal(str)

    cache_folder = "data/map_tiles/osm_map_tiles_cache"

    def run(self):
        print("MAP_WORKER STARTED")
        try:
            map_service = MapService(
                zoom=self._zoom,
                latitude=self._new_latitude,
                longitude=self._new_longitude
            )

            ready_map = map_service.render_map()
            if ready_map:
                self.mapReady.emit(ready_map)

        except Exception as e:
            print(f"MapWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self._running = False