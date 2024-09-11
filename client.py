import paho.mqtt.client as mqtt

class MQTTClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        
        self.output_state_space = 'output/state_space'
        self.output_state_space_info = 'output/state_space_info'
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message  # callback
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.output_state_space)
        self.client.subscribe(self.output_state_space_info)
        
    def on_message(self, client, userdata, msg):
        if msg.topic == self.output_state_space:
            print(str(msg.payload.decode()))  # message carried
        elif msg.topic == self.output_state_space_info:
            print(str(msg.payload.decode()))
        
if __name__ == '__main__':
    mqtt_client = MQTTClient('127.0.0.1', 1883)