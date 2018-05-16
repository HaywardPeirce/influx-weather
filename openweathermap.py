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
                "coord_lon": data['coord']['lon'],
                "coord_lat": data['coord']['lat'],
                "weather_id":data['weather'][0]['id'],
                "weather_main":data['weather'][0]['main'],
                "weather_description":data['weather'][0]['description'],
                "weather_icon":data['weather'][0]['icon'],
                "base":data['base'],
                "main_temp":float(data['main']['temp']),
                "main_pressure":(data['main']['pressure']/10),
                "main_humidity":data['main']['humidity'],
                "main_temp_min":data['main']['temp_min'],
                "main_temp_max":data['main']['temp_max'],
                "visibility":data['visibility'],
                "wind_speed":data['wind']['speed'],
                "wind_deg":float(data['wind']['deg']),
                "clouds_all":data['clouds']['all'],
                "dt":data['dt'],
                "sys_type":data['sys']['type'],
                "sys_id":data['sys']['id'],
                "sys_message":data['sys']['message'],
                "sys_country":data['sys']['country'],
                "sys_sunrise":data['sys']['sunrise'],
                "sys_sunset":data['sys']['sunset'],
                "id":data['id'],
                "name":data['name'],
                "cod":data['cod']
            }
        }
    ]

    return json_data

def main():
    weatherdata = getWeatherData(cityid)
    
    return weatherdata

if __name__ == '__main__':
    main()
