# DIG5508: Final Project
# Name: Alfred Pennyworth
# Time Spent: Rihanna-turning-hand.gif

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
from tkinter import *

# CLASSES

class User(object):
    def __init__(self, fname, lname, gender):
        self.fname = fname
        self.lname = lname
        self.gender = gender

# GRAB SETTINGS FROM JSON FILE
with open('settings.txt') as json_file:
    data = json.load(json_file)
    for d in data['user']:
        createUser = User(d['fname'],d['lname'],d['gender'])

print(createUser.fname)

#--------------------------------------------------------------------------

# FUNCTIONS

#--------------------------------------------------------------------------

#lsjkdgn

#--------------------------------------------------------------------------

# 3.0 BUIDING GUI

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