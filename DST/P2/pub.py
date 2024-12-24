import paho.mqtt.client as mqtt

# MQTT_BROKER = "test.mosquitto.org"
MQTT_BROKER = "158.42.32.220"
MQTT_PORT = 1883

MQTT_TOPIC = "salon/luz"
MQTT_MSG = input("Introduce valor ON/OFF: ")

cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

cliente.connect(MQTT_BROKER, MQTT_PORT)
print("conectado al broker", MQTT_BROKER)

cliente.publish(MQTT_TOPIC, MQTT_MSG)
print("publicado en el topic", MQTT_MSG, "en el topic: ", MQTT_TOPIC)
cliente.disconnect()
