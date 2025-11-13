#roi_processor.py
#This class is responsible for handling logic with
# **CREATION of ROI** used later in MOB CV Detection Pipeline
import cv2
import numpy as np
from ultralytics import YOLO

class RoiProcessor():
    def __init__(self,model_path):
        self._model = YOLO(model_path)

    ### ROI CREATION ###

    def _mask_exporter(self, img):
        #method responsible for exporting the ROI mask coordinates

        if img is None:
            raise TypeError("img is None!")
        if self._model is None:
            raise TypeError("_model is None!")
        
        #Run inference
        results = self._model(img)

        #access the first (class) result
        result = results[0]

        #Save the mask coordinates to a text file
        #np.savetxt('mask_coordinates.txt', result.masks.xy[0], fmt='%f', delimiter=',')

        return result.masks.xy[0]
    
    def _mask_painter(self, image, mask_coords):
        #Painting mask over the image using cv2

        try:
            img = cv2.imread(image)

            #Load mask coordinates and prepare them for polylines
            #self._mask_coords = np.loadtxt('mask_coordinates.txt', delimiter=',', dtype=np.int32)
            mask_coords_poly = np.array(mask_coords, dtype=np.int32)

            #Draw the mask on the image
            cv2.polylines(img, [mask_coords_poly], isClosed=True, color=(0, 255, 0), thickness=40)

            return img

        except Exception as e:
            print(f"CvService mask_painter failed: {e}")
            return None

        