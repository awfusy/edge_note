import paho.mqtt.client as mqtt
import cv2
import base64
import time

BROKER = 'localhost'
port = 1883
subscribe_topic = "webcam/capture"
publish_topic = "webcam/image"
camera_index = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Webcam Publisher: Connected to MQTT broker")
        client.subscribe(subscribe_topic)
    else:
        print(f"Webcam Publisher: Connection failed with code {rc}")

def on_message(client, userdata, msg):
    if msg.topic == subscribe_topic:
        print("Webcam Publisher: Capture request received")
        capture_and_publish(client)

def capture_and_publish(client):
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Webcam Publisher: Error: Could not open webcam.")
            return

        ret, frame = cap.read()
        cap.release()

        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            client.publish(publish_topic, image_base64)
            print("Webcam Publisher: Image captured and published")
        else:
            print("Webcam Publisher: Error: Failed to capture image.")
    except Exception as e:
        print(f"Webcam Publisher: Error during capture and publish: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, port, 60)
client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Webcam Publisher: Stopping MQTT client")
    client.loop_stop()
    client.disconnect()
