# Project Requirements

1. Programming Languages & Libraries
- Python 3.x
    - Libraries:
        - [PyQt5](https://packages.debian.org/search?keywords=python3-pyqt5) - QtQuick, Multimedia, DevTools, QtQml
        - [Ultralytics](https://pypi.org/project/ultralytics/)
        - [OpenCV](https://pypi.org/project/opencv-python/)
        - [NumPy](https://pypi.org/project/numpy/)
- QML (GUI)
    - Modules:
        - QtQuick 2
        - QtQuick Layouts
        - QtQuick Controls
        - QtQuick Controls 2

2. Code Structure
- 

3. Usability
- 

4. Documentation
- 

5. Installation
- To run this application on RaspberryPi **it is necessary to expose the python virtual enviroment to system site packages (`python3 -m venv --system-site-packages venv`)**.

> For the time of the project creation there is an issue with PyQt5 packages - their pip source is broken and they have to be installed globally via sudo apt install. In this kind of setup venv has to be exposed to system packages in order to see PyQt5 modules and import them.
    