import paho.mqtt.client as mqtt
import time


def on_message(client, userdata, message):
    print(
        "Mensaje recibido: ",
        str(message.payload.decode("utf-8")) + "en el topic: " + message.topic,
    )


# MQTT_BROKER = "test.mosquitto.org"
MQTT_BROKER = "158.42.32.220"
MQTT_PORT = 1883

MQTT_TOPIC = "salon/#"

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente.on_message = on_message

cliente.connect(MQTT_BROKER, MQTT_PORT)
print("conectado al broker", MQTT_BROKER)

cliente.subscribe(MQTT_TOPIC)
print("suscrito al topic", MQTT_TOPIC)

cliente.loop_start()
time.sleep(15)
cliente.loop_stop()

cliente.disconnect()
