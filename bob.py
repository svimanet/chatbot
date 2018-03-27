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
		"Nick":"Bob",
		"Server":server,
		"Channel":channel,
		"Port":6697
	}

	config["MODULES"] = {
		"BlackJack":False,
		"Urban":True,
		"Dictionary":True,
		"Reminder":False
	}

	# Save config with default data.
	with open(file, "w+") as data_file:
		config.write(data_file)
		print("wrote " + file)

# Run Bob, run!
file_data = open(file).read()
config = cp.ConfigParser()
config.read(file)
bob = irc_bob.I_Bob(config)
bob.run()