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
cycle_mode = False
sync_mode = False


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
    global speed
    # Cycle through rainbow colors on neopixels
    for j in range(255):
        for i in range(NUM_LEDS):
            idx = int((i * 256 / NUM_LEDS) + j)
            np[i] = wheel(idx & 255)
        np.write()
        time.sleep(speed)
        if not rainbow_mode:
            break


def sync():
    global speed
    colors = [wheel(j) for j in
              range(256)]  # Generate colors for all 256 positions
    j = 0  # Initialize j variable
    while True:
        color = colors[j % 256]
        for i in range(NUM_LEDS):
            np[i] = color  # Set the LED color to the current color
        np.write()
        time.sleep(speed)
        j += 1  # Increment j variable
        if not sync_mode:
            break


def cycle():
    global speed
    gradient_segments = [(0.0, (255, 0, 0)),
                         (0.2, (255, 127, 0)),
                         (0.4, (255, 255, 0)),
                         (0.6, (0, 255, 0)),
                         (0.8, (0, 0, 255)),
                         (1.0, (75, 0, 130))]
    for j in range(255):
        for i in range(NUM_LEDS):
            offset = i / NUM_LEDS
            for idx in range(len(gradient_segments) - 1):
                if gradient_segments[idx + 1][0] > offset:
                    break
            segment_offset = (offset - gradient_segments[idx][0]) / (gradient_segments[idx + 1][0] - gradient_segments[idx][0])
            color1, color2 = gradient_segments[idx][1], gradient_segments[idx + 1][1]
            color = tuple(int(c1 * (1 - segment_offset) + c2 * segment_offset) for c1, c2 in zip(color1, color2))
            np[i] = color
        np.write()
        time.sleep(speed * 25)
        gradient_segments = gradient_segments[1:] + [gradient_segments[0]]
        if not cycle_mode:
            break


def neo_thread():
    global rainbow_mode, cycle_mode, sync_mode, speed
    while True:
        if rainbow_mode:
            rainbow_cycle()
        elif cycle_mode:
            cycle()
        elif sync_mode:
            sync()
        else:
            time.sleep(0.01)


# Start the thread
_thread.start_new_thread(neo_thread, ())


def callback(topic, message):
    # Define the callback function to handle received messages
    global rainbow_mode, cycle_mode, sync_mode, speed
    print("Received message: {} on topic: {}".format(message, topic))
    if message.startswith(b"rgb"):
        rainbow_mode = False
        cycle_mode = False
        sync_mode = False
        rgb = message.decode().split(":")[1].split(",")
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        np[0] = (r, g, b)
        np[1] = (r, g, b)
        np[2] = (r, g, b)
        np.write()
    else:
        mode = message.split(b".")[0]
        if mode == b"rainbow":
            rainbow_mode = True
            cycle_mode = False
            sync_mode = False
        elif mode == b"cycle":
            rainbow_mode = False
            cycle_mode = True
            sync_mode = False
        elif mode == b"sync":
            rainbow_mode = False
            cycle_mode = False
            sync_mode = True
        speed = float(message.split(b".")[-1]) / 1000


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
