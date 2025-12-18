#main.py
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QUrl

import qml_rc # DON'T DELETE
from factories.create_backend import create_backend

def create_app():
    # Composition function - it wires together all components required to start an app
    # Create Qt app and QML engine (view)
    app = QGuiApplication(sys.argv)
    view = QQmlApplicationEngine()
    view.addImportPath(sys.path[0])
    
    # Create backend class, expose it to QML engine. 
    # Load qrc resources
    backend = create_backend()
    view.rootContext().setContextProperty("backend",backend)
    view.load(QUrl("qrc:main.qml"))

    return app, view, backend


if __name__ == "__main__":
    # Entry point - create app and run it
    app, view, backend = create_app()
    ex = app.exec()

    # After Qt app finishes
    del view
    sys.exit(ex)