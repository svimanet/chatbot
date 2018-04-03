from firebase import firebase
import requests

def create_reminder(nick, database, title, date, time):
	data = firebase.FirebaseApplication(database+nick, None)
	reminders = print_reminder(nick, database)
	num = len(reminders)
	result = data.put("{}/{}".format(nick, num), "title", title)
	result = data.put("{}/{}".format(nick, num), "date" , date)
	result = data.put("{}/{}".format(nick, num), "time", time)
	result = data.put("{}/{}".format(nick, num), "id", num)


def delete_reminder(nick, database, title):
	data = firebase.FirebaseApplication(database+nick, None)	
	reminders = print_reminder(nick, database)
	
	result = data.get(nick, None)
	for entry in result:
		if title in entry["title"]:
			data.delete("/{}.json".format(nick), entry["id"])
			print("deleted " + entry)




# DB is your own firebase real time database 
def print_reminder(nick, database):
	data = firebase.FirebaseApplication(database+nick, None)
	result = data.get(nick, None)
	reminders = []
	if result != None:
		for entry in result:
			title = entry["title"]
			date = entry["date"]
			time = entry["time"]
			num = entry["id"]
			reminder = "{} - {}: {} - {}".format(date, time, num, title)
			reminders.append(reminder)
		return reminders
	return reminders



db = "https://mydatabase.firebaseio.com/reminders/"
delete_reminder("svimanet", db, "test")
#create_reminder("test", db, "test", "01.02.03", "01:00")
#print(print_reminder("test", db))