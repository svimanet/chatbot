import json
import os

def create_reminder(nick, reminder):
	data = reminder.split(" ")
	if data[0]:

	directory = os.path.dirname(os.path.realpath(__file__))
	file = directory + "/reminders.json"
	if not os.path.isfile(file):
		with open(file, "w+") as data_file:
			data_file.write(data)


def get_reminders():
	print("reminders yall!")


create_reminder("sender", "22.03 ")