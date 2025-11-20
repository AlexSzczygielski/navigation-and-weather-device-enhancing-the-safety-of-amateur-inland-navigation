#image_encoder.py
# Image conversions, cv2 img to string types

import numpy as np
import cv2
import base64

class ImageEncoder:
    
    @staticmethod
    def to_base64(img: np.ndarray) -> str:
        #Encodes a cv2 img into a base64 JPG string
        if img is None:
            raise IOError(f"{__class__.__name__}.to_base64: img object is empty")
        
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer).decode('utf-8')