import time
import machine
from network_espnow import SensorBase

class SensorMHZ19(SensorBase):
    def __init__(self, peer_mac):
        super().__init__(peer_mac)

    def send_sensor_data(self):
        for i in range(100):
            self.e.send(self.peer_mac, str(i))
            print("Mensaje enviado:", i)
            time.sleep(2)