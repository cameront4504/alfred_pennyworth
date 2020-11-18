# DIG5508: Final Project
# Name: Personal Assistant App, Alfred
# Time Spent: Rihanna-turning-hand.gif

# TO DO LIST
"""

        - Streamline Thoughts
            + Maybe certain functions, like change name / change assist name could be combined?
            + Instead, dialogue and variables would change depending on what or who is being changed
            + Similarly, have all changes to settings.txt run through updateSettings
                - Use parameters to change what sections are affected
        - Things to Streamline:
            + JSON reading and writing? [x]
            +
            +
        - Remembrance:
            + Has user already interacted with assistant. If so, change some lines like
            + "What nickname would you like?" would be "What would you like to change your nickname to?"

"""

#--------------------------------------------------------------------------

# Table of (Relative) Contents

#--------------------------------------------------------------------------

# WIP functions have the string of ++++

# 1.0 SETUP
#       - Libraries / Addons
#       - Classes / Objects
# 2.0 FUNCTIONS
#       - startup: Begins program using the following functions
#           + andNowTheWeather: Grabs weather from openweathermap API
#           + timeIsAConstruct: Generates current date/time in specific format
#           + butObeyWeMust: Uses date/time data to change program greeting
#       - changeAssistantMenu: Features all stuff below
#           + changeVoice: Change assistant's voice
#           + changeAssistName: Change assistant's name
#           + changePersonality: Change assistant's personality +++++++++++++++++++++++++++++++++++++++++
#       - changePersonalMenu: Features all stuff below; update user information
#           + changeName: Self explanatory
#           + changeNickname: Self explanatory
#           + changeHonor: Change term of addressment (Sir, Ma'am, Serah, Madam, etc.) +++++++++++++++++++++++++++++++++++++++++
#       - updateSettings: Writes any changes to settings.txt via JSON
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
    def __init__(self, fname, lname, nickname):
        self.fname = fname
        self.lname = lname
        self.nickname = nickname

class Assistant(object):
    def __init__(self,name,status):
        self.name = name
        self.status = status

class Weather(object):
    def __init__(self,temp,desc):
        self.temp = temp
        self.desc = desc

#--------------------------------------------------------------------------

# 2.0 FUNCTIONS
#       - 2.1: Housekeeping & JSON
#       - 2.2: Changes to Assistant
#       - 2.3: Changes to User
#       - 2.4: Startup & Main Interface

#--------------------------------------------------------------------------

# 2.1 Startup & Housekeeping

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
    elif time[6] == "P":
        if currentHour == 12:
            timeGreeting = "A high noon to you"
        elif currentHour >= 1 and currentHour <=3:
            timeGreeting = "Good Afternoon"
        elif currentHour >= 4 and currentHour <=7:
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
        for d in data['assistant']:
            voice = d['id']
            a_name = d['name']
            a_bool = d['hasMetUser']
    # Set voice from settings
    engine.setProperty('voice', voice)
    # return values for user class
    return fname, lname, nickname, a_name, a_bool

