#import urllib2
from urllib.request import urlopen
from datetime import datetime
import json, time, datetime, requests, configparser, sys, json
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('abm-config.ini')

json_url = config['ABM']['JSONURL']


with open('abm-value-config.json') as f:
    abmValues = json.load(f)

#print(type(influxPort))

#influx_client = InfluxDBClient(influxAddress, influxPort, influxUser, influxPassword, influxDatabase)

def getWeatherData(json_url):
    try:
        # requestURL = 'http://api.wunderground.com/api/' + weatherapikey + '/conditions/q/' + str(cityid)+ '.json'
    
        response = requests.get(json_url)
    
        data = json.loads(response.text)
    
        json_data = formatData(data)
    
        return json_data
    except ValueError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except KeyError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except TypeError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except AttributeError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except:
        e = sys.exc_info()[0]
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None

def formatData(data):

    json_data = [
        {
            "measurement": "austrlianbureaumeteorology",
            "tags": {},

            "fields": {}
        }
    ]
    
    try:
        # make sure that the nessesary tags are present, otherwise exit
        # TODO: should we return null?
        
        json_data[0]['tags']['name'] = (str(data['observations']['header'][0]['name']))
        json_data[0]['tags']['ID'] = (str(data['observations']['header'][0]['ID']))
        json_data[0]['tags']['main_ID'] = (str(data['observations']['header'][0]['main_ID']))
    except ValueError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except KeyError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except TypeError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except AttributeError as e:
        print("Unable to retrieve ABM Weather info: {}".format(e))
        return None
    except:
        e = sys.exc_info()[0]
        print("Unable to collect tag info: {}".format(e))
        return None
    
    print("sort_order", data['observations']['data'][0]['sort_order'])
    print(data['observations']['data'][0])
    
    print(abmValues)
    
    for entry in abmValues:
        print(entry, " ", abmValues[entry])
        if entry in data['observations']['data'][0]:
            
            if data['observations']['data'][0][entry] == None:
                json_data[0]['fields'][entry] = data['observations']['data'][0][entry]
                continue
            
            elif abmValues[entry] == "str":
                json_data[0]['fields'][entry] = str(data['observations']['data'][0][entry])
                
            elif abmValues[entry] == "float":
                json_data[0]['fields'][entry] = float(data['observations']['data'][0][entry])
    
    print(json_data)

    return json_data

def main():
    weatherdata = getWeatherData(json_url)
    
    return weatherdata

if __name__ == '__main__':
    main()
