# DIG5508: Final Project
# Name: Personal Assistant App, Alfred
# Time Spent: Rihanna-turning-hand.gif

"""
# TO DO LIST

        - Features:
            [ ] Recordkeeping
                    [ ] Scheduling
                    [x] Habits
                    [ ] Budgeting
                    [ ] Taste Tracker
            [ ] Entertainment
                    [ ] Games & Such
                            [x] Rock, Paper, Scissors
                            [ ] Upgraded Hangman(?)
                    [ ] Recommendations
                            [ ] By Genre
                            [ ] By Mood
            [ ] Research
                    [ ] BUG-ish: What to do if page lookup fails
                    [ ] BUG: Why does browser not open sometimes
            [ ] Games & Entertainment
            [x] Assistant Remembering User if interacted before
            [x] Settings JSON
            [x] Change Settings Functions
        - Cleanup / Streamlining
            [x] JSON reading and writing
            [x] Create speech function
                    [x] assistantSpeech(current):
                            engine.say(current)
                            engine.runAndWait()
                    [x] Go through functions and update with it
            [x] createMenu: Function that takes options variable and uses it to create input?
                    [x] Adapt current functions/menus

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
#       - recordKeeping: Encompasses group of functions below (WIP)
#               - dailyTracker: Bullet Journal -esque system
#                    + dailyTrackerNewTracker: Lets user append new tracker to settings.json
#                    + dailyTrackerAddEntry: Lets user add dated entry to an existing tracker
#                    + dailyTrackerViewAll: Lets user select a tracker and view all entries for it
#               - tasteTracker: Allows user to enter some values for daily interests
#       - recommendations: (WIP)
#       - research: Lets user look up stuff via wikipedia library
#
#       Settings //
#
#       - grabSettings: Gets some values from settings.json ()
#       - updateSettings: Writes any changes to settings.json via JSON
#       - resetPrompt: Leads to next function
#           + resetSettings: Reset program and any user data
#       - changeAssistantMenu: Features all stuff below
#           + changeAssistVoice: Change assistant's voice
#           + changeAssistName: Change assistant's name
#       - changePersonalMenu: Features all stuff below; update user information
#           + changeName: Change user's name and/or nickname
#
#       Other Stuff //
#
#       - doNotLetHimSpeak: Function that accepts a dialogue value and uses it to have assist talk
#         (cuts down on how many lines are written)
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
import random
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
    def __init__(self,name,status, personality):
        self.name = name
        self.status = status
        self.personality = personality

#--------------------------------------------------------------------------

# 2.0 FUNCTIONS

#--------------------------------------------------------------------------

def doNotLetHimSpeak(currentDialogue,printcheck):
    # IF followed by input, don't print
    if printcheck == True:
        print(currentDialogue)
    engine.say(currentDialogue)
    engine.runAndWait()

def createMenu(menu):
    # Not huge difference, but takes options from other place and uses it to make a menu
    # Spits out user input for local function use

    userinput = -1
    userinput = int(input(menu))

    return userinput

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
    with open('settings.json') as json_file:
        data = json.load(json_file)
        for d in data['user']:
            name = d['name']
            nickname = d['nickname']
        for d in data['assistant']:
            voice = d['id']
            a_name = d['name']
            a_bool = d['hasMet']
            a_per = d['personality']
    # Set voice from settings
    engine.setProperty('voice', voice)
    # return values for user class
    return name, nickname, a_name, a_bool, a_per

def updateSettings(updateWhat,changedValue,newValue):
    # Handles all changes to settings.json JSON
    # First, open settings.json and create a data from the readings
    with open('settings.json') as json_file:
        data = json.load(json_file)

        # IF FIRST TIME USER
        if changedValue == "status":
            data['assistant'][0]['hasMet'] = newValue

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

    # WRITE TO settings.json     
    with open('settings.json', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

def resetSettings():
    # Reset application to beginning state
    # Clear trackers, reset hasMet, etc.
    print("delete")

    # Reset settings.json
    with open('settings.json') as json_file:
        data = json.load(json_file)

        data['user'][0]['name'] = "Damian"
        data['user'][0]['nickname'] = "Daymi"
        data['assistant'][0]['name'] = "Alfred"
        data['assistant'][0]['hasMet'] = "False"


    with open('settings.json', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

def resetPrompt(user):
    current = "You have selected to reset the application."
    doNotLetHimSpeak(current,True)
    current = "This will reset your assistant, clear your user settings, and delete any stored data."
    doNotLetHimSpeak(current,True)

    current = "Is that ok?"
    doNotLetHimSpeak(current,False)
    userinput = input(current + "[y/n]")

    if userinput == "y":
        current = "Please enter your name to confirm."
        doNotLetHimSpeak(current,False)
        userinput = input(current + " (Your name is currently stored as "+user.name+".)")

        if userinput == user.name:
            resetSettings()

def changeAssistVoice():
    doNotLetHimSpeak("These are the current voices on your machine:",True)
    print("\n")

    # List current voices on machine
    # Preprend number for user to select, if they decide to change it
    option = 0
    for voice in voices:
        print(str(option)+". "+ voice.name)
        option += 1

     # keep looping through test until user selects voice
    # reset variables to use as bools, in a sense
    userinput = 0
    newVoice = 0
    while userinput != "y":
        current = "Which voice would you like?"
        doNotLetHimSpeak(current,False)
            
        # Grab user input and test voice
        newVoice = int(input(current))
        voice_id = voices[newVoice].id
        engine.setProperty('voice', voice_id)

        # test for feedback
        current = "This is how it sounds, is that alright?"
        doNotLetHimSpeak(current,False)
        userinput = input(current+" [y/n]")
        
    doNotLetHimSpeak("Voice confirmed.",True)

    # update settings
    updateWhat = "assistant"
    changedValue = "voice"
    newValue = voices[newVoice].id
    updateSettings(updateWhat,changedValue,newValue)

def changeAssistName(assist):
    current = "I'm currently called " + assist.name+ "."
    doNotLetHimSpeak(current,True)
    current= "What would you like to call me?"
    doNotLetHimSpeak(current,False)
    assistName = 0
    userinput = 0
    # Until a proper string is entered, ask for input
    while isinstance(assistName, str) == False:
        assistName = input(current)

    while userinput != "y":
        current = "You've entered "+assistName+". Is that correct?"
        doNotLetHimSpeak(current,False)
        userinput = input(current+" [y/n]")
        if userinput == "n":
            current = "I must have misheard. What would you prefer?"
            doNotLetHimSpeak(current,False)
            assistName = input(current)

    # set new details and send to updateSettings
    current = assistName+", it is."
    doNotLetHimSpeak(current,True)

    updateWhat = "assistant"
    changedValue = "name"
    newValue = assistName
    updateSettings(updateWhat,changedValue,newValue)

def changeAssistantMenu(assist):
    current = "Here are your options. What would you like to change?"
    doNotLetHimSpeak(current,True)

    options = """
        0. Rename Assistant
        1. Change Assistant Voice
    """
    userinput = createMenu(options)

    if userinput == 0:
        changeAssistName(assist)
    elif userinput == 1:
        changeAssistVoice()

def changePersonalName(user):
    current = "What would you prefer to be called?"
    doNotLetHimSpeak(current,False)

    newName = 0
    userinput = 0
    # Until a proper string is entered, ask for input
    while isinstance(newName, str) == False:
        newName = input(current)

    while userinput != "y":
        current = "You've entered "+newName+". Is that correct?"
        doNotLetHimSpeak(current,False)
        userinput = input(current+" [y/n]")
        if userinput == "n":
            current = "I must have misheard. What would you prefer?"
            doNotLetHimSpeak(current,False)
            newName = input(current)

    # set new details and send to updateSettings
    user.name = newName
    updateWhat = "user"
    changedValue = "name"
    newValue = newName
    updateSettings(updateWhat,changedValue,newValue)

    # ask if user wants a nickname
    current = newName+", it is. Would you like to have a nickname?"
    doNotLetHimSpeak(current,False)
    nickname = 0
    userinput = input(current + "[y/n]")
    if userinput == "y":
        current = "What nickname would you like?"
        doNotLetHimSpeak(current,False)
        while isinstance(nickname, str) == False:
            nickname = input(current)

        userinput = 0
        while userinput != "y":
            current = "You've entered "+nickname+". Is that correct?"
            doNotLetHimSpeak(current,False)
            userinput = input(current+" [y/n]")
            if userinput == "n":
                current = "I must have misheard. What would you prefer?"
                doNotLetHimSpeak(current,False)
                nickname = input(current)
    else:
        nickname = user.name
    # If nickname, send to updateSettings
    updateWhat = "user"
    changedValue = "nickname"
    newValue = nickname
    updateSettings(updateWhat,changedValue,newValue)

def changePersonalMenu(user):
    doNotLetHimSpeak("Here are your options. What would you like to change?",True)

    userinput = int(input("""
        0. Change Name And/Or Nickname
        1. WIP
    """))

    if userinput == 0:
        changePersonalName()
    elif userinput == 1:
        print("wippppp")
    else:
        print("exited")

def recordKeeping():
    doNotLetHimSpeak("What would you like to check?",True)

    options = """
        0. Budgeting (WIP)
        1. Scheduling (WIP)
        2. Daily Task Trackers
        3. Taste Tracking
    """
    userinput = createMenu(options)

    if userinput == 0:
        print("budgeting")
    elif userinput == 1:
        print("scheduling")
    elif userinput == 2:
        dailyTrackers()
    elif userinput == 3:
        tasteTracker()
    else:
        doNotLetHimSpeak("Back to work then.",True)

def updateTrackers(tracker,entry):
    # Similar to updateSettings, but userdata.json
    # I want to keep most of the JSON affecting stuff together if I can
    with open('userdata.json') as json_file:
        data = json.load(json_file)

        checkExists = False
        id = -1

        # CHECK IF TRACKER IS NEW
        # Iterate over data to see if value exists, ignore case
        for d in data['trackers']:
            if d['name'].lower() == tracker.lower():
                id = int(d['id'])
                checkExists = False
                break
            else:
                checkExists = True

        # IF NEW, ADD TO FILE
        if checkExists == True:
            lastID = int(data['trackers'][-1]['id'])
            nextID = str(lastID + 1)
            newTracker = {
                "id": ""+nextID+"",
                "name": ""+tracker+"",
                "entries": []
                }
            data['trackers'].append(newTracker)
        else:
            data['trackers'][id]['entries'].append(entry)

    # WRITE TO userdata.json     
    with open('userdata.json', 'w') as json_file:
            json_file.write(json.dumps(data,indent=4))

def dailyTrackerAddEntry():
    # Display current Trackers by ID
    current = "These are your current Trackers:"
    doNotLetHimSpeak(current,True)

    with open('userdata.json') as json_file:
        data = json.load(json_file)
        for d in data['trackers']:
            print("""        """+
            d['id'] +". "+ d['name']+""" """)

        current = "Which would you like to add an entry for?"
        doNotLetHimSpeak(current,False)
        userinput = int(input(current))

        tracker = data['trackers'][userinput]['name']
        d,_ = timeIsAConstruct()
        dateFormatted = d.strftime("%m_%d_%Y")

        current = "Do you want to mark today's entry for complete or incomplete?"
        doNotLetHimSpeak(current,False)           
        entry = int(input(current+" [1/0]"))

        current = "Entry marked."
        doNotLetHimSpeak(current, True)

        newEntry = dateFormatted+": "+str(entry)
        newValue = newEntry
        updateTrackers(tracker,newEntry)

def dailyTrackerNewTracker():
    newTracker = 0
    current = "What would you like to call this tracker?"
    doNotLetHimSpeak(current,False)
    while isinstance(newTracker, str) == False:
        newTracker = input(current)

    userinput = 0
    current = "You've entered "+newTracker+". Is that correct?"
    while userinput != "y":
        doNotLetHimSpeak(current,False)
        userinput = input(current+" [y/n]")
        if userinput == "n":
            current = "I must have misheard. What would you like to call this tracker?"
            doNotLetHimSpeak(current,False) 
            newTracker = input(current)

    # Send new Tracker to settings.json for update/append
    # Second value is boogey, basically
    updateTrackers(newTracker,newTracker)

    # check if user wants to add an entry immediately
    # if so, switch to dailyTrackerAddEntry
    userinput = 0
    current = "Would you like to add an entry for this tracker today?"
    doNotLetHimSpeak(current,False)
    userinput = input(current+" [y/n]")

    if userinput == "y":
        userinput = 0
        d,_ = timeIsAConstruct()
        dateFormatted = d.strftime("%m_%d_%Y")
        
        current = "Do you want to mark today's entry for complete or incomplete?"
        doNotLetHimSpeak(current,False)
        entry = input(current+" [1/0]")

        newEntry = dateFormatted+": "+entry
        newValue = newEntry
        updateTrackers(newTracker,newEntry)

        current = "Tracker updated."
        doNotLetHimSpeak(current,True)

def dailyTrackersViewAll():
    # Display current Trackers by ID
    current = "These are your current Trackers:"
    doNotLetHimSpeak(current,True)
    print("\n")

    with open('userdata.json') as json_file:
        data = json.load(json_file)
        for d in data['trackers']:
            print(d['id'] +". "+ d['name'])

        current = "For which would you like to view the entries?"
        doNotLetHimSpeak(current,False)
        userinput = int(input("\n"+current+"\n"))

        # Grab all entries and split by date and status (complete/incomplete)
        # Don't need to rid of : necessarily, but might do some stuff here in future
        entries = data['trackers'][userinput]['entries']
        translateStatus = "Translate"
        print(data['trackers'][userinput]['name']+":")
        for entry in entries:
            cleaned = entry.replace(":"," ")
            date,status = cleaned.split("  ",1)
            # Translate binary to more human friendly terms
            if status == "1":
                translateStatus = "Complete"
            else:
                translateStatus = "Incomplete"
            print(date+": "+ translateStatus)

def dailyTrackers():
    # section for keeping track of habits
    # Ex: did dishes today, drank enough water, did SOME homework at least

    current = "These are a few of the things you can do."
    doNotLetHimSpeak(current,True)

    options = """
        0. Create a new tracker
        1. Create an entry for an existing tracker
        2. Edit an entry for an existing tracker (WIP)
        3. View all entries for an existing tracker
    """
    userinput = createMenu(options)

    if userinput == 0:
        dailyTrackerNewTracker()
    elif userinput == 1:
        dailyTrackerAddEntry()
    elif userinput == 2:
        print("edit entry")
    elif userinput == 3:
        dailyTrackersViewAll()
    else:
        doNotLetHimSpeak("Back to work then.",True)

# WIP ----------------------------------------------------------------------------------------------------------

def tasteTracker():
    # Inspired by those silly updates on deviantArt
    # (CURRENTLY) What have you been up to:
    #    Listening to, playing, watching, eating, quote of the day
    print("Tastes")

def birthdays():
    # section to add birthdays or edit current entries

    # update my birthday
    # add a birthday for someone else
    # edit an entry (need in case date wrong?)
    # delete an entry oof ouchies
    print("Birthdays")

# WIP ----------------------------------------------------------------------------------------------------------

def research():
    current = "What would you like to research?"
    doNotLetHimSpeak(current,False)

    # get input and then search using Wikipedia API, limit 2 sentences
    # print first because this'll probably take a bit for talks
    topic = input (current)
    print(wikipedia.summary(topic, sentences=2))
    current = "According to Wikipedia: "+wikipedia.summary(topic, sentences=2)
    doNotLetHimSpeak(current,False)

    current = "Does that answer your questions? Otherwise, here are some other options."
    doNotLetHimSpeak(current,True)

    options = ("""
        0. Open Page in Browser
        1. Lookup Something Else
        2. Finish Research
    """)
    userinput = createMenu(options)

    if userinput == 0:
        # BUG x 2
        # Why won't you open bud!
        url = "https://en.wikipedia.org/wiki/"+topic
        webbrowser.open(url, new=2)
    elif userinput == 1:
        research()

def wiiWouldLikeToPlay():
    # Ideally, the assistant would randomly grab one of several games to play.
    # Realistically, I'm offering rock, paper, and scissors right now but that's boring so:

    # Fire Emblem System

    # Lance beats SWORD
    # Sword beats AXES
    # Axe beats LANCE

    current = "Sure! Let's try a game of rock paper scissors. Of sorts."
    doNotLetHimSpeak(current,True)

    current = "Which would you prefer?"
    doNotLetHimSpeak(current,True)

    rounds = 3
    roundsPlayed = 0
    userPoints = 0
    assistPoints = 0

    while roundsPlayed < rounds:
        roundsPlayed += 1
        weapons = ["lance","axe","sword"]
        assistattack = random.choice(weapons)
        userattack = ""
        options = """
            0. A Sword
            1. A Lance
            2. An Axe
        """
        # Check play input
        while (userattack != 0 and userattack != 1 and userattack != 2):
            userattack = int(input(options))
        
        # Translate selection
        if userattack == 0:
            userattack = "sword"
        elif userattack == 1:
            userattack = "lance"
        elif userattack == 2:
            userattack = "axe"

        feedback = ["Here are the results.","Here's how the battle progressed.","Here's how the round went."]
        current = random.choice(feedback)
        doNotLetHimSpeak(current,False)

        # REVEAL MATCHUP
        print("ROUND "+str(roundsPlayed)+" -----------------------------\n")
        print("Your assistant brandishes their " + assistattack + "!")
        print("You draw your " + userattack + "!\n")

        # IF A TIE
        if userattack == assistattack:
            print("You're both standing still, evenly matched!")
        # ELSE TALLY SCORES FOR JUDGEMENT
        elif userattack == "lance" and assistattack == "sword":
            userPoints += 1
            print("Success! Your weapon has the advantage!")
        elif userattack == "sword" and assistattack == "axe":
            userPoints += 1
            print("Success! Your weapon has the advantage!")
        elif userattack == "axe" and assistattack == "lance":
            userPoints += 1
            print("Success! Your weapon has the advantage!")
        else:
            assistPoints += 1
            print("A travesty! Your weapon is at a disadvantage!")
        
        if roundsPlayed != 3:
            print("\nEND ROUND ----------------------------\n")
            current = "Which would you prefer for Round "+str(roundsPlayed+1)+"?"
            doNotLetHimSpeak(current,True)

    # Check who won by comparing points
    if userPoints > assistPoints:
        winner = "user"
    elif userPoints < assistPoints:
        winner = "assistant"
    else:
        winner = "none"

    # END MATCH
    # Game End #1: Not Today
    if winner == "user":
        print("They battled fiercely, but you won!")
        
        current = "Fantastic sporting, Serah!"
        doNotLetHimSpeak(current,True)
    # Game End #2: Death Comes for All of Us
    elif winner == "assistant":
        print("You battled fiercely, but they won!")
        
        current = "Good luck next time, Serah."
        doNotLetHimSpeak(current,True)
    # Game End #4: New Best Buds
    else:
        print("A draw!\nYou sense your Assistant's budding respect--\nAnd you buy each other sangria. Or juice, if you prefer.""")

        current = "Good show, Serah!"
        doNotLetHimSpeak(current,True)

