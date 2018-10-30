from dateutil.parser import parse
import datetime
import time
import json
import pytz
import os


def create_file(file):
    """ Creates data file if none present 
    :return reminders: Python dict containing reminders. 
    """
    reminder = {}
    reminder["Null"] = [["10.10.18", "Null"]]
    with open(file, "w+") as data_file:
        data_file.write(json.dumps(reminder, indent=4, sort_keys=True))
    return get_reminders()    


def get_reminders():
    """ Retrieves the list of reminders.
    :return reminders: Python dict containing reminders.
    """
    file = "{}/reminders.json".format(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isfile(file):
        with open(file, "r") as data_file:
            reminders = json.load(data_file)
            return reminders
    else: create_file(file)


def set_reminder(nick, msg): 
    """ Creates a reminder and either creates user data or appends to user data.

    :param nick: The users nickname to connect the reminder to.
    :param msg: The users string input declaring a reminder.
    :return String: String response to user. 
    """
    try:
        file = "{}/reminders.json".format(os.path.dirname(os.path.realpath(__file__)))
        remind_msg = parse_inp(msg)
        reminders = get_reminders()
        reminder = {}

        if nick in reminders.keys():
            reminders[nick].append([remind_msg[0], remind_msg[1]])
        else:
            reminders[nick] = [[remind_msg[0], remind_msg[1]]]
        with open(file, "w+") as data_file:
            data_file.write(json.dumps(reminders, indent=4, sort_keys=True))
        return "Reminder created for: {} {}".format(remind_msg[0], remind_msg[1])
    except Exception as e:
        print(e)
        return "Couldn't set reminder. '!remind 10.11.18 message here'"

def parse_inp(inp):
    """ Used to handle incoming 'set_reminder' strings. 

    :param inp: User input, from IRC, as string.
    :return list: User input as an ordered list.
    """
    msg = inp.split(" ")
    date = msg[0]
    content = ""
    del msg[0]
    for x in range(len(msg)):
        content += "{} ".format(msg[x])
    return [date, time, content]


def check_reminders(nick):
    """ Checks if the given user has any reminders.

    :param nick: The users nickname.
    :return info: String containing reminders. 
    """
    info = []
    reminders = get_reminders()
    if not reminders == None:
        reminder = reminders.get(nick)
        if not reminder == None:
            info = ["{} reminders for {}:".format(len(reminder), nick)]
            for k, v in enumerate(reminder):
                future = parse(v[0]).date()
                today = datetime.date.today()
                diff = abs((future - today).days)
                r = "({} days left) {} : {}".format(diff, v[0], v[1])
                info.append(r)
                
        else: info = ["Found no reminders for {}.".foramt(nick)]
    else: return None
    return info


def daily_reminder():
    """ Iterates through users and reminders.
    Sends a reminder to nick for each reminder due in 7 days or less. 
    
    :param when: Hour of day to send reminders.
    :return notify: List of reminders to ping users about.
    """
    print("DAILY REMINDERS")
    notify = {}
    reminders = get_reminders()
    for k, v in enumerate(reminders):
        user = reminders.get(v)
        for x in range(len(user)):
            rdate = datetime.datetime.strptime(user[x][0], "%d.%m.%y").strftime("%Y-%m-%d")
            future = parse(rdate).date()
            today = datetime.date.today()
            diff = abs((future - today).days)
            if diff <= 2:
                if v in notify.keys():
                    notify[v].append(user[x])
                else:
                    notify[v] = [user[x]]
    return notify
    

#print(set_reminder("test", "03.11.18 14:00 wow"))
#print(daily_reminder())
#for k, v in enumerate(dr):
#    #print(len(dr[v]), dr[v])
#    for x in range(len(dr[v])):
#        msg = "{} {} -- {}".format(dr[v][x][0], dr[v][x][1], dr[v][x][2])
#        print(msg)