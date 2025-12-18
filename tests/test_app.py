# app_tests.py

import pytest
from PyQt5.QtGui import QGuiApplication
import sys
import cv2
from unittest.mock import patch
from main import create_app
from main import Backend
import cv.roi_processor

from unittest.mock import patch

class DummyRoiProcessor:
    def _mask_exporter(self, img):
        # returns dummy mask coords
        return [[0,0],[1,1]]
    
    def _mask_painter(self, image, mask_coords):
        # Returns dummy image
        img = cv2.imread(image)
        return img 

@pytest.fixture
def mock_roi_processor(monkeypatch):
    # Replace RoiProcessor with it's dummy testing version
    monkeypatch.setattr(cv.roi_processor, "cv.RoiProcessor" , DummyRoiProcessor)



def test_cv_worker(qtbot):
    # Create App
    view, backend = create_app()

     # Run the ROI pipeline
    backend.run_cv_roi_pipe()

    # As CvWorker starts new thread - waiting is required for the signal to comeback
    # waiting for backend.roiImageUpdated
    with qtbot.waitSignal(backend.roiImageUpdated, timeout=5000) as blocker:
        pass 

    assert backend.get_roi_img() is not None, "Mask image was not returned from get_roi_img"