#main.py
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QUrl

import qml_rc # DON'T DELETE
from factories.create_backend import create_backend

def create_app():
    # Composition function - it wires together all components required to start an app
    app = QGuiApplication(sys.argv)
    view = QQmlApplicationEngine()
    view.addImportPath(sys.path[0])
    
    #backend = create_backend()
    backend = create_backend()
    view.rootContext().setContextProperty("backend",backend)

    #view.load("App/views/home.qml")
    view.load(QUrl("qrc:main.qml"))

    return app, view, backend


if __name__ == "__main__":
    # Create app and run it
    app, view, backend = create_app()
    ex = app.exec()

    # After Qt app finish
    del view
    sys.exit(ex)