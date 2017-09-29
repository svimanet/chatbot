import json
import socket
import ssl
import time
import urban
import random
import functions

class I_Bob(object):

	# Define bot
	def __init__(self, name, server, channel, port):
		""" the bot construcotr. Requires bot name, server to connect to, servers port, and channel on server."""
		self.server = server
		self.port = port
		self.name = name
		self.channel = channel

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.server, self.port))
		self.ircsock = ssl.wrap_socket(self.s)


	# Method for the bot to send a public message to the channel.
	# Channel is either IRC channel or Twitch streamer channel, both work.
	def send_channel(self, message):
		#Used to send messages in channels to avoid code duplication.
		self.ircsock.send("PRIVMSG %s :%s\r\n" %(self.channel, message))
		print("PRIVMSG %s :%s\r\n" %(self.channel, message))

	
	# Method for the bot to send a private message in IRC to a user.
	# Currently not supported for Twitch chat, will fix one day.
	def send_priv(self, nick, message):
		self.ircsock.send("PRIVMSG %s :%s\n" %(nick, message))
		print("PRIVMSG %s :%s\r\n" %(nick, message))


	# if the server says PING, The bot will respond PONG + the relevant data.
	# Also works for Twich bot
	def ping_pong(self, data):
		# Makes sure the bot returns a PONG and data if the server PINGS.
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
		if "266" in data:
			print("JOIN %s\r\n" %self.channel)
			self.ircsock.send("JOIN %s\r\n" %self.channel)

			
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

			# Sends commadn list in priv msg
			if "!help" in message_start:				
				self.send_priv(nick, "# !play - Blackjack <1-6> players [p1: !play p2 p3 p4 p5 p6]")
				self.send_priv(nick, "# !urban - Search for a urban dictionary term [!urban <term>]")

			if "!play" in message_start:
				message = msg.split("!play")[1].lower()
				if nick in message:
					self.send_channel(" # %s dont inlcude your own name, you are automatically in the game if you start it. <p1>:!play <p2> <p3>")
				else:
					functions.blackjack(self, nick, message)

			if "!urban" in message_start:
				if len(msg.split(" "))>1:
					term = msg.split("n ")[1]
					term = term.replace(" ", "+")
					response = urban.urban(term)
					self.send_channel("%s" %response)
					self.send_channel("http://urbandictionary.com/define.php?term=%s" %term)
				else:
					response = urban.urban("foolish")
					self.send_channel("%s" %response)
					self.send_channel("http://urbandictionary.com/define.php?term=%s" %term)
			

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
		self.ircsock.send("USER %s %s %s %s\r\n" % (navn, navn, navn, navn))
		self.ircsock.send("NICK %s\n" % navn)

		while True:
			data = self.ircsock.recv(1024)
			print(data)

			self.join_channel(data)
			self.ping_pong(data)
			self.parse_message(data)