#video_processor.py
# This class is responsible for handling logic with
# model_path - weights.pt
# video_path - either filepath to the demonstration asset or camera index 
# (both work fine with cv2.VideoCapture())
# **MOB DETECTION CV PIPELINE**

import cv2
from ultralytics import YOLO
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add logging handler for separate process
if not logger.hasHandlers():
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class VideoProcessor():
    def __init__(self,model_path, video_path, roi_mask):
        self._model = YOLO(model_path)
        self._video_path = video_path
        self._roi_mask = roi_mask
    
    ### ROI CV COUNT PIPELINE ###

    def run_video_inference(self, stop_event):
        #This method uses yield
        #This is a generator method
        cap = cv2.VideoCapture(self._video_path)
        try:
            #Perform checks
            if not cap.isOpened():
                raise IOError(f"Cannot open video input: {self._video_path}")
            if self._model is None:
                raise TypeError("_model is None!")
            if self._roi_mask is None:
                raise TypeError(f"[{__name__}]: ROI mask is none")
            
            logger.info("Started video inference")
            while True:
                if stop_event.is_set():
                    #Exit upon stop event
                    logger.info("Stop event received, exiting the loop")
                    break

                ret, frame = cap.read()
                if not ret: #End of the clip
                    logger.info("Stopped video inference")
                    yield None
                    break
                
                #Perform inference
                results = self._model(frame, classes=[0], verbose=False) #Detect only people class

                # Visualize
                annotated_frame = results[0].plot()

                yield annotated_frame #return each frame without ending the method

        finally:
            logger.info("Releasing videocapture")
            cap.release()