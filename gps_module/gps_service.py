#gps_service.py

import serial
import config

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

            serial_AT.close()
        except (serial.SerialException) as e:
            print(f"Serial exception {e}")
        finally:
            if serial_AT and serial_AT.is_open:
                serial_AT.close()

if __name__ == "__main__":
    service = GpsService()
    service.start_gps_service()