from datetime import datetime
from configparser import ConfigParser
import bottle
from bottle import run, route, response
from Temp import Temp
import numpy as np
import csv
import json
i = 0

config = ConfigParser()
config.read('config.ini')
# tempfileSection = config['tempfile']
logfilepath = config['tempfile']['logfilepath']

def tojson(self):
    return self.__dict__
Date =''

@route('/<Date>')
def date(Date):
    filename = str(datetime.now().strftime(Date) + "_templog.csv")
    logfile = str(logfilepath + filename)

    logfile = open(logfile,'r')

    with logfile:
        reader = csv.DictReader(logfile)
        objs = []
        
        for row in reader:
            tempObj = Temp()
            tempObj.date = row['Datum']
            tempObj.temp = row['Temperatur']
            tempObj.hum = row['Humidity']

            objs.append(tempObj)

    logfile.close()

    response.content_type = 'application/json'
    return json.dumps(objs, default=tojson)

@route('/')
def index():
    
    filename = str(datetime.now().strftime("%Y-%m-%d") + "_templog.csv")
    logfile = str(logfilepath + filename)

    logfile = open(logfile,'r')

    with logfile:
        reader = csv.DictReader(logfile)
        objs = []
        
        for row in reader:
            tempObj = Temp()
            tempObj.date = row['Datum']
            tempObj.temp = row['Temperatur']
            tempObj.hum = row['Humidity']

            objs.append(tempObj)

    logfile.close()

    response.content_type = 'application/json'
    return json.dumps(objs, default=tojson)

run(host='0.0.0.0', port=8080, debug=True, reloader=True)