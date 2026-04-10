from abc import abstractmethod, ABC
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import Config

class BaseMqtt(ABC):
    def __init__(self, client_id):
        self.client_id = client_id
        self.broker_host = Config.MQTT_BROKER_HOST
        self.broker_port = Config.MQTT_BROKER_PORT
        self.keepalive = Config.MQTT_KEEPALIVE
        self.isConnected = False
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv311)
        self.setupCallbacks()
        self.client.will_set = self.setupWillMessage

    def setupCallbacks(self):
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    # appeler quand la connexion est perdue
    def setupWillMessage(self):
        self.client.will_set(
            self.get_online_topic(),
            payload="Offline",
            qos=1,
            retain=True
        )

    def _on_connect(self, client, userdata, flags, rc):
        print(f"{self.client_id} [CONNECTER] avec le code={rc}")
        self.isConnected = (rc == 0)
        if self.isConnected:
            self.client.publish(
                self.get_online_topic(),
                payload="Online",
                qos=1,
                retain=True
            )
            self.on_connect()
        else:
            print(f"{self.client_id} [ERREUR] échec de connexion au broker MQTT")

    def _on_disconnect(self, client, userdata, rc):
        print(f"{self.client_id} [DECONNECTER] avec le code={rc}")
        self.isConnected = False
        self.on_disconnect()

    def _on_message(self, client, userdata, msg):
        try:
            self.on_message(client, userdata, msg)
        except Exception as e:
            print(f"{self.client_id} [ERREUR] dans on_message: {e}")

    def connect(self):
        self.client.connect(self.broker_host, self.broker_port, keepalive=self.keepalive)
        self.client.reconnect_delay_set(min_delay=1, max_delay=30)
        self.client.loop_start()

    def disconnect(self):
        try:
            self.client.publish(
                self.get_online_topic(),
                payload="Offline",
                qos=1,
                retain=True
            )
        except Exception as e:
            print(f"{self.client_id} [ERREUR] lors de la déconnexion: {e}")

        self.client.disconnect()
        self.client.loop_stop()

    def publish(self, topic, payload, qos=0, retain=False):
        if self.isConnected:
            self.client.publish(topic, payload=payload, qos=qos, retain=retain)
        else:
            print(f"{self.client_id} [ERREUR] impossible de publier, client non connecté")

    def subscribe(self, topic, qos=0):
        if self.isConnected:
            self.client.subscribe(topic, qos=qos)
        else:
            print(f"{self.client_id} [ERREUR] impossible de s'abonner, client non connecté")

    @staticmethod
    def get_time_now():
        return datetime.now(timezone.utc).isoformat()

    @abstractmethod
    def get_online_topic(self):
        pass

    @abstractmethod
    def on_connect(self):
        pass

    @abstractmethod
    def on_message(self, client, userdata, msg):
        pass

    @abstractmethod
    def on_disconnect(self):
        pass