# app_tests.py

import pytest
from PyQt5.QtGui import QGuiApplication
import sys
from main import create_app

def test_cv_worker(qtbot):
    # Create App
    view, backend = create_app()

     # Run the ROI pipeline
    backend.run_cv_roi_pipe()

    # Wait for the signal from the backend
    with qtbot.waitSignal(backend.roiImageUpdated, timeout=5000) as blocker:
        pass  # the signal will be captured here

    # Assert that the backend stored the image
    assert backend.get_roi_img() is not None, "Mask image was not returned from get_roi_img"