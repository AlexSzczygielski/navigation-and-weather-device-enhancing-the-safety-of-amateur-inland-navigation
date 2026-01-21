#cv_backend.py
"""This module contains the CvBackend class, responsible for managing backend of CV Components"""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QProcess, QUrl
import logging

from cv.cv_worker import CvWorker
from cv.cv_state import CvState
from cv.cv_demo_state_service import CvDemoStateService
from cv.cv_data import CvData

logger = logging.getLogger(__name__)

class CvBackend(QObject):
    """
    Manages connection (using signals/slots) between the CV GUI and CV Workers.

    CvBackend is responsible for delegating tasks that are triggered through signals coming from
    GUI (e.g. a button click) to dedicated workers, that handle the task's execution. Workers 
    are able to return data back to GUI using slots.

    Supports:
    - ROI (Region of Interest) mask creation pipeline
    - MOB (Man Overboard) detection pipeline

    Inherits from QObject - base class that provides signals/slots, event handling, object trees,
    memory management for Qt Objects.

    Each task checks if the previous worker is still running - to prevent starting many workers
    before the current one finishes it's job.
    Not being able to create ROI mask while running MOB detection task is intentional.

    Parameters
    ----------
    roi_img_model_path : str
        Path to the boat_deck_segmenation ML model weights.
    vid_model_path : str
        Path to the YOLO CV model weights.
    
    Attributes
    ----------
    roiImageUpdated : pyqtSignal(str)
        PyQt signal emitted when new ROI mask is returned.
    mobFrameUpdated : pyqtSignal(str)
        PyQt signal emitted when new MOB frame is returned.
    """
    def __init__(self,roi_img_model_path,vid_model_path):
        super().__init__()
        self._cv_data = CvData()
        self._roi_img_model_path = roi_img_model_path
        self._vid_model_path = vid_model_path
        self._worker = None
    

    def shutdown(self):
        "Terminate all CvWorkers at appliaction close triggered by GUI."
        if self._worker:
            self._worker.stop()
            self._worker.quit()
            self._worker.wait()
            logger.info("shutdown called")
        self._worker = None

    
    #Possible signals
    @pyqtProperty(QObject, constant=True)
    def cv_data(self):
        return self._cv_data
    

    ### ROI CREATION PIPELINE ###
    @pyqtSlot()
    def run_cv_roi_pipe(self):
        """
        Runs the Region Of Interest creation pipeline, PyQt slot.

        Returns immediately if previous worker (pipe)
        is still running.
        Creates a new CVWorker, uses _on_run_cv_roi_pipe_finished(),
        _on_run_cv_roi_pipe_error() and 
        get_roi_img() to communicate with GUI. 

        Emits
        -----
        roiImageUpdated : str
            Base64 encoded string of image.
        """
        try:
            #Ensure old worker is cleaned up
            if self._worker and self._worker.isRunning():
                logger.warning("run_cv_roi_pipe(): Previous worker still running")
                return

            task = "roi_creation"
            self._worker = CvWorker(self._roi_img_model_path,CvDemoStateService(), task, self._cv_data) #worker with context
            self._worker.finished.connect(self._on_run_cv_roi_pipe_finished)
            self._worker.error.connect(self._on_run_cv_roi_pipe_error)
            self._worker.finished.connect(self._worker.deleteLater)
            self._worker.start()
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.run_cv_roi_pipe error: {e}")

    def _on_run_cv_roi_pipe_finished(self):
        """Handles end of the task - emits to GUI."""
        self._worker = None #Release the reference

    def _on_run_cv_roi_pipe_error(self):
        """Emits error GUI."""
        logger.error("run_cv_roi_pipe_error")

    @pyqtSlot(result=str)
    def get_roi_img(self):
        """If ready return base64 encoded ROI image."""
        #This can be used when loading/reloading the cv_create_roi_panel view
        if self._cv_data.roiImageBase64 is None:
            return None
        return self._cv_data.roiImageBase64


    ### MOB CV DETECTION PIPE ###  
    @pyqtSlot()
    def run_cv_mob_detect_pipe(self):
        """
        Runs the Man Overboard detection pipeline. PyQt slot.

        Returns immediately if previous worker (pipe)
        is still running.
        Creates a new CVWorker, uses _on_run_cv_mob_detect_pipe_finished(),
        _on_run_cv_mob_detect_pipe__error() and 
        _onMobFrameUpdated() to communicate with GUI. 

        Emits
        -----
        _onMobFrameUpdated : str
            Base64 encoded string of an image frame.
        """
        #Runs mob detection system
        try:
            if self._worker and self._worker.isRunning():
                logger.warning("run_cv_mob_detect_pipe(): Previous worker still running")
                return
            
            task = "mob_detection_pipe"
            self._worker = CvWorker(self._vid_model_path,CvDemoStateService(),task, self._cv_data) #worker with context
            self._worker.finished.connect(self._on_run_cv_mob_detect_pipe_finished)
            self._worker.error.connect(self._on_run_cv_mob_detect_pipe_error)
            self._worker.finished.connect(self._worker.deleteLater)
            self._worker.start()
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.run_cv_mob_detect_pipe error: {e}")

    def _on_run_cv_mob_detect_pipe_finished(self):
        """Handles end of the task - emits to GUI."""
        self._worker = None

    def _on_run_cv_mob_detect_pipe_error(self):
        """Emits error GUI."""
        logger.error("run_cv_mob_detect_pipe_error(): error")