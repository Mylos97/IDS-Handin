import requests as re
import json 

## API used in the project
## https://freegeoip.app/json/
## https://www.metaweather.com/api/location/search/?query=london
## https://www.metaweather.com/api/location/554890/


## Get json weather data
class Weather:

    ## Get the city from the ip
    def get_city_from_ip(self, ip):
        ip_json = re.get(url = 'https://freegeoip.app/json/' + ip).json()
        city = ip_json['city']

        return city

    ## Get weather from city
    def getWeatherFromCity(self,city):
        weatherData=re.get(url='https://www.metaweather.com/api/location/search/?query='+city)
        weather_data_json = weatherData.json()
        return weather_data_json


    ## Get WOEID from json
    def getWOEIDFromJSON(self, weather_json):
        woeid = weather_json[0]['woeid']

        return woeid


    ## Get the 5 day forecast for the weather
    def getWeatherForecast(self, woeid):
        fiveDayForecast = re.get(url='https://www.metaweather.com/api/location/'+ str(woeid) +'/')
        fiveDayForecast_json = fiveDayForecast.json()
        return fiveDayForecast_json


    ## Save the IP 
    def write_ip_to_file(self):
        get_ip = re.get(url = "https://freegeoip.app/json/")
        get_ip_json = get_ip.json()


        file = open('ip_address.txt', 'a')
        file.truncate(0)
        file.write(get_ip_json["ip"])
        file.close()

        return get_ip_json['ip']


    ## Returns the saved ip from the file and checks if there is a IP stored
    def get_ip_from_file(self):
    
        with open('ip_address.txt') as f:
            first_line = f.readline()

        ## Test if theres an ip stored in the textfile
        if len(first_line) < 6:
            return '-1'

        else:
            return first_line  
    
    