def updateSettings(updateWho,changedValue,newValue):
    # Handles all changes to the assistant
    # First, open settings.txt and create a data from the readings
    with open('settings.txt') as json_file:
        data = json.load(json_file)

        # IF A NAME WAS UPDATED
        if changedValue == "name":
            if updateWho == "user":
                data['user'][0]['fname'] = newValue
            else:
                data['assistant'][0]['name'] = newValue
    
        # IF NICKNAME WAS ADDED
        if changedValue == "nickname":
            data['user'][0]['nickname'] = newValue

        # IF ASSISTANT VOICE WAS UPDATED
        if changedValue == "voice":
            with open('settings.txt') as json_file:
                data = json.load(json_file)
                data['assistant'][0]['id'] = newValue

    # WRITE TO SETTINGS.TXT     
    with open('settings.txt', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

# 2.2: Changes to Assistant

def changeVoice():
    # List current voices on machine
    # Preprend number for user to select, if they decide to change it
    option = 0
    for voice in voices:
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
        engine.say("Voice confirmed.")
        engine.runAndWait()
        updateWho = "assistant"
        changedValue = "voice"
        newValue = voices[newVoice].id
        updateSettings(updateWho,changedValue,newValue)
        
    elif userinput == "n":
        engine.say("Very well, the voice will remain the same.")
        engine.runAndWait()
    else:
        badResponse()

def changeAssistName(assist):
    engine.say("I'm currently called " + assist.name+ ". What would you like to call me?")
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
    updateWho = "assistant"
    changedValue = "name"
    newValue = assistName
    updateSettings(updateWho,changedValue,newValue)

def changeAssistantMenu(assist):
    engine.say("Here are your options. What would you like to change?")
    engine.runAndWait()
    userinput = int(input("""
        0. Rename Assistant
        1. Change Assistant Voice
    """))

    if userinput == 0:
        changeAssistName(assist)
    elif userinput == 1:
        changeVoice()

# 2.3: Changes to User

def changePersonalName(user):
    engine.say("What would you prefer to be called?")
    engine.runAndWait()
    newName = 0
    userinput = 0
    # Until a proper string is entered, ask for input
    while isinstance(newName, str) == False:
        newName = input("What would you prefer to be called?")

    while userinput != "y":
        engine.say("You've entered "+newName+". Is that correct?")
        engine.runAndWait()
        userinput = input("You've entered "+newName+". Is that correct? [y/n]")
        if userinput == "n":
            engine.say("I must have misheard. What would you prefer?")
            engine.runAndWait()
            newName = input("I must have misheard. What would you prefer?")

    # set new details and send to updateSettings
    updateWho = "user"
    changedValue = "name"
    newValue = newName
    updateSettings(updateWho,changedValue,newValue)

    # ask if user wants a nickname
    engine.say(newName+" it is. Would you like to have a nickname?")
    engine.runAndWait()
    nickname = 0
    userinput = input("Would you like to have a nickname?")
    if userinput == "y":
        engine.say("What nickname would you like?")
        engine.runAndWait()
        while isinstance(nickname, str) == False:
            nickname = input("What nickname would you like?")

        userinput = 0
        while userinput != "y":
            engine.say("You've entered "+nickname+". Is that correct?")
            engine.runAndWait()
            userinput = input("You've entered "+nickname+". Is that correct? [y/n]")
            if userinput == "n":
                engine.say("I must have misheard. What would you prefer?")
                engine.runAndWait()
                nickname = input("I must have misheard. What would you prefer?")
    else:
        nickname = user.fname
    # If nickname, send to updateSettings
    updateWho = "user"
    changedValue = "nickname"
    newValue = nickname
    updateSettings(updateWho,changedValue,newValue)

def changePersonalMenu(user):
    engine.say("Here are your options. What would you like to change?")
    engine.runAndWait()
    userinput = int(input("""
        0. Change Name And/Or Nickname
        1. ???? I don't know yet
    """))

    if userinput == 0:
        changePersonalName(user)
    elif userinput == 1:
        print("something")

# 2.4 Startup & Main Interface

def startup(user):
    # Grab Weather NEED TO UNCOMMENT TO USE
    # UNCOMMENT AT LAUNCH temp,desc = andNowTheWeather()

    # Assistant greets User
    greeting = butObeyWeMust()
    engine.say(greeting+" "+user.fname)
    engine.runAndWait()
    # Assistant discusses the weather
    #UNCOMMENT AT LAUNCH engine.say("It is currently " +str(temp) + "degrees in North Orlando.")
    engine.runAndWait()

def mainInterface(user,assist):
    # Main menu that launches after startup
    # Links to all other functions/menus/etc
    engine.say("What can I help you with?")
    engine.runAndWait()

    userinput = int(input("""
        0. option
        0. option
        1. Manage Personal Settings
        2. Manage Assistant Settings
    """))

    if userinput == 0:
        print("0")
    elif userinput == 1:
        changePersonalMenu(user)
    elif userinput == 2:
        changeAssistantMenu(assist)

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

# Startup

# Grab settings
fname, lname, nickname, a_name, a_bool = grabSettings()

# if User is using program for first time, run enchantee
# Aka run through questions to get values for settings.txt
# if a_bool == false:
    #enchantee() WIP

# Create objects from classes
theUser = User(fname,lname,nickname)
theAssistant = Assistant(a_name, a_bool)

# Initialize
startup(theUser)

# Main Menu
mainInterface(theUser,theAssistant)