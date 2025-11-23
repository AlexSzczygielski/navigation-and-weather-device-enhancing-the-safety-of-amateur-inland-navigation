# Engineering Thesis
## A navigation and weather device enhancing the safety of amateur inland navigation
The device is based on RaspberryPi single board computer and utilizes several other modules -  a GSM/GPS hat with 4G cellular internet connection, 7 inch touchscreen, camera - all enclosed in a custom designed, 3D printed case. 

### The project consists of:

- Custom GUI built on top of linux operating system,

- Cellular internet connection,

- Weather forecast and warnings data fetched via API,

- Current yacht's telemetry (position, speed, etc.),

- A custom Man Overboard detection system based on computer vision solution,


<div align="center">

[![PyQt5](https://img.shields.io/badge/GUI_Framework-x?logo=qt&label=PyQt5)](https://pypi.org/project/PyQt5/)
[![Yolo](https://img.shields.io/badge/Computer_Vision-blue?logo=YOLO&label=YOLOv11)](https://github.com/ultralytics)
[![Python](https://img.shields.io/badge/Python-Backend-blue?logo=python&logoColor=yellow)](https://www.python.org)

</div>

<div align="center">
<img width = 80%  src= "https://www.agh.edu.pl/repozytoria/__processed__/1/d/csm_N_agh_znak_nazwa_sym_1w_en_9000c48428.webp">
</div>

---

## Documentation:
### [UML Class Diagram](UML/class_diagram.md)

---

## Components Overview:

The device consists of:
- [RaspberryPi 4B single-board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- [GSM/GPS 4G HAT](https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT)
- [7-inch touchscreen](https://www.waveshare.com/wiki/7inch_HDMI_LCD_%28C%29)
- [Camera](https://www.waveshare.com/wiki/RPi_Camera_%28G%29)
- Custom 3D printed enclosure
