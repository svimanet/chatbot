# Import libs
import socket
import ssl
import os
import json

# Import modules
from modules import urban_dictionary
from modules import spelling
from modules import roll
from modules import jokes
from modules import quote_day
from modules import horoscope
from modules import name_day
from modules import random_cat
from modules import random_dog
from modules import meme_factory

class Bot:
    def __init__(self):
        self.irc_socket = False
        
        # Load config
        self.load_config()
        
        # Start bot
        self.server_connect()
        self.start_bot()
    
    def load_config(self):
        conf_dir = os.path.abspath(os.path.dirname(__file__))
        conf_fp = os.path.join(conf_dir, 'config.json')
        conf = {}
        try:
            if os.path.isfile(conf_fp):
                conf = json.load(open(conf_fp))
            else:
                default_fp = os.path.join(conf_dir, 'default_config.json')
                conf = json.load(open(default_fp))
                json.dump(conf, open(conf_fp, 'w+'), indent=2)
                print("Using default config. Edit config.json to change connection details")
        except Exception as e:
            print("Exiting program. Could not load config -> ", e)
            exit()
        for k, v in conf.items():
            setattr(self, k, v)
            
        

    def server_connect(self):
        """ Starts server connection to specified self.server. """
        #try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, int(self.port)))
        self.irc_socket = ssl.wrap_socket(sock)
        #except: # TODO find out which exception


    def sock_send(self, msg):
        """ Sends data through socket. Does not send socks. 
        :param msg: The String content to send through socket. """
        msg += '\r\n'  # New line counts as 'return/exec ..'
        self.irc_socket.send(msg.encode('utf-8'))
        print("socket_msg:", msg)


    def send_msg(self, msg, nick, pm):
        """ Sends a Private Message or a message to the channel its connected to.
        :param msg: String message to send.
        :param nick: nick of user that sent msg, and nick to respond if PM.
        :param pm: Boolean if its supposed to send privately. """
        if pm: self.irc_socket.send("PRIVMSG {0} :{1}\r\n".format(nick, msg).encode('utf-8'))
        else: self.irc_socket.send("PRIVMSG {0} :{1}\r\n".format(self.channel, msg).encode('utf-8'))


    def ping_pong(self, data):
        """ Responds PONG to server Pings. 
        :param data: raw socket data from server. """
        if "PRIVMSG" not in data and "PING" in data.split(':')[0]:
            self.sock_send("PONG {}".format(data.split(':')[1]))


    def join_channel(self, data):
        """ Joins a the specified server channel, under startup.
        :param data: Raw socket data from server. """
        if "PRIVMSG" not in data and "266" in data:
            if self.password: msg = "JOIN {} {}".format(self.channel, self.password)
            else: msg = "JOIN {}".format(self.channel)
            self.sock_send(msg)
            return True
        return False


    def check_errors(self, data):
        """ Checks for IRC errors, and one day it will handle it correctly.
        :param data: Raw socket data from server. """
        if "PRIVMSG" not in data and "ERR" in data:
            print("ERROR YALL")
            # TODO: Actual error handling


    def parse_msg(self, data):
        """ Parses messages to check for user messages, and handle them correctly.
        :param data: Raw socket data from server. """
        if "PRIVMSG" in data:
            details = data.split(":")[1]
            nick = details.split("!")[0]
            message = data.split(" :", 1)[1]

            if self.channel in details:  # Its not a PrivateMessage
                self.actuators(message, nick, False)
            else:                        # It is a PrivateMessage
                self.actuators(message, nick, True)


    def actuators(self, message, nick, pm):
        """ Actuators for modules and functions. Only activates on user messages.
        :param message: The user message recieved.
        :param nick: Nick of the user that sent the message.
        :param pm: Whether or not its a private message. """
        message = str(message)
        print(message)
        if "!" in message[0]:
            message_lower = message.lower()
            
            if "!hello" in message_lower:
                msg = "Hello there, {}!".format(nick)
                self.send_msg(msg, nick, pm)
        
            elif "!urban" in message_lower:
                result = urban_dictionary.urban_term(message)
                self.send_msg(result, nick, pm)
        
            elif "!check" in message_lower:
                result = spelling.check_spelling(message)
                self.send_msg(result, nick, pm)
            
            elif "!roll" in message_lower:
                result = roll.roll(message)
                self.send_msg(result, nick, pm)
                
            elif "!flip" in message_lower:
                result = roll.coin_flip()
                self.send_msg(result, nick, pm)

            elif "!joke" in message_lower:
                result = jokes.random_joke()
                self.send_msg(result, nick, pm)

            elif "!quote" in message_lower:
                result = quote_day.quote_of_the_day()
                self.send_msg(result, nick, pm)

            elif "!nameday" in message_lower:
                result = name_day.todays_names()
                self.send_msg(result, nick, pm)

            elif "!chucknorris" in message_lower:
                result = jokes.random_chuck_joke()
                self.send_msg(result, nick, pm)

            elif "!meow" in message_lower:
                result = random_cat.random_cat_pic()
                self.send_msg(result, nick, pm)

            elif "!horoscope" in message_lower:
                try:
                    zodiac = message.split(' ', 1)[1].split('\r\n')[0]
                    result = horoscope.get_horoscope(zodiac)
                    self.send_msg(result, nick, pm)
                except IndexError:
                    self.send_msg('Did you forget the zodiac sign?', nick, pm)
            elif "!dog" in message_lower:
                result = random_dog.random_dog_pic()
                self.send_msg(result, nick, pm)
            elif message_lower.startswith('!meme'):
                meme = meme_factory.meme(message)
                self.send_msg(meme, nick, pm)



    def start_bot(self):
        """ Starts the bot and connects to channel. Then goes into actuator mode. """
        self.sock_send("USER {0} {1} {1} {2}".format(self.nick, self.hostname, self.name))
        print("USER {0} {1} {1} {2}".format(self.nick, self.hostname, self.name))
        self.sock_send("NICK {}".format(self.nick))
        joined = False
        starting = True
        while starting:
            data = self.irc_socket.recv(1024).decode('utf-8')
            print("Startup Recv = ", data)
            self.ping_pong(data)
            joined = self.join_channel(data)
            if joined: starting = False

        print("#############\nStartup success\n#############")
        self.run()


    def run(self):
        """ Keeps the bot running after startup and channel join. """
        running = True
        while running:
            data = self.irc_socket.recv(1024).decode('utf-8')
            print("Recv = ", data)
            self.ping_pong(data)
            self.check_errors(data)
            self.parse_msg(data)
            

# Instansiate
bob = Bot()
