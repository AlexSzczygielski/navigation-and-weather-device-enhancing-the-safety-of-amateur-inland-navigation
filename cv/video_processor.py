#video_processor.py
#This class is responsible for handling logic with
# **MOB DETECTION CV PIPELINE**
import cv2
from ultralytics import YOLO

class VideoProcessor():
    def __init__(self,model_path):
        self._model = YOLO(model_path)
    
    ### ROI CV COUNT PIPELINE ###

    def run_video_inference(self, cap):
        if cap is None:
            raise TypeError("cap (capture cv2 object) is None!")
        if self._model is None:
            raise TypeError("_model is None!")

        # Get video properties
        #width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #fps    = cap.get(cv2.CAP_PROP_FPS)

        # Define output video writer
        #out = cv2.VideoWriter("motor1Out.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        ret, frame = self.fetch_frame(cap)
        if frame is None:
            raise IOError("Cannot access the frame")
            
        while(True):
            ret, frame = self.fetch_frame(cap)
            if not ret: #End of the clip
                break
            
            #Perform inference
            results = self._model(frame)

            # Visualize
            annotated_frame = results[0].plot()

            # Write to output
            #out.write(annotated_frame)
        cap.release()
        #out.release()
