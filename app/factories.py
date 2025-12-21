#factories.py
import config as config
from app.backend import Backend
from app.cv_backend import CvBackend

def create_backend():
    return Backend(
        create_cv_backend()
    )

def create_cv_backend():
    return CvBackend(
        roi_img_model_path=config.MODEL_WEIGHTS["first_deck_seg"],
        vid_model_path=config.MODEL_WEIGHTS["yolo11"]
    )