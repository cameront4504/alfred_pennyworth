# DIG5508: Final Project
# Name: Personal Assistant App, Alfred
# Time Spent: Rihanna-turning-hand.gif

"""
# TO DO LIST

        - Features:
            [ ] Recordkeeping
                    - Scheduling
                    - Habits
                    - Budgeting
                    - Taste Tracker
            [ ] Recommendations
                    - By Genre
                    - By Mood
            [ ] Research
                    - BUG: What to do if page lookup fails
                    - BUG: Why does browser not open sometimes
            [ ] Games & Entertainment
            [x] Assistant Remembering User if interacted before
            [x] Settings JSON
            [x] Change Settings Functions
        - Cleanup / Streamlining
            [x] JSON reading and writing?
            [ ] User Input (Have checkUserInput that accepts options parameter; use array of options to print(?))
            [ ] Creating local variables for dialogue / printing (what is spoken and printed)

ex user input

menu = settings
current = "string"
voice.says(current)
input(string)

so condensed:

while userinput != "y":
    string = "im a question"
    engine.say(string)
    engine.runAndWait()
    userinput = input(string+" [y/n]")
    if userinput == "n":
        engine.say("I must have misheard. What would you prefer?")
        engine.runAndWait()
        newName = input("I must have misheard. What would you prefer?")

how to clean yes/no check?

def checkUserInput():
    if menu == "dailytracker"
        string = "Im a question related to trackers"
    elif menu == "changeVoice"
        string = "Would you like to change voice?"
    while userinput != "y":
        engine.say(string)
        engine.runAndWait()
        userinput = input(string+" [y/n]")
        if userinput == "n":
            engine.say("I must have misheard. What would you prefer?")
            engine.runAndWait()
            newName = input("I must have misheard. What would you prefer?")

Instead of repeating so many lines that do same thing? Maybe, but does it help clarity?

"""

#--------------------------------------------------------------------------

# Table of (Relative) Contents

#--------------------------------------------------------------------------

# 1.0 SETUP
#
#       - Libraries / Addons
#       - Classes / Objects
#
# 2.0 FUNCTIONS (relationship based, see outline for positions)
#
#       Startup / Initialize //
#
#       - enchantee: Checks if user's first time running program, and if so, runs several of main functions
#       - startup: Begins program using the following functions
#           + andNowTheWeather: Grabs weather from openweathermap API
#           + timeIsAConstruct: Generates current date/time in specific format
#           + butObeyWeMust: Uses date/time data to change program greeting
#
#       Main Functions //
#
#       - mainMenu: Main menu of sorts, grants access to app's primary functions
#       - recordKeeping
#       - dailyTracker: Bullet Journal -esque system
#           + dailyTrackerNewTracker: Lets user append new tracker to settings.txt
#           + dailyTrackerAddEntry: Lets user add dated entry to an existing tracker
#             (Ex: November 20: Marked Yes for Doing the Dishes)
#       - recommendations:
#       - research: Lets user look up stuff via wikipedia library
#
#       Settings //
#
#       - updateSettings: Writes any changes to settings.txt via JSON
#       - changeAssistantMenu: Features all stuff below
#           + changeAssistVoice: Change assistant's voice
#           + changeAssistName: Change assistant's name
#       - changePersonalMenu: Features all stuff below; update user information
#           + changeName: Change user's name and/or nickname
#
#       Other Stuff
#
#       - Housekeeping Stuff
#       - Cut Content: Birthdays, Looking Ahead
#
# 3.0 BUILDING GUI (WIP)
#
# 4.0 EXECUTION

#--------------------------------------------------------------------------

# 1.0 SETUP

#--------------------------------------------------------------------------

# LIBRARIES AND ADDONS

# The Basics
import json
from datetime import date, datetime

# API and Web browser related
import requests
import wikipedia    # example: wikipedia.summary("Albert Einstein", sentences=2)
import webbrowser   # example: webbrowser.open('urlgoeshere', new=2)

# Assistant-Related
#from tkinter import *
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# MAKE SOME CLASSES

class User(object):
    def __init__(self, name, nickname):
        self.name = name
        self.nickname = nickname

class Assistant(object):
    def __init__(self,name,status):
        self.name = name
        self.status = status

class Tracker(object):
    def __inite__(self,name,date,entries,entry):
        self.name = name
        self.date = date
        self.entries = entries
        self.entry = entry

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
    t = datetime.now()
    return d,t

def butObeyWeMust():
    d, t = timeIsAConstruct()
    date = d.strftime("%B %d, %Y")
    time = t.strftime("%I:%M %p")

    # CHECK: Is time AM or PM? Then, decide what time of day.
    # This is the epitome of creator bias.
    # AM
    currentHour = int(time[1])
    timeGreeting = "Hello"
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
            name = d['name']
            nickname = d['nickname']
        for d in data['assistant']:
            voice = d['id']
            a_name = d['name']
            a_bool = d['hasMetUser']
    # Set voice from settings
    engine.setProperty('voice', voice)
    # return values for user class
    return name, nickname, a_name, a_bool

