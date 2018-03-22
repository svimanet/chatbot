from modules import irc_bob
import configparser as cp
import os

# Check if the config file exists or no.
# If it doensn't exist, create on based on u.inp.
directory = os.path.dirname(os.path.realpath(__file__))
file = "{}/config.conf".format(directory)
if not os.path.isfile("config.conf"):
	print("Creating default config:")
	server = input("server  > ")
	channel = input("channel > ")
	data = "Bob {} {} {}".format(server, channel, 6697)

	config = cp.ConfigParser()
	config["DEFAULT"] = {
		"NICK":"Bob",
		"SERVER":server,
		"CHANNEL":channel,
		"PORT":6697
	}

	config["MODULES"] = {
		"BLACKJACK":False,
		"URBAN":True,
		"DICTIONARY":True
	}

	# Save config with default data.
	with open(file, "w+") as data_file:
		config.write(data_file)
		print("wrote " + file)

# Run Bob, run!
file_data = open(file).read()
config = cp.ConfigParser()
config.read(file)
data = config["DEFAULT"]
port = int(data["PORT"])
chan = data["CHANNEL"]
serv = data["SERVER"]
nick = data["NICK"]

print("Running {}.".format(nick))
bob = irc_bob.I_Bob(nick, serv, chan, port)
bob.run()