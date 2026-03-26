import threading
import time
from abc import abstractmethod

from BaseMqtt import BaseMqtt
import paho.mqtt.client as mqtt

class MqttPublisher(BaseMqtt):
    def __init__(self, client_id, online_topic):
        self.online_topic = online_topic
        self.stop_thread_event = threading.Event()
        super().__init__(
            client_id=client_id,
        )

    def on_connect(self):
        print(f"{self.client_id} publisher connected")

    def on_disconnect(self):
        print(f"{self.client_id} publisher disconnected")

    def on_message(self, client, userdata, msg):
        pass

    def get_online_topic(self):
        return self.online_topic

    def start_publishing(self, publish_interval=2.0):
        self.stop_thread_event.clear()
        threading.Thread(target=self.publish_loop, args=(publish_interval,)).start()

    def publish_loop(self, publish_interval):
        while not self.stop_thread_event.is_set():
            if self.isConnected:
                try:
                    self.publish_data()
                except Exception as e:
                    print(f"{self.client_id} [ERREUR] lors de la publication: {e}")
            else:
                print(f"{self.client_id} [ATTENTE] en attente de connexion MQTT...")

            self.stop_thread_event.wait(publish_interval)

    @abstractmethod
    def publish_data(self):
        pass

    def stop_publishing(self):
        self.stop_thread_event.set()
