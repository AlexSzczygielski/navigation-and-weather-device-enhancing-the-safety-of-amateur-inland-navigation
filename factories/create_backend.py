# create_backend.py
from app.backend import Backend
import config

def create_backend():
    return Backend(
        roi_img_model_path=config.MODEL_WEIGHTS["first_deck_seg"],
        vid_model_path=config.MODEL_WEIGHTS["yolo11"]
    )