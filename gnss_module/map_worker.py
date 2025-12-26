#map_worker.py

from PyQt5.QtCore import QThread, pyqtSignal
from staticmap import StaticMap, CircleMarker
import os

import config

class MapWorker(QThread):
    def __init__(self, new_latitude, new_longitude):
        super().__init__()
        self._running = True
        self._new_latitude = new_latitude
        self._new_longitude = new_longitude
        self._out_path = None

    mapReady = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        print("MAP_WORKER STARTED")
        try:
            # Create outpath - add logic checking for correct coords map naming here - map_lon_lat_width_height_zoom.png - or save this in metadata? #TODO
            # This is dummy for tests
            self._out_path = "data/map_tiles/output.png"

            # If map already exists, emit it, else fetch new tile from api
            if os.path.exists(self._out_path):
                self.mapReady.emit(self._out_path)
            else:
                m = StaticMap(config.MAP_WIDTH,config.MAP_HEIGHT)
                mark = CircleMarker(
                    coord=(self._new_longitude, self._new_latitude),
                    color='red',
                    width=12
                )
                m.add_marker(marker=mark)

                image = m.render(zoom=15)
                os.makedirs(os.path.dirname(self._out_path), exist_ok=True)
                image.save(self._out_path)
                self.mapReady.emit(self._out_path)

        except Exception as e:
            print(f"MapWorker failure: {e}")
            self.error.emit(str(e))

    def stop(self):
        self._running = False