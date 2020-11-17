# DIG5508: Final Project
# Name: Alfred Pennyworth
# Time Spent: Rihanna-turning-hand.gif

# Feature Planning
"""
    [ ] GUI interface [ ]
    [x] Tells time
    [x] Tells weather
    [ ] Customize Assistant
        [ ] Personality (Acrux (Posh), Montana (Sassy),Gallagher (Friendly))
        [x] Change Voice (Based on machine's voices)

"""

#--------------------------------------------------------------------------

# Table of Contents

#--------------------------------------------------------------------------

# 1.0 SETUP
# 2.0 FUNCTIONS
# 3.0 BUILDING GUI
# 4.0 EXECUTION

#--------------------------------------------------------------------------

# 1.0 SETUP

#--------------------------------------------------------------------------

# LIBRARIES AND ADDONS

import json
from datetime import date, datetime
from tkinter import *
import requests
import pyttsx3

# INITIALIZE SOME THINGS

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# MAKE SOME CLASSES

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

# 2.0 FUNCTIONS

#--------------------------------------------------------------------------

def andNowTheWeather():
    # Get JSON from openweathermap.org and create an object using data
    # Formatted as: Temp, Description

    weatherRequest = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Orlando&units=imperial&appid=944d36db5865dfe678be92ab8f209646")
    data = weatherRequest.json()
    temp = data['main']['feels_like']
    desc = data['weather'][0]['description']
    return temp, desc

def timeIsAConstruct():
    # Get current date and time, and change assistant greeting a result
    # Formatted mm-dd-yyyy and 00:00 in the 12 hour system

    d = date.today()
    theDate = d.strftime("%B %d, %Y")
    t = datetime.now()
    theTime = t.strftime("%I:%M %p")

    return theDate, theTime

def butObeyWeMust():
    date, time = timeIsAConstruct()

    # CHECK: Is time AM or PM? Then, decide what time of day.
    # This is the epitome of creator bias.

    # AM
    currentHour = int(time[1])
    if time[6] == "A":
        if currentHour <= 4 or currentHour == 12:
            print("Happy Witching Hours")
        elif currentHour > 4 and currentHour <= 11:
            print("Good morning")
    # PM
    else:
        if currentHour == 12:
            print("It's high noon")
        elif currentHour >= 1 and currentHour <=3:
            print("Good afternoon")
        elif currentHour == 4 and currentHour <=7:
            print("Good evening")
        elif currentHour >= 8 and currentHour <= 11:
            print("Good night")

def grabSettings():
    # Sets values based on settings file on startup
    # By doing so, it allows the user to customize the application itself

    # Get JSON from settings file, remembering user preferences
    with open('settings.txt') as json_file:
        data = json.load(json_file)
        for d in data['user']:
            fname = d['fname']
            lname = d['lname']
            nickname = d['nickname']
            gender = d['gender']
        for d in data['assistant']:
            voice = d['id']
            a_name = d['name']
            a_honor = d['honor']
    # Set voice from settings
    engine.setProperty('voice', voice)
    # return values for use
    return fname, lname, nickname, gender

def updateSettings(changedValue,newValue):
    # Handles all changes to the assistant
    # Called several times throughout program

    # CHECK: see what value was changed
    # That way only certain parts of JSON file are edited

    # IF USER'S NAME WAS CHANGED
    #pseudocode

    # IF ASSISTANT'S NAME WAS CHANGED
    #pseudocode

    # IF ASSISTANT'S HONORIFIC WAS CHANGED
    #pseudocode

    # If ASSISTANT'S VOICE WAS CHANGED
    # Update the voice id in the JSON file with the new value
    if changedValue == "voice":
        with open('settings.txt') as json_file:
            data = json.load(json_file)
            data['assistant'][0]['id'] = newValue

        with open('settings.txt', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

def changeVoice():
    # List current voices on machine
    # Preprend number for user to select, if they decide to change it
    option = 0
    for voice in voices: 
        #print("ID: %s" %voice.id)
        print(option, voice.name)
        option += 1
    engine.say("These are the current voices on your machine:")
    engine.runAndWait()

    # CHECK: change voice
    engine.say("Would you like to change the voice?")
    engine.runAndWait()
    userinput = input("Would you like to change the voice? [y/n]")
    if userinput == "y":
        engine.say("Very well. Which voice would you like to use?")
        engine.runAndWait()
        userinput = int(input("Please enter the corresponding number."))
        voice_id = voices[userinput].id
        engine.setProperty('voice', voice_id)
        engine.say("Voice setting changed.")

        changedValue = "voice"
        newValue = voices[userinput].id
        updateSettings(changedValue,newValue)
    elif userinput == "n":
        engine.say("Very well, the voice will remain the same.")
    else:
        engine.say("That response doesn't work here.")
    engine.runAndWait()

def startup():
    # Initialize settings
    fname,lname,nickname,gender = grabSettings()
    theUser = User(fname,lname,nickname,gender)
    # Grab Weather NEED TO UNCOMMENT TO USE
    #temp,desc = andNowTheWeather()

    # Assistant greets User
    engine.say("Happy Witching Hours " +theUser.fname)
    engine.runAndWait()
    # Assistant discusses the weather
    # engine.say("It is currently " +str(temp) + "degrees in North Orlando.")
    #engine.runAndWait()

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


#--------------------------------------------------------------------------

# 4.0 EXECUTION

#--------------------------------------------------------------------------

#startup()