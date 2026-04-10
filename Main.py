from typing import List
from BaseMqtt import BaseMqtt
from MariadbLogger import MariadbLogger
from TemperatureSensor import TemperatureSensor
#from LedSubscriber import LedSubscriber

class IoTSystem:
    def __init__(self):
        self.clients : List[BaseMqtt] = []
        self.running = False

    def add_client(self, client):
        self.clients.append(client)

    def start(self):
        self.running = True
        for client in self.clients:
            client.connect()
            if hasattr(client, "start_publishing"):
                client.start_publishing()
        print("IoT System started")

    def stop(self):
        self.running = False
        for client in self.clients:
            if hasattr(client, "stop_publishing"):
                client.stop_publishing()
            client.disconnect()
        print("IoT System stopped")

    def run(self):
        try:
            self.start()
            while self.running:
                pass
        except KeyboardInterrupt:
            print("\n[STOP] arrêt demandé (Ctrl+C)")
        finally:
            self.stop()

def main():
    system = IoTSystem()

    system.add_client(TemperatureSensor())
    #system.add_client(LedSubscriber())
    system.add_client(MariadbLogger())

    system.run()

if __name__ == "__main__":
    main()