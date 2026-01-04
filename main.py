#main.py
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine 
from PyQt5.QtCore import QUrl
import platform

# Set new process start method to 'spawn' - for correct YOLO initialization in vid processor
from multiprocessing import set_start_method
try:
    set_start_method('spawn')
except RuntimeError:
    pass #Already set

import qml_rc # DON'T DELETE
from app.factories import create_backend

def create_app():
    # Composition function - it wires together all components required to start an app
    # Create Qt app and QML engine
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    
    # Create backend classes, expose them to QML engine. 
    backend = create_backend()
    engine.rootContext().setContextProperty("backend",backend)
    engine.rootContext().setContextProperty("cv_backend",backend.cv)
    engine.rootContext().setContextProperty("gnss_backend",backend.gps)
    engine.rootContext().setContextProperty("weather_backend",backend.weather_backend)

    # Load qrc resources
    engine.load(QUrl("qrc:main.qml"))

    # Start the app full screen on Linux
    if platform.system() == 'Linux':
        window = engine.rootObjects()[0]
        window.showFullScreen()

    return app, engine, backend


if __name__ == "__main__":
    # Entry point - create app and run it
    app, engine, backend = create_app()
    ex = app.exec()

    # Clean up after Qt app finishes
    del engine
    sys.exit(ex)