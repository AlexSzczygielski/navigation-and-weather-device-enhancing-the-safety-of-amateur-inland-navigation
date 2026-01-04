#factories.py
"""This module contains functions responsible for creation of backends."""
import config as config
import platform
from app.backend import Backend
from app.cv_backend import CvBackend
from app.gnss_backend import GnssBackend
from app.weather_backend import WeatherBackend

def create_backend():
    return Backend(
        create_cv_backend(),
        create_gnss_backend(),
        create_weather_backend()
    )

def create_cv_backend():
    return CvBackend(
        roi_img_model_path=config.MODEL_WEIGHTS["first_deck_seg"],
        vid_model_path=config.MODEL_WEIGHTS["yolo11"]
    )

def create_gnss_backend():
    return GnssBackend()

def create_weather_backend():
    return WeatherBackend()