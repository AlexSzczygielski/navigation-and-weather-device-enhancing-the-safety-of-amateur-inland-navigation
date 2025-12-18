#video_processor.py
# This class is responsible for handling logic with
# model_path - weights.pt
# video_path - either filepath to the demonstration asset or camera index 
# (both work fine with cv2.VideoCapture())
# **MOB DETECTION CV PIPELINE**

import cv2
from ultralytics import YOLO

class VideoProcessor():
    def __init__(self,model_path, video_path, roi_mask):
        self._model = YOLO(model_path)
        self._video_path = video_path
        self._roi_mask = roi_mask
    
    ### ROI CV COUNT PIPELINE ###

    def run_video_inference(self):
        #This method uses yield
        #This is a generator method
        cap = cv2.VideoCapture(self._video_path)

        #Perform checks
        if not cap.isOpened():
            raise IOError(f"Cannot open video input: {self._video_path}")
        if self._model is None:
            raise TypeError("_model is None!")
            
        while True:
            ret, frame = cap.read()
            print("it works")
            if not ret: #End of the clip
                print("end")
                break
            
            #Perform inference
            results = self._model(frame, classes=[0]) #Detect only people class

            # Visualize
            annotated_frame = results[0].plot()

            yield annotated_frame #return each frame without ending the method

        cap.release()