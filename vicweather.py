#import urllib2
from urllib.request import urlopen
from lxml import html, etree, objectify
from datetime import datetime
import json, time, datetime, requests, configparser, sys, json


# from influxdb import InfluxDBClient
# from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
# from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('vicweather-config.ini')

stationId = config['VICWEATHER']['stationId']

with open('vicweather-value-config.json') as f:
    vicWeatherValues = json.load(f)

# with open('abm-value-config.json') as f:
#     abmValues = json.load(f)

def getWeatherData(stationId):
    try:
        page = requests.get('http://victoriaweather.ca/current_obs_explainer.php?id=' + stationId)
        
        tree = html.fromstring(page.content)
        # print(tree)
        # weatherValues = tree.xpath('//div[@id="current_obs"]')[0][0]

        weatherValues = tree.xpath('//div[@id="outline_container"]')[0]
        # //*[@id="current_obs"]/table/tbody
        # print(weatherValues)
        # print(weatherValues[0])
        # print(weatherValues[0][0])

        return formatData(weatherValues)

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
            "measurement": "vicschoolweather",
            "tags": {},

            "fields": {}
        }
    ]
    
    # make sure that the nessesary tags are present, otherwise exit
    try:
        #print("title: `{}`".format(data[0][0].text))
        #configure the tags for the entry
        json_data[0]['tags']['stationName'] = (str(data[0][0].text))
        json_data[0]['tags']['stationId'] = int(stationId)
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
    
    data = data[0][1][0][0] 

    # Loop through each of the fields that have been configured in the `vicweather-value-config.json` file
    for row in data:
        # print(row)
        # print(row.tag)
        # print(row[0].text)

        for entry in vicWeatherValues:
            # print("row comparison `{}`, `{}`".format(row[0].text, entry['title']))

            if row[0].text == entry['title']:
                # print(entry)

                if entry['split']:
                    value = row[1][0].text
                    value = value.split(entry['split'])[0]
                else: 
                    value = row[1][0].text

                if entry['type'] == "str":
                    value = str(value)
                elif entry['type'] == "float":
                    value = float(value)

                json_data[0]['fields'][entry['name']] = value

            # handling of additional information that needs to be parsed
            if row[0].text == "Wind Speed: ":
                windDirection = row[1][0].text
                windDirection = windDirection.split(entry['split'])[2]
                # print("Wind Direction - `{}`".format(windDirection))
                json_data[0]['fields']['wind_direction'] = str(windDirection)

            #TODO: work out how to translate their graphical representation of the pressure trend and wind direction (should it be degrees?) also, should the date be converted into a timestamp?            
        
    
    # print(json_data)

    return json_data

def main():
    weatherdata = getWeatherData(stationId)
    
    return weatherdata

if __name__ == '__main__':
    main()
