import time
import json
import os

# Returns the list of reminders as dict.
# @return reminders - Python Dictionary
def get_reminders():
    file = "{}/reminders.json".format(os.path.dirname(os.path.realpath(__file__)))
    with open(file, "r") as data_file:
        reminders = json.load(data_file)
    return reminders


# Creates a reminder and writes it to file.
def set_reminder(nick, msg, date, time): 
    # Checks if user has existing reminders; if so: append to user reminders. 
    reminders = get_reminders()
    reminder = {}
    if nick in reminders.keys():
        reminders[nick].append([msg, date, time])
        with open(file, "w+") as data_file:
            data_file.write(json.dumps(reminders, indent=4, sort_keys=True))
    else:
        reminders[nick] = [[msg, date, time]]
        with open(file, "w+") as data_file:
            data_file.write(json.dumps(reminders, indent=4, sort_keys=True))
    #print("After\n{}\n".format(reminders))


# Iterates over reminders and sends PM to users if time and date.
def remind(nick):
    
# test

set_reminder("hm","tannlege elns", "12.01.02","14:00")