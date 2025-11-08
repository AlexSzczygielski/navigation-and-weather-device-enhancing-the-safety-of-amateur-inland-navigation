#CvService.py
#This is a class file responsible for handling operations connected with
#Computer Vision modules
from ultralytics import YOLO
import numpy as np
import cv2

class CvService():
    def __init__(self, model_path):
        self._model_path = model_path
        self._image_path = None
        self._mask_coords = None

    def _fetch_image(self):
        self._image_path = 'cv/demonstration_assets/IMG_6003.jpg'

    def _mask_exporter(self):
        #method responsible for exporting the ROI mask coordinates
        #Fetch image
        self._fetch_image()

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