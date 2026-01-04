# app_tests.py

import pytest
from app.factories import create_backend

# Create Backend
backend = create_backend()

def test_cv_worker(qtbot):
     # Run the ROI pipeline
    backend.cv.run_cv_roi_pipe()

    # As CvWorker starts new thread - waiting is required for the signal to comeback
    # waiting for backend.roiImageUpdated
    with qtbot.waitSignal(backend.cv.cv_data.roiImageBase64Updated, timeout=5000) as blocker:
        pass 

    assert backend.cv.get_roi_img() is not None, "Mask image was not returned from get_roi_img"