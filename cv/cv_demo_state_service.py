#cv_demo_state_service.py
#This state is demonstration - reads from disk instead of camera
from cv.cv_state import CvState
from cv.cv_service import CvService
import cv2
import logging

import config

logger = logging.getLogger(__name__)

class CvDemoStateService(CvState):
    def get_vid_source(self):
        return config.DEMO_ASSETS["video2"]

    def setup_vid_stream(self):
        cap = cv2.VideoCapture(self.get_vid_source())
        return cap

    def fetch_image(self):
        self.context._image_path = config.DEMO_ASSETS["deck_photo"]
        return self.context._image_path

    def fetch_frame(self, cap):
        ret, frame = cap.read()
        
        if not ret:
            logger.warning("Can't read the frame")
            return None
        else:
            return ret, frame