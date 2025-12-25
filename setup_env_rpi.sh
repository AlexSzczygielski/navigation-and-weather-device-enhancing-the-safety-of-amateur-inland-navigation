#!/bin/bash
# setup_env.sh - setup enviroment for PyQt5 + Ultralytics YOLO, OpenCV on RaspberryPi 4B

set -e #stopping on the first error

echo "Updating system"
sudo apt update && sudo apt upgrade -y

echo "Installing Python and pip"
sudo apt install -y python3 python3-pip

echo "Creating and activating python virtual enviroment (with exposure to system-site-packages)"
python3 -m venv --system-site-packages venv
source venv/bin/activate

echo "Updating system"
sudo apt update -y

echo "Ensuring the pip is installed"
sudo apt install -y python3-pip

echo "Upgrading pip inside venv"
pip install -U pip

echo "Install Ultralytics (YOLO) package"
pip install ultralytics

echo "Installing GUI dependencies"

echo "Installing PyQt5 and QML"
sudo apt install -y python3-pyqt5 python3-pyqt5.qtquick python3-pyqt5.qtmultimedia pyqt5-dev-tools

echo "Installing QtQuick dependencies"
sudo apt install -y qml-module-qtquick2 qml-module-qtquick-layouts qml-module-qtquick-controls qml-module-qtquick-controls2

echo "Installing python-gps"
sudo apt install python3-gps

echo "Installing gpsd"
sudo apt install gpsd gpsd-clients
echo "Disabling gps socket mode"
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

echo "Configure gpsd daemon from etc_files gpsd prepared script"
sudo cp sys_conf_files/etc_files/gpsd /etc/default/gpsd

echo "Starting and enabling gpsd"
sudo systemctl enable gpsd
sudo systemctl start gpsd

echo "Copy and enable auto gps start md service"
sudo cp sys_conf_files/systemd_files/sim7600eh-gps.service /etc/systemd/system/sim7600eh-gps.service
sudo systemctl daemon-reload
sudo systemctl enable sim7600eh-gps
sudo systemctl start sim7600eh-gps