import sys
import os
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl

import qml_rc
from cv.cv_service import CvService


class Backend(QObject):
    def __init__(self,model_path):
        super().__init__()
        try:
            #Create CV class
            self.model_path = model_path
            self.cv_proc = CvService(model_path)
        except Exception as e:
            print(f"Failed to initialize CV module: {e}")
            self.cv_proc = None
        
    img_ready = pyqtSignal(str)
    imageUpdated = pyqtSignal(str)

    @pyqtSlot()
    def run_cv(self):
        #Run Create ROI pipe
        mask_coords = self.cv_proc.mask_exporter()
        self.cv_proc.mask_painter()
        try:
            img_path = os.path.abspath('output_mask.jpg')
            self.imageUpdated.emit(img_path)
        except Exception as e:
            print(f"Failed to load painted mask image: {e}")        


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