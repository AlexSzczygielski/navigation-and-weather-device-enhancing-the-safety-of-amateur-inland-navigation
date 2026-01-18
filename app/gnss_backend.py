#gnss_backend.py
"""This module contains the GnssBackend class responsible for managing backend of the GPS components."""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from haversine import haversine, Unit

from gnss_module.gnss_worker import GnssWorker
from gnss_module.map_worker import MapWorker
from gnss_module.gnss_data import GnssData
import config

class GnssBackend(QObject):
    def __init__(self):
        super().__init__()
        self._gnss_worker = None
        self._map_worker = None
        self._gnss_data = GnssData()
        self._last_latitude = None
        self._last_longitude = None
        self._pending_zoom = None
    
    def __del__(self):
        """Update last position in config.py"""
        if self._last_latitude is not None:
            if self._last_longitude is not None:
                config.LAST_SESSION_LATITUDE = self._last_latitude
                config.LAST_SESSION_LONGITUDE = self._last_longitude

    def shutdown(self):
        "Terminate all workers at appliaction close triggered by GUI."
        if self._gnss_worker:
            self._gnss_worker.stop()
            self._gnss_worker.quit()
            self._gnss_worker.wait()
            print("shutdown called")
        self._gnss_worker = None

        if self._map_worker:
            self._map_worker.stop()
            self._map_worker.quit()
            self._map_worker.wait()
            print("shutdown called")
        self._map_worker = None
    
    def get_last_position(self):
        return self._last_latitude, self._last_longitude

    #Possible signals
    @pyqtProperty(QObject, constant=True)
    def gnss_data(self):
        return self._gnss_data

    error = pyqtSignal(str)

    ### GNSS WORKER ###
    @pyqtSlot()
    def start_gnss_worker(self):
        try:
            #Ensure old worker is cleaned up
            if self._gnss_worker and self._gnss_worker.isRunning():
                print("Previous worker still running")
                return
            
            self._gnss_worker = GnssWorker(gnss_data=self.gnss_data)
            """Method on_x_updated is called automatically whenever x emits value. Arguments are automatically passed to the pointed method."""
            self._gnss_data.latitudeChanged.connect(self._on_latitude_updated)
            self._gnss_data.longitudeChanged.connect(self._on_longitude_updated)

            self._gnss_worker.error.connect(self.error)

            self._gnss_worker.finished.connect(self._on_start_gnss_worker_finished)
            self._gnss_worker.error.connect(self._on_start_gnss_worker_error)
            self._gnss_worker.finished.connect(self._gnss_worker.deleteLater)
            self._gnss_worker.start()

        except Exception as e:
            print(f"{self.__class__.__name__}.start_gnss_worker error: {e}")

    def _on_start_gnss_worker_finished(self):
        """Handles end of the task."""
        self._gnss_worker = None #Release the reference

    def _on_start_gnss_worker_error(self):
        """Emits error GUI."""
        print("error")
    
    def _on_latitude_updated(self, latitude):
        #First emit signal, later update map
        self._last_latitude = latitude
    
    def _on_longitude_updated(self, longitude):
        #First emit signal, later update map
        self._update_map_worker(self._last_latitude,longitude)

        #Update class's last longitude **after** map update
        self._last_longitude = longitude
    ###

    ### MAP WORKER ###
    def should_update_map(self, new_latitude, new_longitude, minimum_distance = 1, new_zoom=None):
        # first update - check if class members exist
        if self._last_latitude is None or self._last_longitude is None:
            return True
        # If user wants to update zoom - allow it
        if new_zoom is not None: 
            return True
        
        #get distance between last position and new position in meters
        distance_change = haversine(
            point1=(self._last_latitude, self._last_longitude),
            point2=(new_latitude, new_longitude),
            unit=Unit.METERS 
        )
        return distance_change >= minimum_distance

    def _update_map_worker(self, new_latitude, new_longitude, new_zoom=None):
        try:
            #Ensure old worker is cleaned up
            if self._map_worker and self._map_worker.isRunning():
                if new_zoom is not None:
                    # Set flag to refetch the map with new zoom when current worker finishes
                    # Prevents lost user request
                    self._pending_zoom = new_zoom
                return
            
            #Prevent single coordinate race
            if new_latitude is None or new_longitude is None:
                    return
                
            # Decision about fetching new map
            if self.should_update_map(new_latitude, new_longitude, new_zoom=new_zoom):
                if new_zoom is None:
                    self._map_worker = MapWorker(self._gnss_data, new_latitude=new_latitude, new_longitude=new_longitude, zoom=self._gnss_data.zoom)
                else:
                    self._map_worker = MapWorker(self._gnss_data, new_latitude=new_latitude, new_longitude=new_longitude, zoom=new_zoom)
                self._map_worker.error.connect(self._on_update_map_worker_error)
                self._map_worker.finished.connect(self._on_update_map_worker_finished)
                self._map_worker.finished.connect(self._map_worker.deleteLater)
                self._map_worker.start()
            else:
                return
        except Exception as e:
            print(f"{self.__class__.__name__}._update_map_worker error: {e}")
        
        

    def _on_update_map_worker_finished(self):
        """Handles end of the task."""
        self._map_worker = None #Release the reference

        # Handle the requested pending zoom change
        if self._pending_zoom is not None:
            zoom = self._pending_zoom
            self._pending_zoom = None # Reset the flag

            self._update_map_worker(    # Call the update
                new_latitude=self._last_latitude,
                new_longitude=self._last_longitude,
                new_zoom=zoom
            )

    def _on_update_map_worker_error(self):
        """Emits error GUI."""
        print("error")
    
    @pyqtSlot(str)
    def change_zoom(self, direction=None):
        if direction is None:
            self.error.emit("Zoom direction was not passed, abandon zoom change.")
            return
        if self.gnss_data.zoom < 0:
            self.error.emit("Zoom not available, abandon zoom change.")
            return
        
        if direction == "+":
            new_zoom = self._gnss_data.zoom + 1
        elif direction == "-":
            new_zoom = self._gnss_data.zoom - 1
        else:
            self.error.emit("Wrong direction, abandon zoom change.")
            return
        
        # Limit zoom range
        new_zoom = max(config.MAP_MIN_ZOOM, min(config.MAP_MAX_ZOOM, new_zoom))

        self._update_map_worker(
            new_latitude=self._last_latitude,
            new_longitude=self._last_longitude,
            new_zoom=new_zoom
        )
    ###