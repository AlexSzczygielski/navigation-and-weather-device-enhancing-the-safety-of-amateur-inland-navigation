#cv_worker.py
"""This module contains the CvWorker class, responsible for starting the managing QThreads used by CvService Components"""
from PyQt5.QtCore import QThread, pyqtSignal
import os
from cv.cv_service import CvService
from cv.image_encoder import ImageEncoder


class CvWorker(QThread):
    """
    A worker class managing asynchronous (threaded) CV tasks execution.

    Responsible for starting appropriate service class and it's task.
    Task is specified during CvWorker initialization (CvBackend).
    Unblocks the main GUI Thread.
    Returns results using PyQt signals.

    Parameters
    ----------
    model_path : str
        Path to the appropriate ML model weights.
    service_state : CvState
        State class object required by CvState.
    task : str
        Task to perform:
        - "roi_creation" : starts ROI pipeline service
        - "mob_detection_pipe" : starts MOB detection pipeline service.

    Signals
    -------
    finished : pyqtSignal(str)
        PyQt signal emitted when task is finished.
    error : pyqtSignal(str)
        PyQt signal emitted upon error.
    frameUpdate : pyqtSignal(str)
        PyQt signal emitted when new MOB frame is returned.
    """
    def __init__(self, model_path, service_state ,task):
        super().__init__()
        self._model_path = model_path
        self._service_state = service_state #State for Service class started from this thread
        self._task = task #Determines the task to be started
        self._cv_service = None
        self._running = True

    def stop(self):
        self._running=False
        if self._cv_service:
            self._cv_service.stop_video_process()

    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    frameUpdate = pyqtSignal(str)

    def run(self):
        """
        This method is entered by calling a QThread.start(). Entry point of the operation.

        Called from backend - `self._task` argument determines which task to start:
        - "ROI creation"
        - "MOB detection pipe"
        Creates CvService, which can emit signal after its' task is finished
        Signal emitted from CvService is emitted further to appropriate backend.

        Raises
        ------
        ValueError
            If `self._task` is none
        """
        #main method, this is entered after backend calls worker
        try:
            self._cv_service = CvService(self._model_path, self._service_state)

            match self._task:
                case "roi_creation":
                    img = self._cv_service.run_roi_creation_pipeline()
                    #img_path = os.path.abspath("output_mask.jpg")
                    #self.finished.emit(img_path)

                    #Encoding image to base_64
                    img_base64 = ImageEncoder.to_base64(img)
                    self.finished.emit(img_base64)
                

                case "mob_detection_pipe":
                    queue = self._cv_service.run_mob_detect_pipe_process()

                    while True:
                        if not self._running:
                            break

                        frame = queue.get(timeout=0.2)
                        if frame is None:
                            self.finished.emit("")
                            break
                        
                        frame_base64 = ImageEncoder.to_base64(frame)
                        self.frameUpdate.emit(frame_base64)                            
                
                case _:
                    raise ValueError(f"Unknown task: {self._task}")
            
        except Exception as e:
            print(f"CvWorker failed: {e}")

        self._cv_service = None