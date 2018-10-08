# made by Svimanet, 09.2018.
import configparser as cp
from modules import urban
from modules import spellcheck
import discord
import os

# Starts the bot if token exists, creates token file and instructions if not.
def create_bot():
    token = "{}/token.txt".format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isfile(token):
        with open(token, "w+") as data_file:
            data_file.write("token")
            print("Token file created.\nPaste your token into the 'token' file.")
    else:
        token = open(token, "r").readline().strip()
        start_bot(str(token))


# Start the bot instance.
def start_bot(token):
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

        # More will come.
        if message.content.startswith('!help'):
            commands = ['!urban (!u) <term> - Self explanatory.',
                        '!ree (ree) - [UGC] rikkjen skrikje.',
                        '!check <sentence|word> - Corrects spelling (English).']
            msg = ""
            for x in range(len(commands)):
                msg += "{}\n".format(commands[x]) 
            await client.send_message(message.channel, msg)

        # As requested by konungen.
        elif message.content.lower().startswith('!ree') or message.content.lower().startswith('ree'):
            msg = 'REEEEEEEEEEEEEEEEEE\nhttps://clips.twitch.tv/BoringColdPelicanDerp'
            await client.send_message(message.channel, msg)

        # Lets user query urban dic through chat
        elif message.content.startswith("!urban"):
            term = message.content.split("!urban ")[1]
            if len(term.split())<25:
                msg = urban.urban(term)
                await client.send_message(message.channel, msg)

        # Another command for urban
        elif message.content.startswith("!u"):            
            term = message.content.split("!u ")[1]
            if len(term.split())<25:
                msg = urban.urban(term)
                await client.send_message(message.channel, msg)

        elif message.content.startswith("!check"):
            sentence = message.content.split("!check ")[1]
            check = spellcheck.check_spelling(sentence)
            msg = "{}: {}".format(message.author.mention, check)
            await client.send_message(message.channel, msg)

        # Simple responses when critiqued or commended
        elif message.content.startswith(client.user.mention):            
            if "good" in message.content:
                msg = "Thanks, {} <3".format(message.author.mention)
            elif "bad" in message.content:
                msg = "Sorry, {} :'(".format(message.author.mention)
            else:
                msg = "Beep Boop Suck my Philipshead, {}.".format(message.author.mention)
            await client.send_message(message.channel, msg)

        # Why not
        elif message.content.startswith("sup"):
            msg = "Nothing much, {}. Just writing some poetry.\nWhats crackalackin?".format(message.author.mention)
            await client.send_message(message.channel, msg) 


    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
    client.run(token)
create_bot()