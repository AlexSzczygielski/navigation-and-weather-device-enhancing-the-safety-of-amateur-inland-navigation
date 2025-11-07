#!/bin/bash
# setup_env.sh - setup enviroment for PyQt5 + Ultralytics YOLO, OpenCV on RaspberryPi 4B

set -e #stopping on the first error

echo "Updating system"
sudo apt update && sudo apt upgrade -y

echo "Installing Python and pip"
sudo apt install -y python3 python3-pip

echo "Creating and activating python virtual enviroment (yolo)"
python3 -m venv --system-site-packages yolo
source yolo/bin/activate

echo "Updating system"
sudo apt update -y

echo "Ensuring the pip is installed"
sudo apt install -y python3-pip

echo "Upgrading pip inside venv"
pip install -U pip

echo "Install Ultralytics (YOLO) package"
pip install ultralytics

echo "Installing GUI dependencies"
sudo apt install 

echo "Installing PyQt5 and QML"
sudo apt install -y python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtmultimedia pyqt5-dev-tools

echo "Installing QtQuick dependencies":
sudo apt install -y qml-module-qtquick2 qml-module-qtquick-layouts qml-module-qtquick-controls qml-module-qtquick-controls2 