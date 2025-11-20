#cv_worker.py
# QThread inherited worker responsible for running Computer Vision tasks in background threads.
# input:
# _model_path: path to the YOLO model
# _service_state: CvState pattern defines the input for services
# _task: string defining which task to perform
# Worker is responsible for starting the CvService, which executes given task without blocking the main UI loop.

from PyQt5.QtCore import QThread, pyqtSignal
import os
from cv.cv_service import CvService
from cv.image_encoder import ImageEncoder


class CvWorker(QThread):
    def __init__(self, model_path, service_state ,task):
        super().__init__()
        self._model_path = model_path
        self._service_state = service_state #State for Service class started from this thread
        self._task = task #Determines the task to be started

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        #main method, this is entered after backend calls worker
        try:
            cv = CvService(self._model_path, self._service_state)

            match self._task:
                case "roi_creation":
                    img = cv.run_roi_creation_pipeline()
                    #img_path = os.path.abspath("output_mask.jpg")
                    #self.finished.emit(img_path)

                    #Encoding image to base_64
                    img_base64 = ImageEncoder.to_base64(img)
                    self.finished.emit(img_base64)
                

                case "mob_detection_pipe":
                    generator = cv.run_mob_detect_pipe_process()

                    while True:
                        try:
                            frame = next(generator)
                            frame_base64 = ImageEncoder.to_base64(frame)
                            self.finished.emit(frame_base64)
                        except StopIteration:
                            break
                
                case _:
                    raise ValueError(f"Unknown task: {self._task}")
            
        except Exception as e:
            print(f"CvWorker failed: {e}")