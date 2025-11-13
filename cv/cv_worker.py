#cv_worker.py
#Class responsible for managing QThreading for cv_service.py logic
from PyQt5.QtCore import QThread, pyqtSignal
import os
import cv2
import base64
from cv.cv_service import CvService


class CvWorker(QThread):
    def __init__(self, model_path, service_state):
        super().__init__()
        self._model_path = model_path
        self._service_state = service_state #State for Service class started from this thread

    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            cv = CvService(self._model_path, self._service_state)
            img = cv.run_roi_creation_pipeline()
            #img_path = os.path.abspath("output_mask.jpg")
            #self.finished.emit(img_path)

            #Encoding image to base_64
            _, buffer = cv2.imencode('.jpg', img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            self.finished.emit(img_base64)
            
        except Exception as e:
            print(f"run_cv_worker failed: {e}")