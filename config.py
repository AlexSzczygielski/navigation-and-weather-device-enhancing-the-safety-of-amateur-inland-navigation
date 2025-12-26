#config.py
"""This module contains CONSTANT configuration and data access paths or parameters."""

# Map configuration
MAP_WIDTH = 500
MAP_HEIGHT = 500
MAP_STANDARD_ZOOM = 15 # 1-19 constraint
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