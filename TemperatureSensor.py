import json
import Config
import random
from MqttPublisher import MqttPublisher

class TemperatureSensor(MqttPublisher):
    def __init__(self):
        super().__init__(
            client_id = Config.SENSOR_PUB_CLIENT_ID,
            online_topic = Config.TOPIC_ONLINE,
        )

    def publish_data(self):
        temperature = self.get_random_temperature()
        payload = {
            "sensor": "temperature",
            "value": temperature,
            "unit": "C",
            "ts": self.get_time_now()
        }
        self.publish(Config.TOPIC_JSON_TEMP, json.dumps(payload), qos=Config.QOS_SENSOR_TEMP)
        self.publish(Config.TOPIC_VALUE_TEMP, str(temperature), qos=Config.QOS_SENSOR_TEMP)
        print(payload)

    def get_random_temperature(self):
        return round(random.uniform(0.0, 40.0), 2)

tmp = TemperatureSensor()
tmp.connect()
tmp.start_publishing()