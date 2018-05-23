import configparser, json, time, datetime, requests, sys
#import urllib2
from urllib.request import urlopen
from datetime import datetime
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('owm-config.ini')

cityid = config['OPENWEATHERMAP']['Location']
weatherapikey = config['OPENWEATHERMAP']['APIKey']

#print(type(influxPort))

#influx_client = InfluxDBClient(influxAddress, influxPort, influxUser, influxPassword, influxDatabase)

def getWeatherData(cityid):
    try:
        requestURL = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(cityid)+ '&units=metric' + '&APPID=' + weatherapikey

        response = requests.get(requestURL)

        data = json.loads(response.text)

        json_data = formatData(data)

        return json_data
    except ValueError as e:
        print("Unable to retrieve Open Weathermap Weather info: {}".format(e))
        return None
    except KeyError as e:
        print("Unable to retrieve Weather Underground Weather info: {}".format(e))
        return None
    except TypeError as e:
        print("Unable to retrieve Open Weathermap Weather info: {}".format(e))
        return None
    except AttributeError as e:
        print("Unable to retrieve Open Weathermap Weather info: {}".format(e))
        return None
    except:
        e = sys.exc_info()[0]
        print("Unable to retrieve Open Weathermap Weather info: {}".format(e))
        return None

def formatData(data):

    json_data = [
        {
            "measurement": "openweathermap",
            "tags": {
                "city": data['name'],
                "location_id": data['id']
            },

            "fields":
            {
                # "coord_lon": data['coord']['lon'],
                # "coord_lat": data['coord']['lat'],
                # "weather_id":data['weather'][0]['id'],
                # "weather_main":data['weather'][0]['main'],
                # "weather_description":data['weather'][0]['description'],
                # "weather_icon":data['weather'][0]['icon'],
                # "base":data['base'],
                # "main_temp":float(data['main']['temp']),
                # "main_pressure":(data['main']['pressure']/10),
                # "main_humidity":data['main']['humidity'],
                # "main_temp_min":data['main']['temp_min'],
                # "main_temp_max":data['main']['temp_max'],
                # "visibility":data['visibility'],
                # "wind_speed":data['wind']['speed'],
                # "wind_deg":float(data['wind']['deg']),
                # "clouds_all":data['clouds']['all'],
                # "dt":data['dt'],
                # "sys_type":data['sys']['type'],
                # "sys_id":data['sys']['id'],
                # "sys_message":data['sys']['message'],
                # "sys_country":data['sys']['country'],
                # "sys_sunrise":data['sys']['sunrise'],
                # "sys_sunset":data['sys']['sunset'],
                # "id":data['id'],
                # "name":data['name'],
                # "cod":data['cod']
            }
        }
    ]
    
    if data['coord']['lon']: json_data[0]['fields']['coord_lon'] = float(data['coord']['lon'])
    if data['coord']['lat']: json_data[0]['fields']['coord_lat'] = float(data['coord']['lat'])
    if data['weather'][0]['id']: json_data[0]['fields']['weather_id'] = int(data['weather'][0]['id'])
    if data['weather'][0]['main']: json_data[0]['fields']['weather_main'] = str(data['weather'][0]['main'])
    if data['weather'][0]['description']: json_data[0]['fields']['weather_description'] = str(data['weather'][0]['description'])
    if data['main']['temp']: json_data[0]['fields']['main_temp'] = float(data['main']['temp'])
    if data['main']['pressure']: json_data[0]['fields']['main_pressure'] = float(data['main']['pressure']/10)
    if data['main']['humidity']: json_data[0]['fields']['main_humidity'] = float(data['main']['humidity'])
    if data['main']['temp_min']: json_data[0]['fields']['main_temp_min'] = float(data['main']['temp_min'])
    if data['main']['temp_max']: json_data[0]['fields']['main_temp_max'] = float(data['main']['temp_max'])
    if data['visibility']: json_data[0]['fields']['visibility'] = float(data['visibility'])
    if data['wind']['speed']: json_data[0]['fields']['wind_speed'] = float(data['wind']['speed'])
    if data['wind']['deg']: json_data[0]['fields']['wind_deg'] = float(data['wind']['deg'])
    if data['clouds']['all']: json_data[0]['fields']['clouds_all'] = float(data['clouds']['all'])
    if data['dt']: json_data[0]['fields']['dt'] = int(data['dt'])
    #if data['sys']['type']: json_data[0]['fields']['sys_type'] = data['sys']['type']
    #if data['sys']['id']: json_data[0]['fields']['sys_id'] = data['sys']['id']
    if data['sys']['country']: json_data[0]['fields']['sys_country'] = str(data['sys']['country'])
    if data['sys']['sunrise']: json_data[0]['fields']['sys_sunrise'] = int(data['sys']['sunrise'])
    if data['sys']['sunset']: json_data[0]['fields']['sys_sunset'] = int(data['sys']['sunset'])
    # if data['id']: json_data[0]['fields']['id'] = data['id']
    # if data['name']: json_data[0]['fields']['name'] = data['name']

    return json_data

def main():
    weatherdata = getWeatherData(cityid)
    
    return weatherdata

if __name__ == '__main__':
    main()
