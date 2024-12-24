import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

MQTT_BROKER = "158.42.32.220"
MQTT_PORT = 1883
MQTT_TOPIC_PETICION = "DST/PETICION"
MQTT_TOPIC_CODIGO = "DST/CODIGO"
MQTT_TOPIC_SOLUCION = "DST/SOLUCION"

DNI = "44895422"
EMAIL = "ojimbou@ade.upv.es"
NAME = "Oscar Jimenez Bou"
USERNAME = "dst"
PASSWORD = "dst"


def on_message(client: mqtt.Client, _, message: mqtt.MQTTMessage):
    response = message.payload.decode("utf-8")
    print(f"Received message: {response} in topic: {message.topic}")

    solution = f"{response};{NAME};{EMAIL}"
    client.publish(MQTT_TOPIC_SOLUCION, solution)

    client.disconnect()
    client.loop_stop()


client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.username_pw_set(USERNAME, PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT)
print("Connected to broker: ", MQTT_BROKER)

client.subscribe(MQTT_TOPIC_CODIGO)
print("Subscribed to topic: ", MQTT_TOPIC_CODIGO)

client.publish(MQTT_TOPIC_PETICION, DNI)
print(f"{DNI} published to topic: ", MQTT_TOPIC_PETICION)

client.loop_forever()
