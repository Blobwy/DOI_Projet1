import json
import datetime
import Config
import paho.mqtt.client as mqtt
from gpiozero import LED

# Fonction pour publier l'état actuel de la LED (allumée ou éteinte) sur le topic MQTT de l'état
def publish_led_state(client: mqtt.Client):
    if led.is_lit:
        val_state = "on"
    else:
        val_state = "off"

    payload_dict = {
        "device": Config.DEVICE,
        "actuator": "led",
        "state": val_state,
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    payload_json = json.dumps(payload_dict)
    client.publish(Config.TOPIC_STATE, payload_json, qos=1, retain=True)
    print(f" [STATE] {Config.TOPIC_STATE} -> {payload_json}")

# Fonction pour tenter de parser le payload JSON et extraire le champ "state" si disponible et valide ("on" ou "off")
def parse_command(payload_text: str) -> str | None:
    try:
        data = json.loads(payload_text)
        if "state" in data:
            s = str(data["state"]).lower().strip()
            if s in ("on", "off"): return s
    except:
        pass
    return None

# Callback appelé lors de la connexion au broker MQTT
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f" [CONNECT] connecté au broker (code {reason_code})")
    if reason_code == 0:
        client.publish(Config.TOPIC_ONLINE, payload="online", qos=1, retain=True)
        client.subscribe(Config.TOPIC_CMD, qos=1)
        print(f" [SUB] Abonné à : {Config.TOPIC_CMD}")
        publish_led_state(client)

# Callback appelé lors de la réception d'un message sur un topic abonné
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8", errors="replace")
    print(f"[MSG] Topic: {msg.topic} | Payload: {payload}")
    
    command = parse_command(payload)
    if command == "on":
        led.on()
    elif command == "off":
        led.off()
    else:
        print("[WARN] Commande JSON invalide reçue")
        return

    publish_led_state(client)

led = LED(Config.LED_PIN_BCM)

# Créer une instance de client MQTT avec un ID unique et le protocole MQTT v3.1.1
client = mqtt.Client(client_id=Config.LED_CLIENT_ID, protocol=mqtt.MQTTv311)
client.will_set(Config.TOPIC_ONLINE, payload="offline", qos=1, retain=True)
client.on_connect = on_connect
client.on_message = on_message

client.connect(Config.MQTT_BROKER_HOST, Config.MQTT_BROKER_PORT, keepalive=Config.MQTT_KEEPALIVE)
print("[INFO] Subscriber LED démarré. En attente de commandes...")
client.loop_forever()