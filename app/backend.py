#backend.py
"""This module contains Backend class - wrapper of all backends used in this app."""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QProcess, QUrl
from app.cv_backend import CvBackend

class Backend(QObject):
    """
    Backend - a wrapper class composed of all service backends used in an app.

    It is created by passing ready to use backend objects.
    There is a file factories.py containing construction functions
    for all service backends as well as this backend."
    """
    def __init__(self, CvBackend):
        super().__init__()
        self.cv = CvBackend

    @pyqtSlot()
    def shutdown_all(self):
        self.cv.shutdown()