from Weather import *
import npyscreen




class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="Weather App")
        self.addForm('SECOND', SecondForm, name="second")
    
    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()


class FirstForm(npyscreen.ActionFormMinimal):
    def create(self):
        self.add(npyscreen.TitleText, w_id="message", name= "How's the weather today?",editable = False, begin_entry_at= 12, relx = 2)

        self.add(npyscreen.ButtonPress, name="Fecth Data from IP", when_pressed_function=self.btn_press, relx = 2)
        
        self.add(npyscreen.TitleText, w_id="city", name= "CITY:", begin_entry_at= 8, relx = 4)
        self.add(npyscreen.ButtonPress, name="Fecth Data from city", when_pressed_function=self.btn_press_city, relx = 2)
        self.add(npyscreen.ButtonPress, name = "Switch", when_pressed_function = self.btn_press_switch, relx = 2)


    ## Fetch data from ip    
    def btn_press(self):
        w = Weather()
        weather = w.getWeatherFromCityIP()
        city =  weather[0]['title']
        woeid = w.getWOEIDFromJSON(weather)
        five_day_forecast = w.getWeatherForecast(woeid)

        weather_today = five_day_forecast["consolidated_weather"][0]["weather_state_name"]
        weather_tommorow = five_day_forecast["consolidated_weather"][1]["weather_state_name"]

        weather_today_temperature = five_day_forecast["consolidated_weather"][0]["the_temp"]
        weather_tommorow_temperature = five_day_forecast["consolidated_weather"][1]["the_temp"]


        
        npyscreen.notify_confirm("Weather today is " + weather_today + " and the temperature is " + str(weather_today_temperature)[:3] + "\n" + "Weather tommorow is " + weather_tommorow + " and the temperature is " + str(weather_tommorow_temperature)[:3], title="Weather Forecast for " + city, wrap=True, wide=True, editw=1)
    



    ## City buttom press
    def btn_press_city(self):
        city = self.get_widget("city").value

        if len(city) > 0:
            w = Weather()
            weather = w.getWeatherFromCity(city)
            if weather and "title" in weather[0]:
                woeid = w.getWOEIDFromJSON(weather)
                five_day_forecast = w.getWeatherForecast(woeid)
                long_string = ''
                for i in range(0,5):
                    list_weather = weather_today = five_day_forecast["consolidated_weather"][i]["weather_state_name"]
                    list_temp = five_day_forecast["consolidated_weather"][i]["the_temp"]
                    long_string += "Weather is " + str(list_temp)[i] + "\n"  
                    #" and the temperature is " + str(list_temp[i])[:3] + "\n"

                weather_today = five_day_forecast["consolidated_weather"][0]["weather_state_name"]
                weather_tommorow = five_day_forecast["consolidated_weather"][1]["weather_state_name"]

                weather_today_temperature = five_day_forecast["consolidated_weather"][0]["the_temp"]
                weather_tommorow_temperature = five_day_forecast["consolidated_weather"][1]["the_temp"]
                
                #npyscreen.notify_confirm(long_string, title="Weather is", wrap=True, wide=True, editw=1)  
                npyscreen.notify_confirm("Weather today is " + weather_today + " and the temperature is " + str(weather_today_temperature)[:3] + "\n" + "Weather tommorow is " + weather_tommorow + " and the temperature is " + str(weather_tommorow_temperature)[:3], title="Weather forecast for " + city, wrap=True, wide=True, editw=1)  
            
            else:
                npyscreen.notify_confirm("Could not fetch data from that city", title="Weather is", wrap=True, wide=True, editw=1)  


            
        
        else:
            npyscreen.notify_confirm("You cannot input an empty string", title="Weather is", wrap=True, wide=True, editw=1)

        




    def btn_press_switch(self):
        self.parentApp.switchForm('SECOND')

    def on_ok(self):
        self.parentApp.switchForm(None)

class SecondForm(npyscreen.ActionFormMinimal):
    def create(self):
        pass

        
    def btn_press(self):
        pass
    
    def btn_back(self):
        self.parentApp.switchForm('MAIN')

    def on_ok(self):
        self.parentApp.switchForm(None)


app = App()
app.run()