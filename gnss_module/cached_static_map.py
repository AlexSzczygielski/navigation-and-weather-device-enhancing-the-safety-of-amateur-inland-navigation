#cached_static_map.py

from staticmap import StaticMap
from urllib.parse import urlparse
import requests
import os
import logging

logger = logging.getLogger(__name__)

class CachedStaticMap(StaticMap):
    """
    Main purpose of this class is to provide a map tiles caching functionality for `staticmap` package.
    !! Stable operation on staticmap version: 0.5.7 !!
    """
    def get(self, url, **kwargs):
        """
        Get map tile from cache, if it does not exist - download and cache it.

        Override of StaticMap `get` method.
        Introduces a map caching (saving and reusing map tiles) functionality.
        IMPORTANT: leave the methods arguments as in the parent class - does not break 
        `get` calls inside staticmap implementation calls

        for context, this is the template we are expecting:
        url_template="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        z - zoom
        x - longitude
        y - latitude
        For the sake of keeping consistent with the parent class, original variable naming is
        preserved (x,y,z instead of more descriptive names).
        """
        #unpack url to get x,y,z for file name
        end_url_path = urlparse(url).path #parse url to get only x,y,z end part
        url_data = end_url_path.strip("/").split("/") #get list of data from url (separating by `/`)
        z = int(url_data[0])
        x = int(url_data[1])
        y = int(url_data[2].split(".")[0]) #remove .png part

        # Prepare cache filepath
        cache_root_dir = "data/map_tiles/osm_map_tiles_cache" # top folder
        cache_instance_dir = os.path.join(cache_root_dir, str(z), str(x)) # prepare z/x path
        os.makedirs(cache_instance_dir, exist_ok=True)
        cache_instance_file_path = os.path.join(cache_instance_dir, (str(y) + ".png")) #final path

        # Check if required tile is already saved and return it
        if os.path.exists(cache_instance_file_path):
            with open(file=cache_instance_file_path, mode="rb") as file: # png file in binary mode
                return 200, file.read() # 200 - response OK, required for parent class reasons
        else: 
            # Otherwise fetch from URL and cache
            res = requests.get(url, **kwargs)

            if res.status_code == 200:
                with open(cache_instance_file_path, "wb") as file: # save png file in binary mode
                    logger.info("fetched map_tile from url and written to file")
                    file.write(res.content)
            return res.status_code, res.content