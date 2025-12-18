#test_vid_processor.py
# This is a simple test for video processor class
# It checks if video processor returns (yields) a frame and does not crash

import pytest
from cv.video_processor import VideoProcessor
import config

dummy_mask = [[0,0],[1,1]]

def test_run_video_inference():
    processor = VideoProcessor(config.MODEL_WEIGHTS["yolo11"], config.DEMO_ASSETS["video"], dummy_mask)

    try:
        generator = processor.run_video_inference()
        frame = next(generator)
        assert frame is not None
    except Exception as e:
        pytest.fail(f"VideoProcessor.run_video_inference() test has failed: {e}")