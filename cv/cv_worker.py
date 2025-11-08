#cv_worker.py
#Class responsible for managing QThreading for cv_service.py logic
from PyQt5.QtCore import QThread, pyqtSignal
import os
from cv.cv_service import CvService


class CvWorker(QThread):
    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path

    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            cv = CvService(self.model_path)
            cv.mask_exporter()
            cv.mask_painter()
            img_path = os.path.abspath("output_mask.jpg")
            self.finished.emit(img_path)
        except Exception as e:
            print(f"run_mask_exporter failed: {e}")