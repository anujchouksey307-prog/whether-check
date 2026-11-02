import requests
import json
import os
import pyttsx3

city = input("Enter the city name: ")

url = f"https://api.weatherapi.com/v1/current.json?key=2d866703f275458d91053722262110&q={city}"

response = requests.get(url)

shortcut = response.json()['location']
shortcut2 = response.json()['current']
# print(shortcut['name'], shortcut['region'], shortcut['country'], shortcut2['temp_c'], "°C", shortcut2['condition']['text'])

text = f"Weather data for {shortcut['name']}, state is {shortcut['region']}, country is {shortcut['country']}, \n Temperature: {shortcut2['temp_c']}°C,\n Condition: {shortcut2['condition']['text']}"
# print(f"Temperature: {shortcut2['temp_c']}°C")
# print(f"Condition: {shortcut2['condition']['text']}")

engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()
    
    
huu = os.getenv('hyy')
print(text)