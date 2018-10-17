from modules import urban
import configparser as cp
import socket
import json
import time
import ssl
import os


""" Create / Retrieve config, connect to server, then start bot loop."""
def create_bot():
    # Check if config file exists. Create if not. 
    file = "{}/config.conf".format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isfile(file):
        print("Creating config...")
        nick = input("Nick > ")
        server = input("Server > ")
        channel = input("Channel > ")
        create_config(nick, server, channel, 6697)
        print("Done!")

    # Get config, set values
    config = get_config()
    nick = config["DEFAULT"]["Nick"]
    server = config["DEFAULT"]["Server"].strip().lower()
    channel = config["DEFAULT"]["Channel"].strip().lower()
    port = config["DEFAULT"]["Port"]

    # Connect to socket, run bot loop
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, int(port)))
    irc_sock = ssl.wrap_socket(sock)
    run(nick, server, channel, port, irc_sock)


""" Creates config file if none are present.
@param name - String name of chatbot.
@param server - String IRC server address.
@param channel - String IRC channel name on server.
@param port - int which port to use.
"""
def create_config(nick, server, channel, port=6667):
    file = "{}/config.conf".format(os.path.dirname(os.path.realpath(__file__)))
    config = cp.ConfigParser()
    config["DEFAULT"] = {
        "Nick":nick,
        "Server":server,
        "Channel":channel,
        "Port":port
    }
    with open(file, "w+") as data_file:
        config.write(data_file)
        print("Wrote config to {}.".format(file))


""" Retrieves config file
# @return config - content of config.conf
"""
def get_config():
    file = "{}/config.conf".format(os.path.dirname(os.path.realpath(__file__)))
    with open(file) as data_file:
        config = cp.ConfigParser()
        config.read_file(data_file)
        return config


""" Sends msg through sock
# @param irc_sock - socket used to communicate with irc-serv.
# @param msg - String message to send through socket.
"""
def send_sock(irc_sock, msg):
    irc_sock.send(msg.encode('utf-8'))
    print("socket_msg:", msg) 


""" Pings the Pong
Responds to server ping checks.
Double checks to avoid creating a list every loop.
@param data - raw data received through socket.
@param irc_sock - socket communication with server.
"""
def ping_pong(irc_sock, data):
    if "PING" in data:
        ping_data = data.split(":")
        if "PING" in ping_data[0]:
            send_sock(irc_sock, "PONG {0}\r\n".format(ping_data[1]))


""" Used to join a channel after connecting to a server.
@param data - Raw data from socket.
@param chan - String defining channel.
"""        
def join_chan(irc_sock, data, chan):
    if ("266" in data) and ("PRIVMSG" not in data):
        print("\n# TRYING TO JOIN #\n", data, "\n####\n")
        send_sock(irc_sock, "JOIN {0}\r\n".format(chan))


""" Sends message to channel or PM to user.
@param mode - int defining PM or CM.
@param chan - String defining Channel.
@param nick - String defining nick to respond.
@param msg - String defining message to send. 
"""
def send_msg(irc_sock, mode, channel, nick, msg):
    if mode == 1:    # 1 = Private Message
        send_sock(irc_sock, "PRIVMSG {0} :{1}\r\n".format(nick, msg))
    elif mode == 0:  # 0 = Channel Message
        send_sock(irc_sock, "PRIVMSG {0} :{1}\r\n".format(channel, msg))


""" Chat parsing and activations """
def parse_msg(irc_sock, data, channel):
    print("# parse_msg #\n", data, "\n###")
    if "PRIVMSG" in data:
        details = data.split(":")[1]
        nick = details.split("!")[0]
        message = data.split(":")[2].lower()
        if channel in details:  # Channel Message
            activate_features(irc_sock, channel, nick, message, 0)
        else:                   # Private Message
            activate_features(irc_sock, channel, nick, message, 1)


""" Function looking for keywords in messages, acting on said words
@param irc_sock - Socket for serv communication.
@param channel - Channel on server.
@param nick - Nick of the user activating.
@param msg - Message from user.
@param mode - Variable to distinguish between PM and CM.
"""
def activate_features(irc_sock, channel, nick, msg, mode):
    print("# activate_features #\n", msg, "\n###")
    if "!status" in msg:
        send_msg(irc_sock, mode, channel, nick, "{0}: alive I guess..".format(nick))
    elif "!urban" in msg:
        response = urban.urban(msg)
        send_msg(irc_sock, mode, channel, nick, response)
    

""" Main run loop 
@param nick - Bot nick/name.
@param server - Server to connect to.
@param channel - Channel to connect to.
@param port - Port to connect to.
@param irc_socket - Socket to communicate with.
"""
def run(nick, server, channel, port, irc_sock):
    send_sock(irc_sock, "USER {0} {0} {0} {0}\r\n".format(nick))
    send_sock(irc_sock, "NICK {0}\n".format(nick))
    running = True    
    while running:
        data = irc_sock.recv(1024).decode('utf-8')
        print(data)
        join_chan(irc_sock, data, channel)
        ping_pong(irc_sock, data)
        parse_msg(irc_sock, data, channel)
        
create_bot()