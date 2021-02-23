import time
import adafruit_dht
from board import D4

dht_device = adafruit_dht.DHT22(D4)

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print("temperatur: ", temperature, "humidity: ", humidity)

    except RuntimeError as error:
        print(error.args)

    time.sleep(2.0)