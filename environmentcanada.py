import configparser
import json
import data_gc_ca_api
from weathergc import Forecast

config = configparser.ConfigParser()
config.read('ec-config.ini')

cityid = config['ENVIRONMENTCANADA']['Location']

def getWeatherData(cityid):

    #print(cityid)
    data = Forecast(cityid)
    #print(data.as_dict())
    data_dict = data.as_dict()
    #print(type(data_dict))
    #print(data_dict['Current Conditions'])

    #data = json.loads(response.text)
    #print(data['main']['temp'])

    json_data = formatData(data_dict)

    return json_data

def formatData(data):

    #print(type(data))
    #print(data)
    #print(data['Current Conditions'][0]['data']['Temperature'])
    #print(data['Current Conditions'][0]['data']['Wind'])
    temperature = data['Current Conditions'][0]['data']['Temperature'].split( )
    wind = data['Current Conditions'][0]['data']['Wind'].split( )
    dewpoint = data['Current Conditions'][0]['data']['Dewpoint'].split( )
    humidity = data['Current Conditions'][0]['data']['Humidity'].split( )
    visibility = data['Current Conditions'][0]['data']['Visibility'].split( )
    pressure = data['Current Conditions'][0]['data']['Pressure / Tendency'].split( )

    #print(wind[0])
    json_data = [
        {
            "measurement": "environmentcanada",
            "tags": {
                "city": cityid
            },

            "fields":
            {
                'Observed at':"Victoria Int'l Airport 7:00 PM PST Tuesday 28 February 2017",
                'Air Quality Health Index':'3',
                'WindSpeed':wind[1],
                'Condition':'Light Rain',
                'Dewpoint':dewpoint[0],
                'Humidity':humidity[0],
                'Visibility':visibility[0],
                'Pressure / Tendency':pressure[0],
                'Temperature':temperature[0]
             }
        }
    ]


    #print(type(json_data))
    #print(json_data)

    return json_data

def main():
    weatherdata = getWeatherData(cityid)
    #sendInfluxData(weatherdata)
    print(weatherdata)
    #help(data_gc_ca_api.cityweather)
    #data_gc_ca_api.cityweather.city("Ottawa")

    #help(weathergc)


    #f.as_json()
    #print(f)

    #time.sleep(delay)
    return weatherdata

if __name__ == '__main__':
    main()
