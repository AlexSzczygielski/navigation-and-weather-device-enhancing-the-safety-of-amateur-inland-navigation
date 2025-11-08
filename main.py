#main.py
import sys
import os
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl

import qml_rc
from cv.cv_worker import CvWorker

class Backend(QObject):
    def __init__(self,model_path):
        super().__init__()
        #Create CV class
        self._model_path = model_path
        self._worker = None
        
    img_ready = pyqtSignal(str)
    imageUpdated = pyqtSignal(str)

    @pyqtSlot()
    def run_cv(self):
        #Run Create ROI pipe
        #Ensure old worker is cleaned up
        if self._worker and self._worker.isRunning():
            print("Previous worker still running")
            return
        self._worker = CvWorker(self._model_path)
        self._worker.finished.connect(self._on_run_cv_finished)
        self._worker.error.connect(self._on_run_cv_error)
        self._worker.start()
        
    def _on_run_cv_finished(self, img_path):
        print("finished")
        self.imageUpdated.emit(img_path)

    def _on_run_cv_error(self):
        print("error")        


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