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



        self.add(npyscreen.ButtonPress, name="Fecth Data from stored IP", when_pressed_function=self.btn_press, relx = 2)
        self.add(npyscreen.ButtonPress, name="Store a new IP", when_pressed_function=self.btn_press_get_IP, relx = 2)
        
        self.add(npyscreen.TitleText, w_id="empty line", name= " ",editable = False)

        self.add(npyscreen.TitleText, w_id="city", name= "City:", begin_entry_at= 8, relx = 4)
        self.add(npyscreen.ButtonPress, name="Fecth Data from city", when_pressed_function=self.btn_press_city, relx = 2)
        

        # If we get to making a second window
        #self.add(npyscreen.ButtonPress, name = "Switch", when_pressed_function = self.btn_press_switch, relx = 2)

        ## Draw a sun in the bottom
        for i in range(0,7):
            self.draw_sun((i*15) + 7,21)




    ## Fetch data from ip    
    def btn_press(self):
        w = Weather()
        weather = w.getWeatherFromCityIP()
        ip = w.get_ip_from_file()

        if ip == '-1':
            npyscreen.notify_confirm("No IP saved please save one before using:(", title="No saved IP" + city + " IP: " + ip, wrap=True, wide=True, editw=1)
        else:
            city =  weather[0]['title']
            woeid = w.getWOEIDFromJSON(weather)
            five_day_forecast = w.getWeatherForecast(woeid)
            long_string = self.week_day_forecast(five_day_forecast)
            


            
            npyscreen.notify_confirm(long_string, title="Weather forecast for " + city + " IP: " + ip, wrap=True, wide=True, editw=1)
    



    ## City buttom press
    def btn_press_city(self):
        city = self.get_widget("city").value

        if len(city) > 0:
            w = Weather()
            weather = w.getWeatherFromCity(city)
            if weather and "title" in weather[0]:
                woeid = w.getWOEIDFromJSON(weather)
                five_day_forecast = w.getWeatherForecast(woeid)
                long_string = self.week_day_forecast(five_day_forecast)
                
                npyscreen.notify_confirm(long_string, title="Weather forecast for " + city , wrap=True, wide=True, editw=1)  
            
            else:
                npyscreen.notify_confirm("Could not fetch data from that city", title="Weather is", wrap=True, wide=True, editw=1)  


            
        
        else:
            npyscreen.notify_confirm("You cannot input an empty string", title="Weather is", wrap=True, wide=True, editw=1)

    ## Store a new IP 
    def btn_press_get_IP(self):
        w = Weather()
        ip = w.write_ip_to_file()
        npyscreen.notify_confirm("Succesfully wrote IP: " + ip + " to file", title="Succes!", wrap=True, wide=True, editw=1)


    ## Method for printing the forecast
    def week_day_forecast(self, json):
        long_string = ''  
        list_weather = ""
        list_temp = ""
        list_date = ''

        for i in range(0,4):
            list_weather = json["consolidated_weather"][i]["weather_state_name"]
            list_temp = json["consolidated_weather"][i]["the_temp"]
            list_date = json["consolidated_weather"][i]["applicable_date"]

            long_string += "Date: " + list_date + " weather is " + str(list_weather).lower() + " and the temperature is " + str(round(list_temp,1)) + "\n"
        
        return long_string

    
    def draw_sun(self, relx, rely):
        self.add(npyscreen.TitleText, w_id="sun", name= "    |",editable = False, relx = relx,rely = rely)
        self.add(npyscreen.TitleText, w_id="sun", name= "  \ | /" ,editable = False,  relx = relx,rely = rely+1)
        self.add(npyscreen.TitleText, w_id="sun", name= "   \*/"  ,editable = False,  relx = relx,rely = rely+2)
        self.add(npyscreen.TitleText, w_id="sun", name= "--**O**-- ",editable = False,  relx = relx,rely = rely+3)
        self.add(npyscreen.TitleText, w_id="sun", name= "   /*\\",editable = False,  relx = relx,rely = rely+4)
        self.add(npyscreen.TitleText, w_id="sun", name= "  / | \\",editable = False,  relx = relx,rely = rely+5)
        self.add(npyscreen.TitleText, w_id="sun", name= "    |",editable = False,  relx = relx,rely = rely+6)



        




    def btn_press_switch(self):
        self.parentApp.switchForm('SECOND')

    def on_ok(self):
        self.parentApp.switchForm(None)



## If we get to making a second form
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