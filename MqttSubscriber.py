from abc import abstractmethod

from BaseMqtt import BaseMqtt

class MqttSubscriber(BaseMqtt):
    def __init__(self, client_id, online_topic):
        super().__init__(
            client_id=client_id,
        )
        self.online_topic = online_topic

    def on_connect(self):
        print(f"{self.client_id} subscriber connected")
        self.subscribe_topic()

    def on_disconnect(self):
        print(f"{self.client_id} subscriber disconnected")

    def get_online_topic(self):
        return self.online_topic

    @abstractmethod
    def subscribe_topic(self):
        pass

    @abstractmethod
    def on_message(self, client, userdata, msg):
        pass