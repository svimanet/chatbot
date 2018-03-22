from modules import irc_bob
import os

# Check if the config file exists or no
directory = os.path.dirname(os.path.realpath(__file__))
file = "{}/bob.config".format(directory)
if not os.path.isfile("bob.config"):
	data = input()
	with open(file, "w+") as data_file:
		data_file.write(data, encoding="UTF-8")
	print("wrote " + directory + "/bob.config")

info = open("{}/config".format(directory)).read().split(", ")
nick = info[0]
server = info[1]
channel = info[2]
iBob = irc_bob.I_Bob(nick, server, channel, 6697)

iBob.run()
