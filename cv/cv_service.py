#CvService.py
#This is a class file responsible for handling/coordinating operations connected with
#Computer Vision modules
#A context class in state pattern
from ultralytics import YOLO
import numpy as np
import cv2
from abc import ABC,abstractmethod
from cv.cv_state import CvState
from cv.roi_processor import RoiProcessor
from cv.video_processor import VideoProcessor

class CvService():
    _state = None
    def __init__(self, model_path, state: CvState) -> None:
        self._model_path = model_path
        self._image_path = None
        self._mask_coords = None
        self._roi_processor = RoiProcessor(model_path)
        self._video_processor = VideoProcessor(model_path)
        self.transition_to(state)
    
    def transition_to(self, state: CvState):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    ### ROI CREATION ###
    def fetch_image(self):
        return self._state.fetch_image()

    def run_roi_creation_pipeline(self):
        img = self.fetch_image() # Important! Fetch image only once (avoids bugs with camera movement)
        roi_mask = self._roi_processor._mask_exporter(img) # !! MASK COORDS SHOULD BE STORED ALSO IN MEMORY! (TODO!)
        return self._roi_processor._mask_painter(img,roi_mask) #image
    
    ### ROI CV COUNT PIPELINE ###
    def fetch_frame(self, cap):
        return self._state.fetch_frame(cap)
    
    def setup_vid_stream(self):
        return self._state.setup_vid_stream()

    def run_video_detection_pipeline(self):
        cap = self.setup_vid_stream()
        self._video_processor.run_video_inference(cap)