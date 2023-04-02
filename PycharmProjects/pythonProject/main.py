import json

import requests
from tkinter import *
from dotenv.main import load_dotenv
import os
from os.path import exists
import datetime
from datetime import datetime
import time
import math

load_dotenv()

api_key = os.environ['API_KEY']
city = input("What is the name of your city :")


def display_results(city, t, fl, h):
    print(f'{city} Weather\nTemperature: {math.floor(t - 273.15)}°C '
          f'\nFeels like: {math.floor(fl - 273.15)}°C \nHumidity: {h}%')


def file_older_than_180_min(file_name):
    file_mod_time = os.path.getmtime(file_name+".txt")
    current_time = time.time()

    # convert timestamps to datetime object
    time1 = datetime.fromtimestamp(file_mod_time)
    time2 = datetime.fromtimestamp(current_time)

    # Difference between two timestamps
    # in hours:minutes:seconds format
    final_time = time2 - time1

    # create 2 dates with 3 hours difference then convert from string to datetime
    datetime_str = '04/01/23 9:00:00'
    datetime_str2 = '04/01/23 6:00:00'
    datetime_conv = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    datetime_conv2 = datetime.strptime(datetime_str2, '%m/%d/%y %H:%M:%S')

    # minus date2 from date1 to get 3 hours difference in timedelta format
    delta = datetime_conv - datetime_conv2

    if final_time>delta:
        return True
    else:
        return False


def weather_request(apiKey, cityName):
    url= f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={apiKey}"
    url2= f"https://api.openweathermap.org/data/2.5/forecast?q={cityName}&appid={apiKey}"

    api_call = requests.get(url).json()
    second_api_call = requests.get(url2).json()

    filename = cityName+str(api_call['coord']['lat'])+"-"+str(api_call['coord']['lon'])
    t = api_call['main']['temp']
    h = api_call['main']['humidity']
    fl = api_call['main']['feels_like']

    if exists(filename+".txt"):
        if file_older_than_180_min(filename):
            with open(filename + ".txt", 'a+') as file:
                file.write(str(api_call))
                t = api_call['main']['temp']
                h = api_call['main']['humidity']
                fl = api_call['main']['feels_like']

                display_results(cityName, t, fl, h)

                return {
                    'temp': math.floor(t - 273.15),
                    'feels_like': math.floor(fl - 273.15),
                    'humidity': h
                   }

        else:
            display_results(cityName, t, fl, h)

            return {
                'temp': math.floor(t - 273.15),
                'feels_like': math.floor(fl - 273.15),
                'humidity': h
            }
    else:
        with open(filename + ".txt", 'a+') as file:
            file.write(str(api_call))
            t = api_call['main']['temp']
            h = api_call['main']['humidity']
            fl = api_call['main']['feels_like']

            display_results(cityName, t, fl, h)

            return {
                'temp': math.floor(t - 273.15),
                'feels_like': math.floor(fl - 273.15),
                'humidity': h
            }


weather = weather_request(api_key,city)

root = Tk()
root.geometry("300x300")
root.title(f'{city} Weather')


def display_city(city_name):
    city_label = Label(root, text=f'{city_name}')
    city_label.config(font=("Consolas",28))
    city_label.pack(side='top')


def display_stats(weather):
    temp = Label(root,text=f"Temperature: {weather['temp']}°C")
    feels_like = Label(root, text=f"Feels Like:  {weather['feels_like']}°C")
    humidity = Label(root, text=f"Humidity: {weather['humidity']}%")

    temp.config(font=("Consolas", 22))
    feels_like.config(font=("Consolas", 16))
    humidity.config(font=("Consolas", 16))

    temp.pack(side='top')
    feels_like.pack(side='top')
    humidity.pack(side='top')


display_city(city)
display_stats(weather)

mainloop()
