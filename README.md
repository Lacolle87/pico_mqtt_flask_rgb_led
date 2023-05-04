<h1>RGB LED Strip Control with Raspberry Pi Pico</h1>
<p>This project allows controlling an RGB LED strip connected to a Raspberry Pi Pico using MQTT messages. The LED strip used is a WS2812.</p>
<h2>Technologies Used</h2>
<ul>
<li>Raspberry Pi Pico W microcontroller board</li>
<li>WS2812 RGB LED strip</li>
<li>MicroPython programming language</li>
<li>Flask web framework</li>
<li>MQTT protocol for message communication</li>
<li>HTML and JavaScript for the user interface</li>
</ul>
<h2>Description</h2>
<p>The project allows the user to control the WS2812 strip by sending MQTT messages. The user interface is a web page that displays a color picker and a checkbox for enabling a rainbow effect. When the user selects a color and submits the form, an MQTT message is sent to the Pico containing the color information. If the rainbow effect is enabled, the message also includes the speed of the effect.</p>
<h2>Usage</h2>
<ol>
<li>Connect the WS2812 LED strip to the Raspberry Pi Pico.</li>
<li>Install MicroPython on the Raspberry Pi Pico.</li>
<li>Upload the Python code to the Pico.</li>
<li>Install the necessary Python packages on the host computer: Flask and Paho MQTT.</li>
<li>Install and start the Mosquitto MQTT broker.</li>
<li>Start the Flask web server.</li>
<li>Open the web page on the browser and select a color and the rainbow effect checkbox.</li>
<li>Submit the form to send the MQTT message to the Raspberry Pi Pico.</li>
</ol>