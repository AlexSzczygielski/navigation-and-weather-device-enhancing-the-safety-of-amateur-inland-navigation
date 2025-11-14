#main.py
import sys
import os
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl

import qml_rc
from cv.cv_worker import CvWorker
from cv.cv_state import CvState
from cv.cv_demo_state_service import CvDemoStateService

class Backend(QObject):
    def __init__(self,model_path):
        super().__init__()
        self._model_path = model_path
        self._worker = None
        self._roi_img_base_64 = None
        
    ### ROI CREATION PIPE ###
    imageUpdated = pyqtSignal(str)

    @pyqtSlot()
    def run_cv_roi_pipe(self):
        #Run Create ROI pipe
        try:
            #Ensure old worker is cleaned up
            if self._worker and self._worker.isRunning():
                print("Previous worker still running")
                return

            self._worker = CvWorker(self._model_path,CvDemoStateService()) #worker with context
            self._worker.finished.connect(self._on_run_cv_roi_pipe_finished)
            self._worker.error.connect(self._on_run_cv_roi_pipe_error)
            self._worker.finished.connect(self._worker.deleteLater)
            self._worker.start()
        except Exception as e:
            print(f"{self.__class__.__name__}.run_cv_roi_pipe error: {e}")

    def _on_run_cv_roi_pipe_finished(self, img_64):
        self._roi_img_base_64 = img_64
        self.imageUpdated.emit(self._roi_img_base_64)
        self._worker = None #Release the reference

    def _on_run_cv_roi_pipe_error(self):
        print("error")

    @pyqtSlot(result=str)
    def get_roi_img(self):
        #This can be used when loading/reloading the cv_create_roi_panel view
        if self._roi_img_base_64 is None:
            return None
        return self._roi_img_base_64

    ### MOB CV DETECTION PIPE ###

    frameUpdated = pyqtSignal(str)        

    @pyqtSlot()
    def run_cv_mob_detect_pipe(self):
        #Runs mob detection system
        try:
            if self._worker and self._worker.isRunning():
                print("Previous worker still running")
                return
            
            self._worker = CvWorker(self._model_path,CvDemoStateService()) #worker with context
            self._worker.finished.connect(self._on_run_cv_mob_detect_pipe_finished)
            self._worker.error.connect(self._on_run_cv_mob_detect_pipe_error)
            self._worker.finished.connect(self._worker.deleteLater)
            self._worker.start()
        except Exception as e:
            print(f"{self.__class__.__name__}.run_cv_mob_detect_pipe error: {e}")

    def _on_run_cv_mob_detect_pipe_finished(self, img64):
        self._worker = None

    def _on_run_cv_mob_detect_pipe_error(self):
        pass
        

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQmlApplicationEngine()
    view.addImportPath(sys.path[0])
    
    _model_path = 'cv/first_model_omega_boat_deck_weights.pt'
    backend = Backend(_model_path)
    view.rootContext().setContextProperty("backend",backend)

    #view.load("App/views/home.qml")
    view.load(QUrl("qrc:main.qml"))
    ex = app.exec()

    del view
    sys.exit(ex)