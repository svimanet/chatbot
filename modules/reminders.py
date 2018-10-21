from dateutil.parser import parse
import datetime
import time
import json
import os

def create_file(file):
    reminder = {}
    reminder["0"] = [["0", "0", "0"]]
    with open(file, "w+") as data_file:
        data_file.write(json.dumps(reminder, indent=4, sort_keys=True))
    return get_reminders()    


# Returns the list of reminders as dict.
# @return reminders - Python Dictionary
def get_reminders():
    file = "{}/reminders.json".format(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isfile(file):
        with open(file, "r") as data_file:
            reminders = json.load(data_file)
            return reminders
    else: create_file(file)


# Creates a reminder and writes it to file.
def set_reminder(nick, msg, date, time): 
    file = "{}/reminders.json".format(os.path.dirname(os.path.realpath(__file__)))
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
    info = []
    reminders = get_reminders()
    if not reminders == None:
        reminder = reminders.get(nick)
        if not reminder == None:
            info = ["{} reminders for {}:".format(len(reminder), nick)]
            for k, v in enumerate(reminder):
                future = parse(v[1]).date()
                today = datetime.date.today()
                diff = abs((future - today).days)

                reminder_x = "({} days left) {} {}: {}".format(diff, v[1], v[2], v[0])
                info.append(reminder_x)

        else: info = ["Found no reminders for {}.".foramt(nick)]
    else: return None

    for x in range(len(info)):
        print(info[x]) 

    return info

#set_reminder("svimanet", "msg", "26.10.18", "14:00")
remind("svimanet")