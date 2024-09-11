import paho.mqtt.client as mqtt
import threading
import stateSpace
import readSerial
import time

ADDR, port = 'localhost', 1883
topic1 = 'output/state_space'
topic2 = 'output/state_space_info'
client = mqtt.Client()
client.connect(ADDR, port)

def publish_data():
    while not readSerial.stop_event.is_set():
        with stateSpace.y_lock:
            if stateSpace.y is not None:
                output = stateSpace.y
                info = stateSpace.info
                client.publish(topic1, output)
                client.publish(topic2, info)
        time.sleep(1)

serial_thread = threading.Thread(target=readSerial.read_serial)
simulation_thread = threading.Thread(target=stateSpace.stateSpaceCalculation)
publisher_thread = threading.Thread(target=publish_data)

serial_thread.start()
simulation_thread.start()
publisher_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    readSerial.stop_event.set()
    serial_thread.join()
    simulation_thread.join()
    publisher_thread.join()
    client.disconnect()