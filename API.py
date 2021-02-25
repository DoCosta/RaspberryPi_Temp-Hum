from datetime import datetime
from configparser import ConfigParser
from bottle import run, route

i = 0
config = ConfigParser()
config.read('config.ini')
# tempfileSection = config['tempfile']
logfilepath = config['tempfile']['logfilepath']



filename = str(datetime.now().strftime("%Y-%m-%d") + "_templog.csv")
logfile = str(logfilepath + filename)
file = open(logfile,'r')

@route('/') 
def index():
    return {file.read()}

run(host='localhost', port=8080, debug=True, reloader=True)
file.close()






