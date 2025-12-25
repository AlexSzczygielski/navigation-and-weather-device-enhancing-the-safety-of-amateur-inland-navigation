#gps_service.py

import serial
from config import config

class GpsService():
    def __init__(self):
        pass

    def send_AT(self,serial_port: serial.Serial, message: str):
        """Encodes the AT message and sends it through serial port."""
        message_encoded = f"{message}\r\n".encode()
        serial_port.write(message_encoded)

    def send_and_verify_AT(self,serial_port: serial.Serial, message: str) -> bool:
        """
        Encodes, sends (using send_AT) the AT command and checks if it returns OK code.

        This method should be used with simple, AT commands returning only 'OK'
        Ensure the command used here returns **ONLY** 'OK'
        """
        
        self.send_AT(serial_port=serial_port, message=message)
        serial_response = serial_port.readline().decode(errors="ignore").strip()
        return serial_response == 'OK'
    
    def start_gps_service(self):
        serial_AT = serial.Serial(
            port=config.AT_SERIAL_PORT,
            baudrate=config.AT_BAUD_RATE,
            timeout=config.AT_TIMEOUT
        )
        try:
            if not self.send_and_verify_AT(serial_AT,"AT"): #Test AT connection
                raise serial.SerialException("AT connection failed")
            
            if not self.send_and_verify_AT(serial_AT,"AT+CGPS=1"): #Open GPS
                raise serial.SerialException("GPS initialization failed")
            
            self.send_AT(serial_AT, "AT+CGPSNMEAPORTCFG=3") #Configure NMEA port output
            self.send_AT(serial_AT, "AT+CGPSNMEA=197119") # Enable NMEA sentences
            self.send_AT(serial_AT, "AT+CGPSINFOCFG=10,31") # GPS info fields passed in NMEA
            self.send_AT(serial_AT, "AT+CGPSAUTO=1") # GPS auto start at reboot

            serial_AT.close()
        except (serial.SerialException) as e:
            print(f"Serial exception {e}")
        finally:
            if serial_AT and serial_AT.is_open:
                serial_AT.close()

    def read_gps_output(self):
        serial_gps_out = serial.Serial(
            port=config.GPS_SERIAL_PORT,
            baudrate=config.GPS_BAUD_RATE,
            timeout=config.GPS_TIMEOUT
        )

        while True:
            gps_out_line = serial_gps_out.readline().decode(errors="ignore").strip()
            if gps_out_line.startswith("$"):
                print(gps_out_line)

if __name__ == "__main__":
    service = GpsService()
    GpsService.start_gps_service()
    GpsService.read_gps_output()