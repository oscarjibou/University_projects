import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, reason_code, properties):
    global FLAG
    print("Conectado al callback")
    FLAG = False


broker_address = "158.42.32.220"

client = mqtt.Client(mqtt.CallbakcAPIVersion.VERSION2)
client.on_connect = on_connect
client.loop_start()

client.connect(broker_address)

FLAG = True
counter = 0

while FLAG:
    print("Esperando conexión", counter)
    time.sleep(1)
    counter += 1
    if counter > 50:
        print("No se ha podido conectar")
        break

client.disconnect()
client.loop_stop()
