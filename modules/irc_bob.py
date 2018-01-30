import json
import socket
import ssl
import time
import random
from modules import urban
from modules import blackjack

class I_Bob(object):

	# Define bot
	def __init__(self, name, server, channel, port):
		""" the bot construcotr. Requires bot name, server to connect to, servers port, and channel on server."""
		self.server = server
		self.port = port
		self.name = name
		self.channel = channel.strip()

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.server, self.port))
		self.ircsock = ssl.wrap_socket(self.s)

	# sends message to socket
	def send_socket(self, message):
		self.ircsock.send(message.encode("utf-8"))
		print(message)

	# Method for the bot to send a public message to the channel.
	# Channel is either IRC channel or Twitch streamer channel, both work.
	def send_channel(self, message):
		#Used to send messages in channels to avoid code duplication.
		self.send_socket("PRIVMSG {0} :{1}\r\n".format(self.channel, message))
	
	# Method for the bot to send a private message in IRC to a user.
	# Currently not supported for Twitch chat, will fix one day.
	def send_priv(self, nick, message):
		self.send_socket("PRIVMSG {0} :{1}\n".format(nick, message))

	# if the server says PING, The bot will respond PONG + the relevant data.
	# Also works for Twich bot
	def ping_pong(self, data):
		# Makes sure the bot returns a PONG and data if the server PINGS.
		if "PING" in data:
			pongData=data.split(":")[1]
			self.send_socket("PONG {0}\r\n".format(pongData))
			print(data)


	# Joins a channel after a ceretain ID id recieved, to ensure it doenst connect too soon.
	# Also works for twitch, but twitch server sends out another ID. 
	# ID's may differ according to servers, but standard for IRC is the 266 id. 
	# This can fail if the server has specified anything but default.
	def join_channel(self, data):
		if "266" in data:
			self.send_socket("JOIN {0}\r\n".format(self.channel))
			
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
			if_channel = str("PRIVMSG {}".format(self.channel))

			# Sends commadn list in priv msg
			if "!help" in message_start:				
				self.send_priv(nick, "# !play - Blackjack <1-6> players [p1: !play p2 p3 p4 p5 p6]")
				self.send_priv(nick, "# !urban - Search for a urban dictionary term [!urban <term>]")

			if "!play" in message_start:
				message = msg.split("!play")[1].lower()
				if nick in message:
					self.send_channel(" # {0} dont inlcude your own name, you are automatically in the game if you start it. <p1>:!play <p2> <p3>".format(nick))
				else:
					blackjack.blackjack(self, nick, message)

			if "!urban" in message_start:
				if len(msg.split(" "))>1:
					term = msg.split("!urban ")[1]
					term = term.replace(" ", "+")
					response = urban.urban(term)

					if if_channel in data:
						self.send_channel("{0}".format(response))
						self.send_channel("http://urbandictionary.com/define.php?term=%s" %term)
					else:
						self.send_priv(nick, "{0}".format(response))
						self.send_priv(nick, "http://urbandictionary.com/define.php?term=%s" %term)

				else:	
					response = urban.urban("foolish")
					if if_channel in data:
						self.send_channel("Foolish - {0}".format(response))
						self.send_channel("http://urbandictionary.com/define.php?term=foolish")
					else:
						self.send_priv(nick, "Foolish - {0}".format(response))
						self.send_priv(nick, "http://urbandictionary.com/define.php?term=foolish")
			

			if "!define" in message_start:
				if len(msg.split(" "))>1:
					term = msg.split("!define ")[1]
					term = term.replace(" ", "-")
					response = str(urban.define(term))
					content = response.split("&+")[0]
					example = response.split("&+")[1]
					if if_channel in data:
						self.send_channel("{0}".format(content))
						self.send_channel("{0}".format(example))
						self.send_channel("http://dictionary.com/browse/{}".format(term))
					else:
						self.send_priv(nick, "{0}".format(content))
						self.send_priv(nick, "{0}".format(example))
						self.send_priv(nick, "http://dictionary.com/browse/{}".format(term))
				else:
					if if_channel in data:
						send_channel("Did you forget something?")
					else:	
						send_priv(nick, "Did you forget something?")


	# while loop #3. Because thats just how I roll.
	# see functions.py, This is where th bot awaits a player action
	def response(self, nick):
		while True:
			response = self.ircsock.recv(1024).decode('utf-8')
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
		self.send_socket("USER {0} {0} {0} {0}\r\n".format(navn))
		self.send_socket("NICK {0}\n".format(navn))

		while True:
			data = self.ircsock.recv(1024).decode('utf-8')
			print(data)

			self.join_channel(data)
			self.ping_pong(data)
			self.parse_message(data)
