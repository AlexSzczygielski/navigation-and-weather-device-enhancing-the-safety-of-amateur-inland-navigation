#map_service.py
from gnss_module.cached_static_map import CachedStaticMap
from staticmap import CircleMarker
import config
import os

from PIL import Image
from io import BytesIO
import base64

class MapService():
    def __init__(self, zoom=None, latitude = None, longitude=None):
          self._zoom = zoom
          self._latitude = latitude
          self._longitude = longitude

    def render_map(self):
            if self._zoom is None or self._latitude is None or self._longitude is None:
                return None
            
            # Configure static map
            m = CachedStaticMap(config.MAP_WIDTH,config.MAP_HEIGHT)
            mark = CircleMarker(
                coord=(self._longitude, self._latitude),
                color='red',
                width=12
            )
            m.add_marker(marker=mark)

            # Render map
            image = m.render(zoom=self._zoom) #PIL object

            return self._encode_pil_to_base_64(image)

    def _encode_pil_to_base_64(self, image: Image.Image):
          buffer = BytesIO()
          image.save(buffer, format="PNG")
          buffer.seek(0)
          return base64.b64encode(buffer.read()).decode("utf-8")