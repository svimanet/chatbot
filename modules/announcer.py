import json
import os

def set_event(message, time, game, host, authorized):
    event = {}
    event["msg"] = message
    event["time"] = time
    event["game"] = game
    event["host"] = host
    json_event = json.dumps(event)

    events_file = "{}/events.json".format(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isfile(events_file):
        with open(events_file, "r") as data_file:
                events = json.load(data_file)
        print(events)
    else:
        with open(events_file, "w+") as data_file:
            data_file.write(json_event)
            print("Made events file")

def announce(message, time, game, user, authorized):
    if authorized:
        msg = ["Attention @everyone! {} has announced a game of {}!".format(user, game),
                '"{}"'.format(message),
                "{} | {}".format(game, time)]
        for x in range(len(msg)):
            print(msg[x])


#announce("Det vart spill med golf it i kveld håper alle kan komme eksde", "19:20", "Golf It", "Rikkjen", True)
set_event("msg", "19:30", "Golf It", "Svimanet", True)