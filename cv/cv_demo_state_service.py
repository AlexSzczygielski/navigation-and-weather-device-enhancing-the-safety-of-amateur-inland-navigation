#cv_demo_state_service.py
#This state is demonstration - reads from disk instead of camera
from cv.cv_state import CvState
from cv.cv_service import CvService

class CvDemoStateService(CvState):
    def fetch_image(self):
        print("CvDemoStateService does the work")
        self.context._image_path = 'cv/demonstration_assets/IMG_6003.jpg'