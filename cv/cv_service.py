#CvService.py
#This is a class file responsible for handling operations connected with
#Computer Vision modules
from ultralytics import YOLO
import numpy as np
import cv2

class CvService():
    def __init__(self, model_path):
        self.model_path = model_path
    
    image_path = ''

    def fetch_image(self):
        self.image_path = '/Users/olek_szczygielski/Desktop/AGH/praca_inzynierska/Training_Data_Photos/boat_deck_test_photos_jpg/IMG_6003.jpg'

    def mask_exporter(self):
        #method responsible for exporting the ROI mask coordinates
        #Fetch image
        self.fetch_image()

        #Load model
        model = YOLO(self.model_path)

        #Run inference
        results = model(self.image_path)

        #access the first result
        result = results[0]

        #Get the mask coordinates
        mask_coords = result.masks.xy[0]
        #print(mask_coords)

        #Save the mask coordinates to a text file
        np.savetxt('mask_coordinates.txt', mask_coords, fmt='%f', delimiter=',')

        return mask_coords
    
    def mask_painter(self):
        #Painting mask over the image using cv2
        #Load image
        try:
            img = cv2.imread(self.image_path)
        except Exception as e:
            print(f"Failed to load image to mask_painter module: {e}")

        #Load mask coordinates
        mask_coords = np.loadtxt('mask_coordinates.txt', delimiter=',', dtype=np.int32)

        #Draw the mask on the image
        cv2.polylines(img, [mask_coords], isClosed=True, color=(0, 255, 0), thickness=2)

        #while(True):
            #print("here")

        #Save the image
        cv2.imwrite("output_mask.jpg", img)