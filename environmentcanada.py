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
    except ValueError as e:
        print("Unable to format Environment Canada Weather data: {}".format(e))
        return None
    except TypeError as e:
        print("Unable to format Environment Canada Weather data: {}".format(e))
        return None
    except AttributeError as e:
        print("Unable to format Environment Canada Weather data: {}".format(e))
        return None
    except:
        e = sys.exc_info()[0]
        print("Unable to format Environment Canada Weather data: {}".format(e))
        
        return None

def formatData(data):
    
    #print(data.station['code'])
    #print(type(data.pressure.cdata))
    
    #TODO: check that values are not empty (they seem to all start as stings) before converting to floats (really doesnt like that)
    
    
    json_data = [
        {
            "measurement": "environmentcanada",
            "tags": {
                "stationCode": str(data.station['code'])
            },

            "fields":
            {
                
                # 'pressure': ,
                # 'pressure_tendency': str(data.pressure['tendency']),
                # 'pressure_change': float(data.pressure['change']),
                # #'visibility': float(data.visibility.cdata),
                # 'relativeHumidity':float(data.relativeHumidity.cdata),
                # 'wind_speed': float(data.wind.speed.cdata),
                # 'wind_direction': str(data.wind.direction.cdata),
                # 'wind_bearing': float(data.wind.bearing.cdata)
             }
        }
    ]
    
    #print(json_data[0]['fields'])
    
    if data.dateTime[1].textSummary.cdata: json_data[0]['fields']['observation'] = str(data.dateTime[1].textSummary.cdata)
    if data.condition.cdata: json_data[0]['fields']['condition'] = str(data.condition.cdata),
    if data.temperature.cdata: json_data[0]['fields']['temperature'] = float(data.temperature.cdata)
    if data.dewpoint.cdata: json_data[0]['fields']['dewpoint'] = float(data.dewpoint.cdata)
    if data.pressure.cdata: json_data[0]['fields']['pressure'] = float(data.pressure.cdata)
    if data.pressure['tendency']: json_data[0]['fields']['pressure_tendency'] = str(data.pressure['tendency'])
    if data.pressure['change']: json_data[0]['fields']['pressure_change'] = float(data.pressure['change'])
    if data.relativeHumidity.cdata: json_data[0]['fields']['relativeHumidity'] = float(data.relativeHumidity.cdata)
    if data.dateTime[1].textSummary.cdata: json_data[0]['fields']['wind_speed'] = float(data.wind.speed.cdata)
    if data.dateTime[1].textSummary.cdata: json_data[0]['fields']['wind_direction'] = str(data.wind.direction.cdata)
    if data.dateTime[1].textSummary.cdata: json_data[0]['fields']['wind_bearing'] = float(data.wind.bearing.cdata)
    
    


    #print(type(json_data))
    print(json_data)

    return json_data

def main():
    
    weatherdata = getWeatherData(siteCode, provinceCode)
    
    #print(weatherdata)
    
    return weatherdata
    
if __name__ == '__main__':
    main()
