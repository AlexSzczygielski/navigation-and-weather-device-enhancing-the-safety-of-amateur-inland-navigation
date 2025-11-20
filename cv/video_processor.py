#video_processor.py
#This class is responsible for handling logic with
# **MOB DETECTION CV PIPELINE**
import cv2
from ultralytics import YOLO

class VideoProcessor():
    def __init__(self,model_path, video_path):
        self._model = YOLO(model_path)
        self._video_path = video_path
    
    ### ROI CV COUNT PIPELINE ###

    def run_video_inference(self):
        #This method uses yield
        #This is then a generator method
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
            results = self._model(frame)

            # Visualize
            annotated_frame = results[0].plot()

            yield annotated_frame #return each frame without ending the method

        cap.release()
        #out.release()