def entertainmentMenu():
    current = "What would you like to do?"
    doNotLetHimSpeak(current,True)

    options = """
        0. Play a Game
        1. Get a Recommendation (WIP)
    """
    userinput = createMenu(options)

    if userinput == 0:
        wiiWouldLikeToPlay()
    elif userinput == 1:
        print("recommendations")
    else:
        doNotLetHimSpeak("Back to work then.",True)

def enchantee(user,assist):
    current = "Hello. Welcome to your personal assistant application. To begin, let's set up your user configuration."
    doNotLetHimSpeak(current,True)
    changePersonalName(user)

    current = "Now, let's set up a profile for your assistant."
    doNotLetHimSpeak(current,True)
    changeAssistVoice()
    current = "How about a name?"
    doNotLetHimSpeak(current,True)
    changeAssistName(assist)

    current = "I'm pleased to meet you "+user.name+"."
    doNotLetHimSpeak(current,True)

    # Set hasMet status to True
    updateWhat = "assistant"
    changedValue = "status"
    newValue = "True"
    updateSettings(updateWhat,changedValue,newValue)

def startup(user):
    # Grab Weather
    temp,desc = andNowTheWeather()

    # Assistant greets User
    greeting = butObeyWeMust()
    current = greeting+" "+user.name+"."
    doNotLetHimSpeak(current,True)

    # Assistant discusses the weather
    current = "It is currently " +str(temp) + " degrees in North Orlando."
    doNotLetHimSpeak(current,True)

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
name, nickname, a_name, a_bool, a_per = grabSettings()

# Create objects from classes
theUser = User(name,nickname)
theAssistant = Assistant(a_name, a_bool, a_per)

# check if first-time user

if theAssistant.status == "False":
    enchantee(theUser,theAssistant)
else:
    startup(theUser)

# Main menu that launches after startup
# Links to all other functions/menus/etc

current = "What can I help you with?"
doNotLetHimSpeak(current,True)

options = """
    0. Recordkeeping
    1. Research & Information
    2. Recommendations & Entertainment
    3. Manage Personal Settings
    4. Manage Assistant Settings
    5. Reset Application

    Exit with any other key.
"""
userinput = createMenu(options)

if userinput == 0:
    recordKeeping()
elif userinput == 1:
    research()
elif userinput == 2:
    entertainmentMenu()
elif userinput == 3:
    changePersonalMenu(theUser)
elif userinput == 4:
    changeAssistantMenu(theAssistant)
elif userinput == 5:
    resetPrompt(theUser)
else:
    doNotLetHimSpeak("Back to work then.",True)
