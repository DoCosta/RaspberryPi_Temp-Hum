from datetime import datetime
from configparser import ConfigParser
from bottle import run, route
import numpy as np
import csv
i = 0


config = ConfigParser()
config.read('config.ini')
# tempfileSection = config['tempfile']
logfilepath = config['tempfile']['logfilepath']

filename = str(datetime.now().strftime("%Y-%m-%d") + "_templog.csv")
logfile = str(logfilepath + filename)

logfile = open(logfile,'r')

with logfile:
    reader = csv.DictReader(logfile)
    
    for row in reader:
        Date = row['Datum']
        Temp = row['Temperatur']
        Hum = row['Humidity']
logfile.close()


@route('/')
def index():
    return { "Date" : Date, "Temp": Temp, "Hum" : Hum }

run(host='localhost', port=8080, debug=True, reloader=True)


