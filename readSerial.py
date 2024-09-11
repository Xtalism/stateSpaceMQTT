import serial
import threading

data = None
stop_event = threading.Event()

def read_serial():
    global data
    with serial.Serial('COM4', 115200) as arduino:
        while not stop_event.is_set():
            try:
                data = arduino.readline().decode().strip()
            except serial.SerialException:
                break