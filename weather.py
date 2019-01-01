import configparser
import requests
import importlib
#import urllib2
#from urllib.request import urlopen
from datetime import datetime
import json
import time
import datetime
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('config.ini')

delay = float(config['GENERAL']['Delay'])
output = bool(config['GENERAL'].get('Output', fallback=True))
# print(output)

influxAddress = config['INFLUXDB']['Address']
influxPort = float(config['INFLUXDB']['Port'])
influxDatabase = config['INFLUXDB']['Database']
influxUser = config['INFLUXDB'].get('Username', fallback='')
influxPassword = config['INFLUXDB'].get('Password', fallback='')

Sources = json.loads(config['WEATHER'].get('Sources'))

influx_client = InfluxDBClient(influxAddress, influxPort, influxUser, influxPassword, influxDatabase)

#return a list of payloads to send to influxdb
def getSourceData(source):
    
    lib = importlib.import_module(source)

    sourceData = lib.main()

    return sourceData

def sendInfluxData(json_data):

    if output:
        #print(json_data)
        print(type(json_data))

    try:
        influx_client.write_points(json_data)
    except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
        if hasattr(e, 'code') and e.code == 404:

            print('Database {} Does Not Exist.  Attempting To Create'.format(influxDatabase))

            influx_client.create_database(influxDatabase)
            influx_client.write_points(json_data)

            return

        print('ERROR: Failed To Write To InfluxDB')
        print(e)

    if output:
        print('Written To Influx: {}'.format(json_data))


def main():
    while True:
        for source in Sources:

            sourceData = getSourceData(source)
            
            #only send the data if there is non-null data to send
            if sourceData is not None:
                sendInfluxData(sourceData)

        time.sleep(delay)

if __name__ == '__main__':
    main()
