from modules import irc_bob
import os

# Check if the config file exists or no.
# If it doensn't exist, create on based on u.inp.
directory = os.path.dirname(os.path.realpath(__file__))
file = "{}/config.conf".format(directory)
if not os.path.isfile("config.conf"):
	print("Creating default config:")
	server = input("server  > ")
	channel = input("channel > ")
	data = "Bob {} {} 6697".format(server, channel)

	with open(file, "w+") as data_file:
		data_file.write(data)
		print("wrote " + file)

#iBob = irc_bob.I_Bob(nick, server, channel, 6697)
#iBob.run()
