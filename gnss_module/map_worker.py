#map_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
from staticmap import StaticMap, CircleMarker, tile_provider
import os

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
            #Chcek if the cache folder exists, if not create it
            os.makedirs(self.cache_folder, exist_ok=True)

            # Configure map tile provider for staticmap
            provider = tile_provider.OSM()
            provider.tile_cache = self.cache_folder

            # Configure static map
            m = StaticMap(config.MAP_WIDTH,config.MAP_HEIGHT, tile_provider=provider)
            mark = CircleMarker(
                coord=(self._new_longitude, self._new_latitude),
                color='red',
                width=12
            )
            m.add_marker(marker=mark)

            # Render map
            image = m.render(zoom=self._zoom)

            #Save new map tile and emit filepath
            image.save(self._map_tile_path)
            self.mapReady.emit(self._map_tile_path)

        except Exception as e:
            print(f"MapWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self._running = False