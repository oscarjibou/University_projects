import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = "158.42.32.220"
MQTT_PORT = 1883
MQTT_TOPIC_PETICION = "DST/PETICION"
MQTT_TOPIC_CODIGO = "DST/CODIGO"
MQTT_TOPIC_SOLUCION = "DST/SOLUCION"

DNI = os.getenv("DNI")
EMAIL = os.getenv("EMAIL")
NAME = os.getenv("NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def on_message(
    client: mqtt.Client, _, message: mqtt.MQTTMessage
):  # se ejecuta cuando llega un mensaje a un topic al que estamos suscritos
    response = message.payload.decode(
        "utf-8"
    )  # decodificamos el mensaje que llega a utf-8
    print(f"Received message: {response} in topic: {message.topic}")

    solution = f"{response};{NAME};{EMAIL}"  # creamos la solucion con el mensaje que llega, nuestro nombre y email
    client.publish(
        MQTT_TOPIC_SOLUCION, solution
    )  # publicamos la solucion en el topic DST/SOLUCION

    client.disconnect()
    client.loop_stop()


client = mqtt.Client(
    CallbackAPIVersion.VERSION2
)  # creamos el cliente mqtt con la version 2
client.on_message = on_message  # asignamos la funcion on_message al evento on_message
client.username_pw_set(
    USERNAME, PASSWORD
)  # asignamos el usuario y contraseña al cliente mqtt
client.connect(MQTT_BROKER, MQTT_PORT)  # conectamos el cliente al broker
print("Connected to broker: ", MQTT_BROKER)

client.subscribe(MQTT_TOPIC_CODIGO)  # nos suscribimos al topic DST/CODIGO
print("Subscribed to topic: ", MQTT_TOPIC_CODIGO)

client.publish(MQTT_TOPIC_PETICION, DNI)
print(f"{DNI} published to topic: ", MQTT_TOPIC_PETICION)

client.loop_forever()
