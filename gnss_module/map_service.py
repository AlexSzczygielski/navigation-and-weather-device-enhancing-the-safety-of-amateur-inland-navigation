#map_service.py
from gnss_module.cached_static_map import CachedStaticMap
from staticmap import CircleMarker
import config

class MapService():
    def __init__(self, zoom=None, latitude = None, longitude=None):
          self._zoom = zoom
          self._latitude = latitude
          self._longitude = longitude

    def render_map(self):
            if self._zoom is None or self._latitude is None or self._longitude is None:
                # Configure static map
                m = CachedStaticMap(config.MAP_WIDTH,config.MAP_HEIGHT)
                mark = CircleMarker(
                    coord=(self._longitude, self._latitude),
                    color='red',
                    width=12
                )
                m.add_marker(marker=mark)

                # Render map
                image = m.render(zoom=self._zoom)

                #Save new map tile and emit filepath
                save_path = "data/temp/current_map.png" #TODO: Change to pass this map as binary or encoded base64
                image.save(save_path)
            else:
                  return None