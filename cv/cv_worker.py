#cv_worker.py
"""This module contains the CvWorker class, responsible for starting the managing QThreads used by CvService Components"""
from PyQt5.QtCore import QThread, pyqtSignal
import os
from queue import Empty
import logging
import queue
import multiprocessing

from cv.cv_pipe_status import CvPipeStatus
from cv.cv_service import CvService
from cv.image_encoder import ImageEncoder
from cv.cv_data import CvData
from cv.cv_state import CvState

logger = logging.getLogger(__name__)

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
    def __init__(self, model_path: str, service_state: CvState ,task: str, cv_data: CvData):
        super().__init__()
        self._model_path = model_path
        self._service_state = service_state #State for Service class started from this thread
        self._task = task #Determines the task to be started
        self._cv_service = None
        self._running = True
        self._cv_data = cv_data

    def stop(self):
        self._running=False
        self._cv_data.runningMobPipeStatus=False
        if self._cv_service:
            self._cv_service.stop_video_process()

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

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
            self._cv_service = CvService(self._model_path, self._service_state, self._cv_data.mask_coords)

            match self._task:
                case "roi_creation":
                    img, self._cv_data.mask_coords = self._cv_service.run_roi_creation_pipeline()

                    #Encoding image to base_64
                    img_base64 = ImageEncoder.to_base64(img)
                    self._cv_data.roiImageBase64 = "data:image/png;base64," + img_base64
                

                case "mob_detection_pipe":
                    status_queue, frame_queue = self._cv_service.run_mob_detect_pipe_process()
                    self._cv_data.runningMobPipeStatus=False

                    while self._running:
                        try:
                            status, msg = status_queue.get_nowait()
                            if status == CvPipeStatus.Running:
                                self._cv_data.runningMobPipeStatus=True
                                logger.info("MOB CV pipe running")

                            elif status == CvPipeStatus.END:
                                logger.info("MOB CV pipe end signal - stopping")
                                self._cv_data.runningMobPipeStatus = False
                                self._running = False
                                break
                            
                            elif status == CvPipeStatus.ERROR:
                                self._cv_data.runningMobPipeStatus=False
                                self._running = False
                                logger.error(f"MOB CV pipe error: {msg}")

                        except (queue.Empty, multiprocessing.queues.Empty):
                            pass
                        
                        if self._cv_data.runningMobPipeStatus:
                            try:
                                frame = frame_queue.get(timeout=5)
                                if frame is None: # END of stream - send empty string
                                    logger.info("MOB CV pipe frame stream ended")
                                    self._cv_data.mobFrameBase64 = ""
                                    self._running = False
                                    self._cv_data.runningMobPipeStatus=False
                                    break
                                
                                frame_base64 = ImageEncoder.to_base64(frame)
                                self._cv_data.mobFrameBase64 = "data:image/png;base64," + frame_base64

                            except (queue.Empty, multiprocessing.queues.Empty):
                                pass
                                continue
                        
                case _:
                    raise ValueError(f"Unknown task: {self._task}")
            
        except Exception as e:
            logger.error(f"CvWorker failed: {e}")
        
        finally:
            if self._task == "mob_detection_pipe" and self._cv_service:
                self._cv_service.shutdown()
            self._cv_service = None