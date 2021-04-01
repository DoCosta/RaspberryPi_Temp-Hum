from datetime import datetime
from configparser import ConfigParser
import bottle
from bottle import run, route, response
from Temp import Temp
import numpy as np
import os
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

@route('/DataSince/<date>')
def datasince(date):
    date = date.replace("%20", " ")
    day = date.split(" ", 1)
    objs = []
    
    # start day
    filename = str(datetime.now().strftime(day[0]) + "_templog.csv")
    logfile = str(logfilepath + filename)
    logfile = open(logfile,'r')
    with logfile:
        reader = csv.DictReader(logfile)
        
        for row in reader:
                if date == row['Datum'] or date <= row['Datum']:

                    tempObj = Temp()
                    tempObj.date = row['Datum']
                    tempObj.temp = row['Temperatur']
                    tempObj.hum = row['Humidity']

                    objs.append(tempObj)
    logfile.close()

    files = os.listdir('logfile/')

    # all newer files
    for file in files:
        if filename < file:
            
            logfile = str(logfilepath + file)
            logfile = open(logfile,'r')
            with logfile:
                reader = csv.DictReader(logfile)
                
                for row in reader:
                        if date == row['Datum'] or date <= row['Datum']:
                            tempObj = Temp()
                            tempObj.date = row['Datum']
                            tempObj.temp = row['Temperatur']
                            tempObj.hum = row['Humidity']

                            objs.append(tempObj)
            logfile.close()

    response.content_type = 'application/json'
    objs.sort(key=lambda x: x.date)
    return json.dumps(objs, default=tojson)



# @route('Date/<Date>')
# def date(Date):
#     filename = str(datetime.now().strftime(Date) + "_templog.csv")
#     logfile = str(logfilepath + filename)

#     logfile = open(logfile,'r')

#     with logfile:
#         objs = []
#         reader = csv.DictReader(logfile)
        
        
#         for row in reader:
#             tempObj = Temp()
#             tempObj.date = row['Datum']
#             tempObj.temp = row['Temperatur']
#             tempObj.hum = row['Humidity']

#             objs.append(tempObj)

#     logfile.close()

#     response.content_type = 'application/json'
#     return json.dumps(objs, default=tojson)

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