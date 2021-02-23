import time
import adafruit_dht
from board import D4
from datetime import datetime
from configparser import ConfigParser
from pathlib import Path
import os

# Define Var.
i = 0
wait = 3.0

# Read Config file
config = ConfigParser()
config.read('config.ini')
# tempfileSection = config['tempfile']
logfilepath = config['tempfile']['logfilepath']

# Create Path if not already exists
Path(logfilepath).mkdir(parents=True, exist_ok=True)

# Define Logfile Name
filename = str(datetime.now().strftime("%Y-%m-%d") + "_templog.csv")
logfile = str(logfilepath + filename)

# Define Temp reader
dht_device = adafruit_dht.DHT22(D4)

# Create File or append new Data
datei = open(logfile,'w+')

while i == 0:
    try:

        # current date and time
        dt_object = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        #Read & Print Temp & Hum
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        data = str(["timestamp: ", dt_object, "; temperatur: ", temperature, "; humidity: ", humidity])
        print("timestamp: ", dt_object, "; temperatur: ", temperature, "; humidity: ", humidity)

        # Write Data into file
        datei.write("\r\n" + data)           

    # Check No Errors
    except RuntimeError as error:
        print(error.args)
        i = 0

        #Repeat if Failed
        print("Repeating action")

    else:
        # Check Temperature has Data
        if temperature != None:
            i = 1

    # Wait specific amount of Time
    time.sleep(wait)