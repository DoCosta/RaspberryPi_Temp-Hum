import time
import adafruit_dht
from board import D4
from datetime import datetime
from configparser import ConfigParser
from bottle import run, route
from pathlib import Path
from os import path
import csv
import os

# Define Var.
i = 0
p = 0
wait = 1.5

# Read Config file
config = ConfigParser()
config.read('config.ini')
# tempfileSection = config['tempfile']
logfilepath = config['tempfile']['logfilepath']

Path(logfilepath).mkdir(parents=True, exist_ok=True)

# Define Logfile Name
filename = str(datetime.now().strftime("%Y-%m-%d") + "_templog.csv")
logfile = str(logfilepath + filename)

# Define Temp reader
dht_device = adafruit_dht.DHT22(D4)

# Create File or append new Data

datei = open(logfile,'a+')

while i == 0:
    try:

        # current date and time
        dt_object = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        #Read & Print Temp & Hum
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        data = str([dt_object, temperature,humidity])
        print(data)

        # Write Data into file
        # Check Temperature has Data
        if temperature != None:
            with datei:
                
                rownames = ['Datum', 'Temperatur', 'Humidity']
                writer = csv.DictWriter(datei, fieldnames=rownames)    

                writer.writeheader()
                writer.writerow({'Datum' : dt_object, 'Temperatur': temperature, 'Humidity' : humidity})


            # datei.write("\r\n" + data)      

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