def updateSettings(updateWhat,changedValue,newValue):
    # Handles all changes to settings.txt JSON
    # First, open settings.txt and create a data from the readings
    with open('settings.txt') as json_file:
        data = json.load(json_file)

        # IF FIRST TIME USER
        if changedValue == "status":
            data['assistant'][0]['hasMetUser'] = newValue

        # IF A NAME WAS UPDATED
        if changedValue == "name":
            if updateWhat == "user":
                data['user'][0]['name'] = newValue
            else:
                data['assistant'][0]['name'] = newValue
    
        # IF NICKNAME WAS ADDED
        if changedValue == "nickname":
            data['user'][0]['nickname'] = newValue

        # IF ASSISTANT VOICE WAS UPDATED
        if changedValue == "voice":
            data = json.load(json_file)
            data['assistant'][0]['id'] = newValue

        # IF A NEW TRACKER WAS ADDED
        if changedValue == "newTracker":
            lastID = int(data['trackers'][-1]['id'])
            nextID = str(lastID + 1)
            newTracker = {
                "id": ""+nextID+"",
                "name": ""+newValue+"",
                "entries": []
                }
            data['trackers'].append(newTracker)
        
        # IF A TRACKER ENTRY WAS ADDED
        # this works if new tracker, but what about old ones?
        if changedValue == "trackerEntry":
            id = int(data['trackers'][-1]['id'])
            data['trackers'][id]['entries'].append(newValue)

    # WRITE TO SETTINGS.TXT     
    with open('settings.txt', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

def changeAssistVoice():
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
        updateWhat = "assistant"
        changedValue = "voice"
        newValue = voices[newVoice].id
        updateSettings(updateWhat,changedValue,newValue)
        
    elif userinput == "n":
        engine.say("Very well, the voice will remain the same.")
        engine.runAndWait()

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
    updateWhat = "assistant"
    changedValue = "name"
    newValue = assistName
    updateSettings(updateWhat,changedValue,newValue)

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
        changeAssistVoice()

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
    updateWhat = "user"
    changedValue = "name"
    newValue = newName
    updateSettings(updateWhat,changedValue,newValue)

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
        nickname = user.name
    # If nickname, send to updateSettings
    updateWhat = "user"
    changedValue = "nickname"
    newValue = nickname
    updateSettings(updateWhat,changedValue,newValue)

def changePersonalMenu(user):
    engine.say("Here are your options. What would you like to change?")
    engine.runAndWait()
    userinput = int(input("""
        0. Change Name And/Or Nickname
        1. WIP
    """))

    if userinput == 0:
        changePersonalName()
    elif userinput == 1:
        print("something")
    else:
        print("bye")

# WIP ----------------------------------------------------------------------------------------------------------

def recordKeeping():
    engine.say("What would you like to check?")
    engine.runAndWait()

    userinput = -1
    userinput = int(input("""
        0. Budgeting (WIP)
        1. Scheduling (WIP)
        2. Daily Task Trackers
        3. Current Taste Trackers (WIP)
    """))

    if userinput == 0:
        print("budgeting")
    elif userinput == 1:
        print("scheduling")
    elif userinput == 2:
        dailyTrackers()
    elif userinput == 3:
        tasteTracker()
    else:
        engine.say("Back to work then.")
        engine.runAndWait()

def dailyTrackerAddEntry():
    print("daily entry added")

def dailyTrackerNewTracker():
    newTracker = 0
    current = "What would you like to call this tracker?"
    engine.say(current)
    engine.runAndWait()
    while isinstance(newTracker, str) == False:
        newTracker = input(current)

    userinput = 0
    current = "You've entered "+newTracker+". Is that correct?"
    while userinput != "y":
        engine.say(current)
        engine.runAndWait()
        userinput = input(current+" [y/n]")
        if userinput == "n":
            engine.say("I must have misheard. What would you like to call this tracker?")
            engine.runAndWait()
            newTracker = input("I must have misheard. What would you like to call this tracker?")

    # Send new Tracker to settings.txt for update/append
    updateWhat = "trackers"
    changedValue = "newTracker"
    newValue = newTracker
    updateSettings(updateWhat,changedValue,newValue)

    # check if user wants to add an entry immediately
    # if so, switch to dailyTrackerAddEntry
    userinput = 0
    current = "Would you like to add an entry for this tracker today?"
    engine.say(current)
    engine.runAndWait()
    userinput = input(current+" [y/n]")

    if userinput == "y":
        userinput = 0
        d,_ = timeIsAConstruct()
        dateFormatted = d.strftime("%m_%d_%Y")

        updateWhat = "trackers"
        changedValue = "newEntry"
        
        entry = input("Do you want to mark today's entry for complete or incomplete?[1/0]")

        newEntry = dateFormatted+": "+entry

        updateWhat = "trackers"
        changedValue = "trackerEntry"
        newValue = newEntry
        updateSettings(updateWhat,changedValue,newValue)

def dailyTrackers():
    # section for keeping track of habits
    # Ex: did dishes today, drank enough water, did SOME homework at least
    print("daily trackers")

    # make new tracker
    # add an entry for a tracker
    # edit an entry (need in case date wrong?)
    # view all entries for tracker

    userinput = -1
    userinput = int(input("""
        0. Create a new tracker
        1. Create an entry for an existing tracker
        2. Edit an entry for an existing tracker (WIP)
        3. View all entries for an existing tracker (WIP)
    """))

    if userinput == 0:
        dailyTrackerNewTracker()
    elif userinput == 1:
        dailyTrackerAddEntry()
    elif userinput == 2:
        print("edit entry")
    elif userinput == 3:
        print("view all entries")
    else:
        engine.say("Back to work then.")
        engine.runAndWait()

def tasteTracker():
    # Inspired by those silly updates on deviantArt
    # (CURRENTLY) What have you been up to:
    #    Listening to, playing, watching, eating, quote of the day
    print("Taste Tracker")

# def lookingAhead():
    # section for goals, upcoming events, and other things of note
    #    print("looking ahead")

#def birthdays():
    # section to add birthdays or edit current entries

    # update my birthday
    # add a birthday for someone else
    # edit an entry (need in case date wrong?)
    # delete an entry oof ouchies

def recommendations():
    # section to get a song recommendation
    # By genre, mood, or, if tastes have been updated, maybe compile some by genre???
    print("Recommendations menu")

# WIP ----------------------------------------------------------------------------------------------------------

def research():
    engine.say("what would you like to research?")
    engine.runAndWait()

    topic = input ("What would you like to research?")
    print(wikipedia.summary(topic, sentences=2))
    engine.say("According to Wikipedia: "+wikipedia.summary(topic, sentences=2))
    engine.runAndWait()

    engine.say("Does that answer your questions? Otherwise, here are some other options.")
    engine.runAndWait()
    userinput = -1
    userinput = input("""Does that answer your questions? Otherwise, here are some other options.
        0. Open Page in Browser
        1. Lookup Something Else
        2. Finish Research""")

    if userinput == 0:
        # BUG x 2
        url = "https://en.wikipedia.org/wiki/"+topic
        webbrowser.open(url, new=2)
    elif userinput == 1:
        research()

def enchantee(user,assist):
    engine.say("Hello. Welcome to ALFRED, a personal assistant application. To begin, let's set up your user configuration.")
    engine.runAndWait()

    changePersonalName(user)

    engine.say("Now, let's set up a profile for your assistant.")
    engine.runAndWait()

    changeAssistVoice()

    engine.say("What about a name?")
    engine.runAndWait()

    changeAssistName(assist)

    engine.say("I'm pleased to meet you "+user.name)
    engine.runAndWait()

    updateWhat = "assistant"
    changedValue = "status"
    newValue = "True"
    updateSettings(updateWhat,changedValue,newValue)

def startup(user):
    # Grab Weather NEED TO UNCOMMENT TO USE
    ################################temp,desc = andNowTheWeather()

    # Assistant greets User
    greeting = butObeyWeMust()
    engine.say(greeting+" "+user.name)
    engine.runAndWait()
    # Assistant discusses the weather
    ################################engine.say("It is currently " +str(temp) + "degrees in North Orlando.")
    engine.runAndWait()

def mainMenu(user,assist):
    # Main menu that launches after startup
    # Links to all other functions/menus/etc
    engine.say("What can I help you with?")
    engine.runAndWait()

    userinput = -1
    userinput = int(input("""
        0. Recordkeeping
        1. Recommendations (WIP)
        2. Research & Information
        3. Manage Personal Settings
        4. Manage Assistant Settings
    """))

    if userinput == 0:
        recordKeeping()
    elif userinput == 1:
        print("recommendations")
    elif userinput == 2:
        research()
    elif userinput == 3:
        changePersonalMenu(user)
    elif userinput == 4:
        changeAssistantMenu(assist)
    else:
        engine.say("Back to work then.")
        engine.runAndWait()

#--------------------------------------------------------------------------

# 3.0 BUILDING GUI

#--------------------------------------------------------------------------

# Honestly, this is probably going to get relegated to next semester or post-thesis

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
name, nickname, a_name, a_bool = grabSettings()

# Create objects from classes
theUser = User(name,nickname)
theAssistant = Assistant(a_name, a_bool)

# check if first-time user
if a_bool == "False":
    enchantee(theUser,theAssistant)
else:
    startup(theUser)

mainMenu(theUser,theAssistant)
