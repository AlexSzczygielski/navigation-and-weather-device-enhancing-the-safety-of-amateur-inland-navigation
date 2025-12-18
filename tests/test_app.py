# app_tests.py

import pytest
from app.factories.create_backend import create_backend

def test_cv_worker(qtbot):
    # Create Backend
    backend = create_backend()

     # Run the ROI pipeline
    backend.run_cv_roi_pipe()

    # As CvWorker starts new thread - waiting is required for the signal to comeback
    # waiting for backend.roiImageUpdated
    with qtbot.waitSignal(backend.roiImageUpdated, timeout=5000) as blocker:
        pass 

    assert backend.get_roi_img() is not None, "Mask image was not returned from get_roi_img"