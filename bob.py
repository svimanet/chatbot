from irc_bob import I_Bob

# fill in the capitalized params. #
# tBob = Twitch
# iBob = IRC
tBob = I_Bob("BOTS TWITCH NICK", "irc.chat.twitch.tv", "#NICK OF STREAMER", 6697, "oauth:BIG ASS TOKEN", "Twitch")
iBob = I_Bob("Bob", "IRC.SERVER.ORG", "#CHANNEL", 6697)

# Run it
iBob.run()
