import requests as re
import json 
import math

## API used in the project
## https://freegeoip.app/json/
## https://ipinfo.io/161.185.160.93/
## https://www.metaweather.com/api/location/search/?query=london
## https://www.metaweather.com/api/location/554890/


## Get json weather data
class Weather:

    def __init__(self):
        self.ip_address = re.get(url = 'https://freegeoip.app/json')
        self.ip_address_json = self.ip_address.json()


    ## Different variables for the city##
        self.ip_address_city = self.ip_address_json["city"]
        self.ip_address_country = self.ip_address_json["country_name"]
        self.ip_address_latlon = (self.ip_address_json["latitude"],self.ip_address_json["longitude"])



    def getWeatherFromCityIP(self):
        weatherData=re.get(url='https://www.metaweather.com/api/location/search/?query='+self.ip_address_city)
        weather_data_json = weatherData.json()

        return weather_data_json

    def getIP(self):
        self.ip_address = re.get(url = 'https://freegeoip.app/json')
        self.ip_address_json = self.ip_address.json()

        return self.ip_address_json['ip']

    def getWeatherFromCity(self,city):
        weatherData=re.get(url='https://www.metaweather.com/api/location/search/?query='+city)
        weather_data_json = weatherData.json()
        return weather_data_json

    ## Get Weather from lattlong
    def getWeatherFromLattLong(self):
        weatherData=re.get(url='https://www.metaweather.com/api/location/search/?lattlong='+str(self.ip_address_latlon[0])+','+str(self.ip_address_latlon[1]))
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


    ## Returns the saved ip from the file
    def get_ip_from_file(self):
    
        with open('ip_adress.txt') as f:
            first_line = f.readline()

        if len(first_line) < 0:
            print("i got no ip")
            return '-1'

        else:
            return first_line  
    

    ## Get the IP adress from the user ##
    