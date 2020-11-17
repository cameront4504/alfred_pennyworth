# DIG5508: Final Project
# Name: Alfred Pennyworth
# Time Spent: Rihanna-turning-hand.gif

# Feature Planning
"""
    - GUI interface [ ]
    - Tells time [x]
    - Tells weather [x]
"""

#--------------------------------------------------------------------------

# Table of Contents

#--------------------------------------------------------------------------
"""

1.0 SETUP
2.0 FUNCTIONS
3.0 BUILDING GUI
4.0 EXECUTION

"""
#--------------------------------------------------------------------------

# SETUP

#--------------------------------------------------------------------------

# LIBRARIES AND ADDONS

import json
from datetime import date, datetime
from tkinter import *
import requests

# CLASSES

class User(object):
    def __init__(self, fname, lname, nickname, gender):
        self.fname = fname
        self.lname = lname
        self.gender = gender

class Weather(object):
    def __init__(self,temp,desc):
        self.temp = temp
        self.desc = desc

#--------------------------------------------------------------------------

# FUNCTIONS

#--------------------------------------------------------------------------

def grabSettings():
    # Get JSON from settings file, remembering user preferences
    with open('settings.txt') as json_file:
        data = json.load(json_file)
        for d in data['user']:
            fname = d['fname']
            lname = d['lname']
            nickname = d['nickname']
            gender = d['gender']
        return fname, lname, nickname, gender

fname,lname,nickname,gender = grabSettings()
theUser = User(fname,lname,nickname,gender)

def andNowTheWeather():
    # Get JSON from openweathermap.org and create an object using data
    # Formatted as: Temp, Description
    weatherRequest = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Orlando&appid=944d36db5865dfe678be92ab8f209646")
    data = weatherRequest.json()
    temp = data['main']['feels_like']
    desc = data['weather'][0]['description']
    return temp, desc

# GET WEATHER AND MAKE OBJECT
# Limited requests, so turn off for testing (It's 1000 I think, but still.)
#temp,desc = andNowTheWeather()
#currentWeather = Weather(temp,desc)
#print(currentWeather.temp)

# GET CURRENT TIME AND DATE
# Formatted mm-dd-yyyy and 00:00 in the 12 hour system
d = date.today()
theDate = d.strftime("%B %d, %Y")
t = datetime.now()
theTime = t.strftime("%I:%M %p")

# Was going to use gtts, but it only has female voice which does not suit my customization goals
import pyttsx3
engine = pyttsx3.init()
engine.say("Good evening" + theUser.fname)
engine.runAndWait()

#--------------------------------------------------------------------------

# 3.0 BUILDING GUI

#--------------------------------------------------------------------------

#root = Tk()

#def myClick():
#	myLabel = Label(root, text="Look! I clicked a Button!!")
#	myLabel.pack()

#myButton = Button(root, text="Click Me!", command=myClick)
#myButton.pack()

#root.mainloop()

# EXECUTE FILE

#main_interface()
