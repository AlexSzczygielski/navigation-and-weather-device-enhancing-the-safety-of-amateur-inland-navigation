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
        self.model_path = model_path
        self.worker = None
        
    img_ready = pyqtSignal(str)
    imageUpdated = pyqtSignal(str)

    @pyqtSlot()
    def run_cv(self):
        #Run Create ROI pipe
        #Ensure old worker is cleaned up
        if self.worker and self.worker.isRunning():
            print("Previous worker still running")
            return
        self.worker = CvWorker(self.model_path)
        self.worker.finished.connect(self.on_run_cv_finished)
        self.worker.error.connect(self.on_run_cv_error)
        self.worker.start()
        
    def on_run_cv_finished(self, img_path):
        print("finished")
        self.imageUpdated.emit(img_path)

    def on_run_cv_error(self):
        print("error")        


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQmlApplicationEngine()
    view.addImportPath(sys.path[0])
    
    model_path = '/Users/olek_szczygielski/Desktop/AGH/praca_inzynierska/repos/ROI-polygon-exporter/first_model_omega_boat_deck_weights.pt'
    backend = Backend(model_path)
    view.rootContext().setContextProperty("backend",backend)

    #view.load("App/views/home.qml")
    view.load(QUrl("qrc:main.qml"))
    ex = app.exec()

    del view
    sys.exit(ex)