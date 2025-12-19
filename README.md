# Engineering Project
## A navigation and weather device enhancing the safety of amateur inland navigation

<div align="center">

[![PyQt5](https://img.shields.io/badge/GUI_Framework-x?logo=qt&label=PyQt5)](https://pypi.org/project/PyQt5/)
[![Yolo](https://img.shields.io/badge/Computer_Vision-blue?logo=YOLO&label=YOLOv11)](https://github.com/ultralytics)
[![Python](https://img.shields.io/badge/Python-Backend-blue?logo=python&logoColor=yellow)](https://www.python.org)

[![Python tests](https://github.com/AlexSzczygielski/navigation-and-weather-device-enhancing-the-safety-of-amateur-inland-navigation/actions/workflows/python-tests.yml/badge.svg)](https://github.com/AlexSzczygielski/navigation-and-weather-device-enhancing-the-safety-of-amateur-inland-navigation/actions/workflows/python-tests.yml)

</div>

The device is based on RaspberryPi single board computer and utilizes several other modules -  a GSM/GPS hat with 4G cellular internet connection, 7 inch touchscreen, camera - all enclosed in a custom designed, 3D printed case. 

### The project consists of:

- Custom dedicated application with it's **frontend** constructed using `QML - a descriptive language framework`, while **backend** was implemented using a `PyQt 5 framework`.

- Cellular `4G` internet connection,

- Weather forecast and warnings data fetched using `weather API`,

- Current yacht's telemetry (position, speed, etc.) accessed using `GPS`,

- A custom **"Man Overboard Accident" detection system** based on `computer vision` solution,




<div align="center">
<img width = 80%  src= "https://www.agh.edu.pl/repozytoria/__processed__/1/d/csm_N_agh_znak_nazwa_sym_1w_en_9000c48428.webp">
</div>

---

## Usage

### For RaspberryPi Deployment
1. Prepare python and it's virtual enviroment with required packages by running `setup_env_rpi.sh`.
```bash
chmod +x setup_env_rpi.sh
./setup_env_rpi.sh
```
> Please watch installation closely - usually one package does not install on the first run and requires re-running this script once again. *Installation might take up to few minutes*. For further explanation please refer to the [requirements installation section](docs/REQUIREMENTS.md#installation)
2. At first run use:
```bash
chmod +x compile.sh
./compile.sh
 ```
 > This script turns on the `venv` and prepares a `.qrc` file necessary to run the QML GUI. Though not necessary `./compile.sh` can also be run at every start of the application and should provide accurate operation.

 3. Every next run use:
 ```bash
source vevn/bin/activate
python main.py
 ```

### For Local Development
1. Prepare and activate a python virtual enviroment
```bash
python3 -m venv venv
source venv/bin/activate
```
> Note: *Activation command might vary depending on the operating system*
2. Install python dependencies (**ensure you are in venv**)
```bash
pip install -r requirements.txt 
```

---

## Project Structure
```bash
navigation-and-weather-device-enhancing-the-safety-of-amateur-inland-navigation % tree -L1
.
├── app/ # Python application code
├── assets/ # Static GUI resources
├── components/ # Reusable QML components
├── cv/ # CV pipelines and logic
├── data/ # Demo datasets/data
├── docs/ # Documentation
├── models/ # ML weights
├── tests/ # Unit tests
├── views/ # QML GUI
├── main.py # Appliaction entry point
├── main.qml # Main QML UI file
├── qml.qrc # QML Resources
├── config.py # Global project configuration
└── setup_env_rpi.sh # Setup script for RPi
```

---

## Documentation:
### [Project Requirements](docs/REQUIREMENTS.md)
### [UML Class Diagram](docs/UML/class_diagram.md)
### [State Diagrams](docs/STATEDIAGRAMS.md)

---

## Components Overview:

The device consists of:
- [RaspberryPi 4B single-board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- [GSM/GPS 4G HAT](https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT)
- [7-inch touchscreen](https://www.waveshare.com/wiki/7inch_HDMI_LCD_%28C%29)
- [Camera](https://www.waveshare.com/wiki/RPi_Camera_%28G%29)
- Custom 3D printed enclosure

---
<div align="center">
<img width = 20%  src= "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Znak_graficzny_AGH.svg/2048px-Znak_graficzny_AGH.svg.png">
<img width = 20%  src= "https://iet.agh.edu.pl/wp-content/uploads/2021/05/Logo-WIET-2021.png">
</div>

