import network
import _thread
import time
from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import neopixel
from config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    BROKER_ADDRESS,
    BROKER_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
    TOPIC,
    CLIENT_ID,
)

# Define the neopixel settings
NUM_LEDS = 3
PIXEL_PIN = 0
np = neopixel.NeoPixel(Pin(PIXEL_PIN), NUM_LEDS)

# Define rainbow mode variable
rainbow_mode = False


def wheel(pos):
    # Generate rainbow colors across 0-255 positions
    if pos < 85:
        return pos * 3, 255 - pos * 3, 0
    elif pos < 170:
        pos -= 85
        return 255 - pos * 3, 0, pos * 3
    else:
        pos -= 170
        return 0, pos * 3, 255 - pos * 3


def rainbow_cycle():
    global rainbow_speed
    # Cycle through rainbow colors on neopixels
    for j in range(255):
        for i in range(NUM_LEDS):
            idx = int((i * 256 / NUM_LEDS) + j)
            np[i] = wheel(idx & 255)
        np.write()
        time.sleep(rainbow_speed)
        if not rainbow_mode:
            break


def neo_thread():
    global rainbow_mode, rainbow_speed
    while True:
        if rainbow_mode:
            rainbow_cycle()
        else:
            time.sleep(0.01)


# Start the thread
_thread.start_new_thread(neo_thread, ())


def callback(topic, message):
    # Define the callback function to handle received messages
    global rainbow_mode, rainbow_speed
    print("Received message: {} on topic: {}".format(message, topic))
    if message.startswith(b"rgb"):
        rainbow_mode = False
        rgb = message.decode().split(":")[1].split(",")
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        np[0] = (r, g, b)
        np[1] = (r, g, b)
        np[2] = (r, g, b)
        np.write()
    elif message.startswith(b"rainbow"):
        # Turn on rainbow mode
        rainbow_mode = True
        # Extract the speed from the message
        speed = message.decode().split(".")[-1]
        # Convert the speed to a float and update the rainbow_speed variable
        rainbow_speed = float(speed) / 1000


def wifi_connect():
    # Connect to the Wi-Fi network
    print("Connecting to WiFi network...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to WiFi network.")
    status = wlan.ifconfig()
    print("ip = " + status[0])


def mqtt_connect():
    # Connect to the MQTT broker
    print("Connecting to MQTT broker...")
    mqtt_client = MQTTClient(
        CLIENT_ID,
        BROKER_ADDRESS,
        BROKER_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        keepalive=300,
    )
    mqtt_client.set_callback(callback)

    while True:
        try:
            mqtt_client.connect()
            mqtt_client.subscribe(TOPIC)
            print("Connected to MQTT broker.")
            break
        except OSError as e:
            print("Connection failed:", e)
            sleep(1)

    # Loop to wait for incoming messages
    while True:
        try:
            mqtt_client.check_msg()
            time.sleep(0.01)
        except OSError as e:
            print("Connection lost, trying to reconnect...", e)
            mqtt_client.disconnect()
            while True:
                try:
                    mqtt_client.connect()
                    mqtt_client.subscribe(TOPIC)
                    print("Reconnected to MQTT broker.")
                    break
                except OSError as e:
                    print("Reconnection failed:", e)
                    time.sleep(1)


def main():
    wifi_connect()
    mqtt_connect()


main()
