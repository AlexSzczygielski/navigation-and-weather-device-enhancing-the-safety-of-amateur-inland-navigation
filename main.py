#main.py
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QUrl
import platform

import qml_rc # DON'T DELETE
from app.factories import create_backend

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
    view.rootContext().setContextProperty("cv_backend",backend.cv)
    view.load(QUrl("qrc:main.qml"))

    # Start the app full screen
    if platform.system() == 'Linux':
        window = view.rootObjects()[0]
        window.showFullScreen()

    return app, view, backend


if __name__ == "__main__":
    # Entry point - create app and run it
    app, view, backend = create_app()
    ex = app.exec()

    # After Qt app finishes
    del view
    sys.exit(ex)