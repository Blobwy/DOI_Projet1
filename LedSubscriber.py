import json

import Config
from MqttSubscriber import MqttSubscriber
from gpiozero import LED

class LedSubscriber(MqttSubscriber):
    def __init__(self):
        super().__init__(
            client_id=Config.LED_CLIENT_ID,
            online_topic=Config.TOPIC_ONLINE,
        )
        self.cmd_topic = Config.TOPIC_CMD
        self.topic_state = Config.TOPIC_STATE
        self.led = LED(Config.LED_PIN_BCM)

    def subscribe_topic(self):
        self.subscribe(self.cmd_topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        command = self.parse_command(payload)
        if command == "on":
            self.led.on()
        elif command == "off":
            self.led.off()
        else:
            print("[WARN] Commande JSON invalide reçue")
            return

    def parse_command(self, payload):
        try:
            data = json.loads(payload)
            if "state" in data:
                state = str(data["state"]).lower().strip()
                if state in ("on", "off"):
                    return state
        except Exception as e:
            print(f"[ERROR] Failed to parse command: {e}")
        return None

tmp = LedSubscriber()
tmp.connect()