from modules import irc_bob
import os

directory = os.path.dirname(os.path.realpath(__file__))
info = open("{}/config".format(directory)).read().split(", ")
nick = info[0]
server = info[1]
channel = info[2]
iBob = irc_bob.I_Bob(nick, server, channel, 6697)

iBob.run()
