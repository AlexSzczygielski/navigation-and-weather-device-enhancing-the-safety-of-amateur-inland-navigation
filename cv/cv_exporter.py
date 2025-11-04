from ultralytics import YOLO
import numpy as np


#Config
model_path = '/Users/olek_szczygielski/Desktop/AGH/praca_inzynierska/repos/ROI-polygon-exporter/first_model_omega_boat_deck_weights.pt'

#Fetch image
image_path = '/Users/olek_szczygielski/Desktop/AGH/praca_inzynierska/Training_Data_Photos/boat_deck_test_photos_jpg/IMG_6003.jpg'

#Load model
model = YOLO(model_path)

#Run inference
results = model(image_path)

#access the first result
result = results[0]

#Get the mask coordinates
mask_coords = result.masks.xy[0]
#print(mask_coords)

#Save the mask coordinates to a text file
np.savetxt('mask_coordinates.txt', mask_coords, fmt='%f', delimiter=',')