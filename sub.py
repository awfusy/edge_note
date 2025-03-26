import paho.mqtt.client as mqtt
import base64
import cv2
import numpy as np

BROKER = 'localhost'
port = 1883
topic = "webcam/image"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Image Viewer: Connected to MQTT broker")
        client.subscribe(topic)
    else:
        print(f"Image Viewer: Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        image_base64 = msg.payload.decode('utf-8')
        image_bytes = base64.b64decode(image_base64)
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        cv2.imshow("Received Image", image)
        cv2.waitKey(1)
    except Exception as e:
        print(f"Image Viewer: Error decoding image: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, port, 60)
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Image Viewer: Stopping MQTT client")
    client.loop_stop()
    client.disconnect()
