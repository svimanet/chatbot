from modules import blackjack
from modules import urban
import configparser as cp
import random
import socket
import json
import time
import ssl

class I_Bob(object):

	# Define bot
	def __init__(self, config):
		""" the bot construcotr. Requires bot name, server to connect to, servers port, and channel on server."""
		self.channel = config["DEFAULT"]["Channel"].lower()
		self.server = config["DEFAULT"]["Server"].lower()
		self.port = int(config["DEFAULT"]["Port"])
		self.name = config["DEFAULT"]["Nick"]

		# Modules anabled through config.
		self.modules = config["MODULES"]
		self.m_dictionary = self.modules["Dictionary"]
		self.m_blackjack = self.modules["BlackJack"]
		self.m_reminder = self.modules["Reminder"]
		self.m_urban = self.modules["Urban"]

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.server, self.port))
		self.ircsock = ssl.wrap_socket(self.s)


	# sends message to socket
	def send_socket(self, message):
		self.ircsock.send(message.encode("utf-8"))
		print(message)


	# Method for the bot to send a public message to the channel.
	def send_channel(self, message):
		self.send_socket("PRIVMSG {0} :{1}\r\n".format(self.channel, message))

	
	# Method for the bot to send a private message in IRC to a user.
	def send_priv(self, nick, message):
		self.send_socket("PRIVMSG {0} :{1}\n".format(nick, message))


	# if the server says PING, The bot will respond "PONG" + ping data.
	def ping_pong(self, data):
		if "PING" in data:
			pongData=data.split(":")[1]
			self.send_socket("PONG {0}\r\n".format(pongData))
			print(data)


	# Joins a channel after a ceretain ID id recieved, to ensure it doenst connect too soon.
	# This can fail if the server has specified anything but default.
	def join_channel(self, data):
		if "266" in data:
			self.send_socket("JOIN {0}\r\n".format(self.channel))

			
	# Method for the bot to sort between user messages and server messages.
	# msg = the whole thing that was said | message_start = first word in thing said.
	def parse_message(self, data):
		if "PRIVMSG" in data:
			one = data.split(":")[1]
			nick = one.split("!")[0].lower()
			msg = data.split(":")[2].lower()
			message_start = msg.split(" ")[0].lower()
			if_channel = str("PRIVMSG {}".format(self.channel))

			# Sends command list in priv msg
			if "!help" in message_start:
				self.send_priv(nick, "{} !play - Blackjack <1-6> players [p1: !play p2 p3 p4 p5 p6]".format(self.check_enable(self.m_blackjack)))
				self.send_priv(nick, "{} !urban - Search for a urban dictionary term [!urban <term>]".format(self.check_enable(self.m_urban)))
				self.send_priv(nick, "{} !define - Search for a dictionary term [!define <term>]".format(self.check_enable(self.m_dictionary)))
				self.send_priv(nick, "{} !remind - Set a reminder for x event. [!remind <'thing thing' 01.01.18]".format(self.check_enable(self.m_reminder)))

			# STart the BlackJack game if enabled.
			if "!play" in message_start and "True" in self.m_blackjack:
				message = msg.split("!play")[1].lower()
				if nick in message:
					self.send_channel(" # {0} dont inlcude your own name, you are automatically in the game if you start it. <p1>:!play <p2> <p3>".format(nick))
				else:
					blackjack.blackjack(self, nick, message)
			else:
				self.send_channel("BlackJack is Disabled.")

			# If user types "!urban x" activate urban on x.
			if "!urban" in message_start and "True" in self.m_urban:
				try:
					if len(msg.split(" "))>1:
						term = msg.split("!urban ")[1]
						term = term.replace(" ", "+")
						response = urban.urban(term)
						if if_channel in data:
							self.send_channel("{0}".format(response))
						else:
							self.send_priv(nick, "{0}".format(response))

				except Exception as e:
					if if_channel in data:
						self.send_channel("Something went wrong :(")
					else:
						self.send_priv("Something went wrong :(")
					print(e)

			# If user types "!define x" in chat, activate dictionary on x.
			if "!define" in message_start and "True" in self.m_dictionary:
				try:
					if len(msg.split(" "))>1:
						term = msg.split("!define ")[1]
						term = term.replace(" ", "-")
						response = str(urban.define(term))
						content = response.split("&+")[0]
						example = response.split("&+")[1]
						if if_channel in data:
							self.send_channel("{0}".format(content))
							self.send_channel("{0}".format(example))
						else:
							self.send_priv(nick, "{0}".format(content))
							self.send_priv(nick, "{0}".format(example))
					
				except Exception as e:
					if if_channel in data:
						self.send_channel("Something went wrong :(")
					else:
						self.send_priv("Something went wrong :(")
					print(e)


	# Just used to prettify command list.
	def check_enable(self, conf):
		if "True" in conf:
			return("[Enabled]")
		return("[Disabled]")


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
