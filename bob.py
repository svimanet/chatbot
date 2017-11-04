from modules import irc_bob


iBob = irc_bob.I_Bob("Bob", "irc.server.com", "#test", 6697)

iBob.run()
