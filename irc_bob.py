import json
import socket
import ssl
import time
import random
import functions

class I_Bob(object):

	# Define bot
	def __init__(self, name, server, channel, port, oauth=None, type="IRC"):
		""" the bot construcotr. Requires bot name, server to connect to, servers port, and channel on server."""
		self.server = server
		self.port = port
		self.name = name
		self.channel = channel
		self.oauth = oauth
		self.type = type

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.server, self.port))
		self.ircsock = ssl.wrap_socket(self.s)

	# Method for the bot to send a public message to the channel.
	# Channel is either IRC channel or Twitch streamer channel, both work.
	def send_channel(self, message):
		""" Used to send messages in channels to avoid code duplication.""" 
		self.ircsock.send("PRIVMSG %s :%s\r\n" %(self.channel, message))
		print("PRIVMSG %s :%s\r\n" %(self.channel, message))
	
	# Method for the bot to send a private message in IRC to a user.
	# Currently not supported for Twitch chat, will fix one day.
	def send_priv(self, nick, message):
		if self.type == "Twitch":
			self.ircsock.send("PRIVMSG %s :/w %s %s\n" %(self.channel, nick, message))
			print("PRIVMSG %s :/w %s %s\n" %(self.channel, nick, message))
		else:
			self.ircsock.send("PRIVMSG %s :%s\n" %(nick, message))
			print("PRIVMSG %s :%s\r\n" %(nick, message))

	# if the server says PING, The bot will respond PONG + the relevant data.
	# Also works for Twich bot
	def ping_pong(self, data):
		""" Makes sure the bot returns a PONG and data if the server PINGS."""
		if "PING" in data:
			pongData=data.split(":")[1]
			self.ircsock.send("PONG "+pongData+"\r\n")
			print(data)
			print("PONG "+pongData+"\r\n")


	# Joins a channel after a ceretain ID id recieved, to ensure it doenst connect too soon.
	# Also works for twitch, but twitch server sends out another ID. 
	# ID's may differ according to servers, but standard for IRC is the 266 id. 
	# This can fail if the server has specified anything but default.
	def join_channel(self, data):
		if "266" in data and self.type == "IRC":
			print("JOIN %s\r\n" %self.channel)
			self.ircsock.send("JOIN %s\r\n" %self.channel)

		if "376" in data and self.type == "Twitch":
			print("JOIN %s\r\n" % self.channel)
			self.ircsock.send("JOIN %s\r\n" % self.channel)

			
	# Method for the bot to sort between user messages and server messages.
	# Here the bots reaction strings are speciefied
	# Also splits messages: nick = Who said a thing | 
	# msg = the whole thing that was said | message_start = first word in thing said.
	def parse_message(self, data):
		if "PRIVMSG" in data:

			one = data.split(":")[1]
			nick = one.split("!")[0].lower()
			msg = data.split(":")[2].lower()
			message_start = msg.split(" ")[0].lower()

			# Sends message in all chat if it's a twitch bot
			# Because the whisper function for twitch is broken atm (in the bot)
			if "!help" in message_start:
				if self.type == "Twitch":
					self.send_channel("#       List of commands")
					self.send_channel("# 'sup'   -  I will reply")
					self.send_channel("# p1 :'!play p2 p3 p4 p5 p6' - Blackjack <2-6> players")
					self.send_channel("# '!stop' -  Force quit blackjack")
					self.send_channel("# '!up'   -  Guess nigga")
				else:
					self.send_priv(nick, "#  %s the prodigy's list of commands.")
					self.send_priv(nick, "# 'sup' - I will reply")
					self.send_priv(nick, "# p1 :'!play p2 p3 p4 p5 p6' Blackjack <2-6> players")
					self.send_priv(nick, "# '!up' - Twitch only command.")

			if "sup" in message_start:
				self.send_channel("/me is beating the meat to a picture of %s's mother." %nick)

			if "!play" in message_start:

				self.send_channel("Fucking time for some blackjack and hookers.")
				message = msg.split("!play")[1].lower()
				if nick in message:
					self.send_channel(" # %s dont inlcude your own name, you are automatically in the game if you start it. <p1>:!play <p2> <p3>")
				else:
					functions.blackjack(self, nick, message)

			if "!up" in message_start:
				self.send_channel("Yes, I'm up :) Thank you for asking %s" %nick)
			
	# while loop #3. Because thats just how I roll.
	# see functions.py, This is where th bot awaits a player action
	def response(self, nick):
		while True:
			response = self.ircsock.recv(1024)
			self.ping_pong(response)
			if "PRIVMSG" in response:

				one = response.split(":")[1]
				nick2 = one.split("!")[0].lower()
				msg = response.split(":")[2]
				message_start = msg.split(" ")[0].lower()
				if nick.strip().lower() in nick2.strip():
					return msg
				elif "!stop" in message_start:
					return "stop"


	# Here the stuff happens.
	def run(self):
		navn = self.name

		if self.type == "IRC":
			self.ircsock.send("USER %s %s %s %s\r\n" % (navn, navn, navn, navn))
			self.ircsock.send("NICK %s\n" % navn)

		else:
			self.ircsock.send("PASS %s\n" % self.oauth)
			self.ircsock.send("NICK %s\n" % navn)

		while True:
			data = self.ircsock.recv(1024)
			print(data)

			self.join_channel(data)
			self.ping_pong(data)
			self.parse_message(data)