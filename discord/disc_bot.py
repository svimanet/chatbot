import configparser as cp
from modules import urban
import discord
import os


def create_bot():
    # Starts the bot if token exists, creates token file and instructions if not.
    token = "{}/token.txt".format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isfile(token):
        with open(token, "w+") as data_file:
            data_file.write("token")
            print("Token file created.\nPaste your token into the 'token' file.")
    else:
        token = open(token, "r").readline().strip()
        start_bot(str(token))


def start_bot(token):
    # Start the bot instance.
    client = discord.Client()
    @client.event
    async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        # Function actuators / Command keywords. 
        if message.content.startswith('!hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)

        # As requested by konungen.
        elif message.content.startswith('!ree') or message.content.startswith('ree'):
            msg = 'https://clips.twitch.tv/BoringColdPelicanDerp'
            await client.send_message(message.channel, msg)

        elif message.content.startswith("!urban"):
            term = message.content.split("!urban ")[1]
            if len(term.split())<25:
                msg = urban.urban(term)
                await client.send_message(message.channel, msg)

        elif message.content.startswith("!u"):            
            term = message.content.split("!u ")[1]
            if len(term.split())<25:
                msg = urban.urban(term)
                await client.send_message(message.channel, msg)

            

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
    client.run(token)
create_bot()