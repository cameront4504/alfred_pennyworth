# DIG5508: Final Project
# Name: Personal Assistant App, Alfred
# Time Spent: Rihanna-turning-hand.gif

#--------------------------------------------------------------------------

# Table of (Relative) Contents

#--------------------------------------------------------------------------

# 1.0 SETUP
#       - Libraries / Addons
#       - Classes / Objects
# 2.0 FUNCTIONS (note: these are not by position, but by relationship and flow [[for my sanity]].)
#       - startup: Begins program using the following functions
#           + andNowTheWeather: Grabs weather from openweathermap API
#           + timeIsAConstruct: Generates current date/time in specific format
#       - changeAssistantMenu: Features all stuff below
#           + changeVoice: Change assistant's voice
#           + changeAssistName: Change assistant's name
#           + changePersonality: Change assistant's personality (WIP)
#           + updateSettings: Writes changes to settings.txt via JSON
#       - Other Stuff:
#           + badResponse: Called whenever user enters a bad value for input
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

def badResponse():
    engine.say("That response doesn't work here.")
    engine.runAndWait()

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
    timeGreeting = "default"
    if time[6] == "A":
        if currentHour <= 4 or currentHour == 12:
            timeGreeting = "Happy Witching Hours"
        elif currentHour >= 5 and currentHour <= 11:
            timeGreeting = "Good Morning"
    # PM
    else:
        if currentHour == 12:
            timeGreeting = "A high noon to you"
        elif currentHour >= 1 and currentHour <=3:
            timeGreeting = "Good Afternoon"
        elif currentHour == 4 and currentHour <=7:
            timeGreeting = "Good Evening"
        elif currentHour >= 8 and currentHour <= 11:
            timeGreeting = "Late tidings"
    return timeGreeting

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
    if changedValue == "name":
        with open('settings.txt') as json_file:
            data = json.load(json_file)
            data['assistant'][0]['name'] = newValue

        with open('settings.txt', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

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
        print(str(option)+". "+ voice.name)
        option += 1
    engine.say("These are the current voices on your machine:")
    engine.runAndWait()

    # CHECK: change voice
    engine.say("Would you like to swap for one?")
    engine.runAndWait()
    userinput = input("Would you like to swap for one? [y/n]")
    if userinput == "y":
        # keep looping through test until user selects voice
        # reset variables to use as bools, in a sense
        userinput = 0
        newVoice = 0
        while userinput != "y":
            engine.say("Very well. Which voice would you like?")
            engine.runAndWait()
            # Grab user input and test voice
            newVoice = int(input("Which voice would you like?"))
            voice_id = voices[newVoice].id
            engine.setProperty('voice', voice_id)
            engine.say("This is how it sounds, is that alright?")
            engine.runAndWait()
            userinput = input("This is how it sounds, is that alright?[y/n]")
        
        # update settings
        changedValue = "voice"
        newValue = voices[newVoice].id
        updateSettings(changedValue,newValue)
    elif userinput == "n":
        engine.say("Very well, the voice will remain the same.")
        engine.runAndWait()
    else:
        badResponse()

def changeAssistName():
    engine.say("What would you like to call me?")
    engine.runAndWait()
    assistName = 0
    userinput = 0
    # Until a proper string is entered, ask for input
    while isinstance(assistName, str) == False:
        assistName = input("What would like to call me?")

    while userinput != "y":
        engine.say("You've entered "+assistName+". Is that correct?")
        engine.runAndWait()
        userinput = input("You've entered "+assistName+". Is that correct? [y/n]")
        if userinput == "n":
            engine.say("I must have misheard. What would you prefer?")
            engine.runAndWait()
            assistName = input("I must have misheard. What would you prefer?")

    # set new details and send to updateSettings
    engine.say(assistName+" it is.")
    engine.runAndWait()
    changedValue = "name"
    newValue = assistName
    updateSettings(changedValue,newValue)

def changeAssistantMenu():
    engine.say("Here are your options. What would you like to change?")
    engine.runAndWait()
    userinput = int(input("""
        0. Rename Assistant
        1. Change Personality
        2. Change Assistant Voice
    """))

    if userinput == 0:
        changeAssistName()
    elif userinput == 1:
        print("change personality")
    elif userinput == 2:
        changeVoice()

def startup():
    # Initialize settings
    fname,lname,nickname,gender = grabSettings()
    theUser = User(fname,lname,nickname,gender)
    # Grab Weather NEED TO UNCOMMENT TO USE
    #temp,desc = andNowTheWeather()

    # Assistant greets User
    greeting = butObeyWeMust()
    engine.say(greeting+" "+theUser.fname)
    engine.runAndWait()
    # Assistant discusses the weather
    # engine.say("It is currently " +str(temp) + "degrees in North Orlando.")
    #engine.runAndWait()

def mainInterface():
    print("wow")

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
#mainInterface()