#config.py
"""This module contains CONSTANT configuration and data access paths or parameters."""

# Cellular modem SIM7600E and GPS expansion configuration
# GPS NMEA returns
GPS_NMEA_SERIAL_PORT = "/dev/ttyUSB2"
GPS__NMEA_BAUD_RATE = 115200
GPS__NMEA_TIMEOUT = 2

# AT Commands Port
AT_SERIAL_PORT = "/dev/ttyUSB2"
AT_BAUD_RATE = 115200
AT_TIMEOUT = 2
#--------------------

# CV Computer Vision configuration
# Paths to the models weights
MODEL_WEIGHTS = {
    "first_deck_seg" : "models/first_model_deck_seg_weights.pt",
    "yolo11" : "models/yolo11n.pt"
}
#-----------------

# Paths to data access
DEMO_ASSETS = {
    "video" : "data/demonstration_assets/vid_demonstration1.mov",
    "deck_photo" : "data/demonstration_assets/roi_base_demonstration1.jpg",
    "deck_photo2" : "data/demonstration_assets/roi_base_demonstration2.jpg"
}