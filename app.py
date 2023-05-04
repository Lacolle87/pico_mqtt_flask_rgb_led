import os

from flask import Flask, render_template, request
from dotenv import load_dotenv
import paho.mqtt.client as mqtt


app = Flask(__name__)

load_dotenv()

# Define the MQTT broker address and port
BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
BROKER_PORT = 1883

# Define the MQTT topic to publish to and subscribe to
TOPIC = os.getenv('TOPIC')

# Define the MQTT client ID
CLIENT_ID = os.getenv('CLIENT_ID')

# Define the MQTT username and password
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

# Define the MQTT client
mqtt_client = mqtt.Client(CLIENT_ID)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)


# Define the on_connect callback function to print the MQTT status
def on_connect(client, userdata, flags, rc):
    print(f"MQTT Connected with result code {rc}")
    # Subscribe to the LED topic on connection
    mqtt_client.subscribe(TOPIC)


# Add the on_connect callback function to the mqtt_client object
mqtt_client.on_connect = on_connect


# Start the MQTT client loop
mqtt_client.loop_start()


@app.route("/", methods=["GET", "POST"])
def home():
    # print(request.form)
    if request.method == "POST":
        if 'color' in request.form:
            rgb = request.form['color']
            print(f"Received RGB: {rgb}")
            mqtt_client.publish(TOPIC, rgb)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
