#test_mask_exporter.py
# This is a simple test for RoiProcessor class
# It checks if mask_exporter returns and does not crash

import pytest
from cv.roi_processor import RoiProcessor
from ultralytics import YOLO
import config
import numpy as np

processor = RoiProcessor(config.MODEL_WEIGHTS["first_deck_seg"])
img = config.DEMO_ASSETS["deck_photo"]

def test_mask_exporter():
    try:
        mask_coords = processor._mask_exporter(img)
        assert mask_coords is not None
        assert isinstance(mask_coords, np.ndarray)
    except Exception as e:
        pytest.fail(f"RoiProcessor._mask_exporter() test has failed: {e}")

def test_mask_painter():
    try:
        mask_coords = processor._mask_exporter(config.DEMO_ASSETS["deck_photo"])
        result_img = processor._mask_painter(img,mask_coords)
        assert result_img is not None
    except Exception as e:
        pytest.fail(f"RoiProcessor._mask_painter() test has failed: {e}")