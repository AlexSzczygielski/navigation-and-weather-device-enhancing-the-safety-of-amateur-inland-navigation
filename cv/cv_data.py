#cv_data.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

class CvData(QObject):
    def __init__(self):
        super().__init__()
        self._roiImageBase64 = None
        self._mobFrameBase64 = None
        self._detectedPeople = None
        self._runningMobPipeStatus = False
        self._boatDeckMaskStatus = False
        self._mobAlarm = False
    
    roiImageBase64Updated = pyqtSignal(str) # ROI Creation pipe
    mobFrameBase64Updated = pyqtSignal(str) # MOB cv detection pipe
    detectedPeopleUpdated = pyqtSignal(str) # MOB cv detection pipe
    runningMobPipeStatusChanged = pyqtSignal(bool)
    boatDeckMaskStatusChanged = pyqtSignal(bool)
    mobAlarmChanged = pyqtSignal(bool)

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
    
    @pyqtProperty(str, notify=detectedPeopleUpdated)
    def detectedPeople(self):
        return self._detectedPeople
    
    @detectedPeople.setter
    def detectedPeople(self,value):
        if self._detectedPeople != value:
            self._detectedPeople = value
            self.detectedPeopleChanged.emit(self._detectedPeople)

    @pyqtProperty(bool, notify=runningMobPipeStatusChanged)
    def runningMobPipeStatus(self):
        return self._runningMobPipeStatus

    @runningMobPipeStatus.setter
    def runningMobPipeStatus(self, value):
        if self._runningMobPipeStatus != value:
            self._runningMobPipeStatus = value
            self.runningMobPipeStatusChanged.emit(self._runningMobPipeStatus)
    
    @pyqtProperty(bool, notify=boatDeckMaskStatusChanged)
    def boatDeckMaskStatus(self):
        return self._boatDeckMaskStatus

    @boatDeckMaskStatus.setter
    def boatDeckMaskStatus(self, value):
        if self._boatDeckMaskStatus != value:
            self._boatDeckMaskStatus = value
            self.boatDeckMaskStatusChanged.emit(self._boatDeckMaskStatus)

    @pyqtProperty(bool, notify=mobAlarmChanged)
    def mobAlarmStatus(self):
        return self._mobAlarmStatus

    @mobAlarmStatus.setter
    def mobAlarmStatus(self, value):
        if self._mobAlarmStatus != value:
            self._mobAlarmStatus = value
            self.mobAlarmStatusChanged.emit(self._mobAlarmStatus)