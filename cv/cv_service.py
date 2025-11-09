#CvService.py
#This is a class file responsible for handling operations connected with
#Computer Vision modules
#This is also a context class in state pattern
from ultralytics import YOLO
import numpy as np
import cv2
from abc import ABC,abstractmethod
from cv.cv_state import CvState

class CvService():
    _state = None
    def __init__(self, model_path, state: CvState) -> None:
        self._model_path = model_path
        self._image_path = None
        self._mask_coords = None
        self.transition_to(state)
    
    def transition_to(self, state: CvState):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def fetch_image(self):
        self._state.fetch_image()

    def _mask_exporter(self):
        #method responsible for exporting the ROI mask coordinates
        #Fetch image
        self.fetch_image()

        #Load model
        model = YOLO(self._model_path)

        #Run inference
        results = model(self._image_path)

        #access the first (class) result
        result = results[0]

        #Get the mask coordinates
        self._mask_coords = result.masks.xy[0]
        #print(self._mask_coords)

        #Save the mask coordinates to a text file
        #np.savetxt('mask_coordinates.txt', self._mask_coords, fmt='%f', delimiter=',')

        return self._mask_coords
    
    def _mask_painter(self):
        #Painting mask over the image using cv2
        #Load image
        try:
            img = cv2.imread(self._image_path)

            #Load mask coordinates and prepare them for polylines
            #self._mask_coords = np.loadtxt('mask_coordinates.txt', delimiter=',', dtype=np.int32)
            mask_coords_poly = np.array(self._mask_coords, dtype=np.int32)

            #Draw the mask on the image
            cv2.polylines(img, [mask_coords_poly], isClosed=True, color=(0, 255, 0), thickness=40)

        except Exception as e:
            print(f"CvService mask_painter failed: {e}")

        #Save the image
        #cv2.imwrite("output_mask.jpg", img)

        return img