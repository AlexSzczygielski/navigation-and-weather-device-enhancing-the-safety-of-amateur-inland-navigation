#config.py
# This file contains CONSTANT configuration paths

# Path to the models weights

MODEL_WEIGHTS = {
    "first_deck_seg" : "models/first_model_deck_seg_weights.pt",
    "yolo11" : "models/yolo11n.pt"
}

DEMO_ASSETS = {
    "video" : "data/demonstration_assets/vid_demonstration1.mov",
    "deck_photo" : "data/demonstration_assets/roi_base_demonstration1.jpg"
}