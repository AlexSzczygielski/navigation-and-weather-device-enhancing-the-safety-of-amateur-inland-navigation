#factories.py
"""This module contains functions responsible for creation of backends."""
import config as config
import platform
from app.backend import Backend
from app.cv_backend import CvBackend
from app.gps_backend import GnssBackend

def create_backend():
    return Backend(
        create_cv_backend(),
        create_gps_backend()
    )

def create_cv_backend():
    return CvBackend(
        roi_img_model_path=config.MODEL_WEIGHTS["first_deck_seg"],
        vid_model_path=config.MODEL_WEIGHTS["yolo11"]
    )

def create_gps_backend():
    return GnssBackend()