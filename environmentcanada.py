import configparser, json, sys, untangle, urllib.request
#import data_gc_ca_api
#from weathergc import Forecast

config = configparser.ConfigParser()
config.read('ec-config.ini')

siteCode = config['ENVIRONMENTCANADA']['SiteCode']
provinceCode = config['ENVIRONMENTCANADA']['Province']

def getWeatherData(siteID, province):
    
    #check that the location that has been submitted is a valid location
    
    try:
        ECLocationList = untangle.parse('http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/siteList.xml')
    except urllib.error.HTTPError as e:
        print("Unable to retrieve Environment Canada Weather Station List: {}".format(e))
    except:
        e = sys.exc_info()[0]
        print("Unable to retrieve Environment Canada Weather Station List: {}".format(e))
        
        return None
        
    #print (ECLocationList.siteList)
    
    
    #loop through each of the sites in the list of available sites to confirm that the requested site is available 
    for item in ECLocationList.siteList.site:
        
        #print(item['code'])
        #print(item.provinceCode.cdata)
        
        #if this site in the list is the same as the site that is asking for
        if siteID == item['code'] and province == item.provinceCode.cdata:
            break
    
    #the site was not one the list
    else:
        print('Unable to find station `{}` in province `{}` on list of available stations'.format(siteID, province))
        return None
        
    #lookup the weather for the requested location
    try:
        locationWeather = untangle.parse('http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/' + province + '/' + siteID + '_e.xml')
    except urllib.error.HTTPError as e:
        print("Unable to retrieve Environment Canada Weather for station {}: {}".format(siteID, e))
    except:
        e = sys.exc_info()[0]
        print("Unable to retrieve Environment Canada Weather for station {}: {}".format(siteID, e))
        
        return None
    
    #print(locationWeather.siteData.currentConditions)
    
    try:
        formattedData = formatData(locationWeather.siteData.currentConditions)
        
        return formattedData
    except:
        e = sys.exc_info()[0]
        print("Unable to format Environment Canada Weather data: {}".format(e))
        
        return None

def formatData(data):
    
    #print(data.station['code'])
    
    json_data = [
        {
            "measurement": "environmentcanada",
            "tags": {
                "stationCode": str(data.station['code'])
            },

            "fields":
            {
                'observation': str(data.dateTime[1].textSummary.cdata),
                'condition': str(data.condition.cdata),
                'temperature': float(data.temperature.cdata),
                'dewpoint': float(data.dewpoint.cdata),
                'pressure': float(data.pressure.cdata),
                'pressure_tendency': str(data.pressure['tendency']),
                'pressure_change': float(data.pressure['change']),
                'visibility': float(data.visibility.cdata),
                'relativeHumidity':float(data.relativeHumidity.cdata),
                'wind_speed': float(data.wind.speed.cdata),
                'wind_direction': str(data.wind.direction.cdata),
                'wind_bearing': float(data.wind.bearing.cdata)
             }
        }
    ]


    #print(type(json_data))
    #print(json_data)

    return json_data

def main():
    
    weatherdata = getWeatherData(siteCode, provinceCode)
    
    #print(weatherdata)
    
    return weatherdata
    
if __name__ == '__main__':
    main()
