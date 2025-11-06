#cv_worker.py
#Class responsible for managing QThreading for cv_service.py logic
from PyQt5.QtCore import QThread, pyqtSignal
import os
from cv.cv_service import CvService


class CvWorker(QThread):
    def __init__()
    finished = pyqtSignal(str)
    error = pyqtSignal(str)