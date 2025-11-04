import cv2
import numpy as np

image_path = '/Users/olek_szczygielski/Desktop/AGH/praca_inzynierska/Training_Data_Photos/boat_deck_test_photos_jpg/IMG_6003.jpg'

#Load image
img = cv2.imread(image_path)

#Load mask coordinates
mask_coords = np.loadtxt('mask_coordinates.txt', delimiter=',', dtype=np.int32)

#Draw the mask on the image
cv2.polylines(img, [mask_coords], isClosed=True, color=(0, 255, 0), thickness=2)

#Save the image
cv2.imwrite("output_mask.jpg", img)