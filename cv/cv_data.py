#cv_data.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

class CvData(QObject):
    def __init__(self):
        super().__init__()
        self._roiImageBase64 = None
        self._mobFrameBase64 = None
    
    roiImageBase64Updated = pyqtSignal(str) # ROI Creation pipe
    mobFrameBase64Updated = pyqtSignal(str) # MOB cv detection pipe

    @pyqtProperty(str, notify=roiImageBase64Updated)
    def roiImageBase64(self):
        return self._roiImageBase64
    
    @roiImageBase64.setter
    def roiImageBase64(self,value):
        if self._roiImageBase64 != value:
            self._roiImageBase64 = value
            self.roiImageBase64Updated.emit(self._roiImageBase64)

    @pyqtProperty(str, notify=mobFrameBase64Updated)
    def mobFrameBase64(self):
        return self._mobFrameBase64
    
    @mobFrameBase64.setter
    def mobFrameBase64(self,value):
        # skipping if already exists check, as this is always new data
        self._mobFrameBase64 = value
        self.mobFrameBase64Updated.emit(self._mobFrameBase64)