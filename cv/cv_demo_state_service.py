#cv_demo_state_service.py
#This state is demonstration - reads from disk instead of camera
from cv.cv_state import CvState
from cv.cv_service import CvService
import cv2

class CvDemoStateService(CvState):
    def setup_vid_stream(self):
        cap = cv2.VideoCapture("cv/demonstration_assets/motor1.MOV")
        return cap

    def fetch_image(self):
        self.context._image_path = 'cv/demonstration_assets/IMG_6003.jpg'
        return self.context._image_path

    def fetch_frame(self, cap):
        ret, frame = cap.read()
        
        if not ret:
            print("Can't read the frame")
            return None
        else:
            print("returning frame")
            return ret, frame