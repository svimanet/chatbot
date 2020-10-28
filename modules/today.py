from lxml import etree as ET
import requests
import random

def get_todays_day():
    req = requests.get('https://www.checkiday.com/rss.php?tz=Europe/Oslo') # TODO: Add timezone to config and utilize
    result = ET.fromstring(req.content)
    things = [thing[1].text for thing in result.iter('item')]
    return random.choice(things)

def get_todays_day_all():
    req = requests.get('https://www.checkiday.com/rss.php?tz=Europe/Oslo') # TODO: Add timezone to config and utilize
    result = ET.fromstring(req.content)
    things = [thing[0].text for thing in result.iter('item')]

    msg = "Today is "
    for x, value in enumerate(things):
        if x+1 == len(things) and len(things) > 2:
            msg += "and " + value + "!"
        elif len(things) > 2: msg += value + ", "
    return msg
