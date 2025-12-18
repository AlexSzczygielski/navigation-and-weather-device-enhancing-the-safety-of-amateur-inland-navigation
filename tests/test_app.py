# app_tests.py

import pytest
from main import Backend
import config

def test_cv_worker(qtbot):
    # Create Backend
    backend = Backend(roi_img_model_path= config.MODEL_WEIGHTS["first_deck_seg"],
                      vid_model_path= config.MODEL_WEIGHTS["yolo11"])

     # Run the ROI pipeline
    backend.run_cv_roi_pipe()

    # As CvWorker starts new thread - waiting is required for the signal to comeback
    # waiting for backend.roiImageUpdated
    with qtbot.waitSignal(backend.roiImageUpdated, timeout=5000) as blocker:
        pass 

    assert backend.get_roi_img() is not None, "Mask image was not returned from get_roi_img"