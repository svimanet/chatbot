import sys
import random

# ############################################################ #
# A method that lets 2-6 players in the chat play blackjack.   #
# ############################################################ #
# Works but needs a few tweaks. Mainly letting the bot draw    #
# if he has less than 16 points, insta blackjack on player 21  #
# and letting the A be either 1 or 11, currently just 11.      #
# ############################################################ #

# Will comment in details once im done because #lazy #plzHireMe #normallyIcomment #promisePlzBoss
def blackjack(bob, nick, messages):
	players=[]
	msg = nick + messages
	message = msg.rstrip().lstrip()
	number = len(message.split(" "))

	""" Checks if more than one player, makes list of players"""
	if number > 1 and number <= 6:
		for x in range(len(message.split(" "))):

			players.append([message.split(" ")[x]])

		number_players = len(players)
		cards = make_deck()

		card_decks = {}
		bot_cards = []
		bot_cards.append(cards.pop())
		bot_cards.append(cards.pop())
		bot_cards_print = (" # My cards: x and %s" %bot_cards[0])
		"""print(bot_cards_print)"""
		bob.send_channel(bot_cards_print)

		for x in range(number_players):
			card1 = cards.pop()
			card2 = cards.pop()
			player = str(players[x]).split("'")[1]
			card_decks[x] = card1, card2

			cards_dealt = " # %s's cards: %s, %s" %(player.split("\\")[0], card1, card2)
			"""print(cards_dealt)"""
			bob.send_channel(cards_dealt)
			""" CARDS DEALT """

		""" WHO BEGINS """
		rand_player = random.randrange(len(players))
		playing = True
		turns = 0

		while playing:
			player_turn = players[rand_player]
			hit(bob, player_turn, rand_player, card_decks, cards, players)
			rand_player = next_player(rand_player, players)
			turns += 1

			if turns == len(players):
				playing = False

		round_it_up(str(bot_cards[0]), str(bot_cards[1]), players, card_decks, bob)

	else:
		error=" # 2-6 players please. <p1>:!play <p2> <p3> <p4> <p5> <p6>"
		bob.send_channel(error)


def round_it_up(bot1, bot2, players, card_decks, bob):
	card1 = check_picture(bot1.split(" ")[0])
	card2 = check_picture(bot2.split(" ")[0])
	total = card1 + card2

	bot_score = " # My cards: %s and %s. Totaling %s." %(card1, card2, total)
	bob.send_channel(bot_score)

	for x in range(len(players)):

		player = str(players[x]).split("'")[1]
		if "\\" in player:
			player = player.split("\\")[0]

		points = count_points(card_decks, x)

		lost = " # LOSS! %s lost with %s points." % (player, str(points))
		won = " # WIN! %s beat me with %s points." % (player, str(points))

		if points > total and points<=21:
			"""print won"""
			bob.send_channel(won)
		else:
			"""print lost"""
			bob.send_channel(lost)

def count_points(card_decks, player):
	cards = len(card_decks[player])
	points = 0
	d = {"A":11, "K":10, "Q":10, "J":10}
	for x in range(cards):

		card_obj = card_decks[player][x]
		print " ______ "
		print card_obj
		card_string = card_obj.split(" ")[0]
		card = d.get(card_string, None)
		if not card:
			card = int(card_string)

		points += card
	return points

def check_bust(points):
	if points > 21:
		return True
	else:
		return False


def check_21(points):
	if points == 21:
		return True
	else:
		return False


def check_picture(card):
	if "K" in card or "Q" in card or "J" in card:
		return 10

	elif "A" in card:
		return 11

	else:
		return int(card)
	
def next_player(prev_player, players):
	if prev_player == len(players)-1:
		return 0
	else:
		return prev_player + 1


def hit(bob, player_turn, rand_player, card_decks, cards, players):

	player = str(player_turn).split("'")[1]
	if "\\" in player:
		player = player.split("\\")[0]

	action_q = " # !hit or !stand, %s?" %player
	bob.send_channel(action_q)
	action = bob.response(player).lower()

	if "stop" in action:
		return false

	if "stand" in action:
		stand = True
		standing = " # %s is standing."%player
		"""print standing"""
		bob.send_channel(standing)

	elif "hit" in action:
		new_card = cards.pop()
		prev_cards = str(card_decks[rand_player])
		card1 = prev_cards.split("'")[1]
		card2 = prev_cards.split("'")[3]

		if len(prev_cards.split("'"))==7:
			card3 = prev_cards.split("'")[5]

			card_decks[rand_player] = card1, card2, card3, new_card
			gave_card = " # Gave %s a %s. => %s, %s, %s, %s" % (player, new_card, card1, card2, card3, new_card)
			"""print gave_card"""
			bob.send_channel(gave_card)
			after_draw(card_decks, player_turn, players, player, rand_player, cards, bob)

		elif len(prev_cards.split("'"))==9:
			card3 = prev_cards.split("'")[5]
			card4 = prev_cards.split("'")[7]

			card_decks[rand_player] = card1, card2, card3, card4, new_card
			gave_card = " # Gave %s a %s. => %s, %s, %s, %s, %s" % (player, new_card, card1, card2, card3, card4, new_card)
			"""print gave_card"""
			bob.send_channel(gave_card)
			after_draw(card_decks, player_turn, players, player, rand_player, cards, bob)

		elif len(prev_cards.split("'"))==11:
			card3 = prev_cards.split("'")[5]
			card4 = prev_cards.split("'")[7]
			card5 = prev_cards.split("'")[9]

			card_decks[rand_player] = card1, card2, card3, card4, card5, new_card
			gave_card = " # Gave %s a %s. => %s, %s, %s, %s, %s, %s " % (player, new_card, card1, card2, card3, card4, card5, new_card)
			"""print gave_card"""
			bob.send_channel(gave_card)
			after_draw(card_decks, player_turn, players, player, rand_player, cards, bob)

		elif len(prev_cards.split("'"))>11:
			gave_card = " # Maker was to lazy, so you cant draw more cards, sry not sry."
			"""print gave_card"""
			bob.send_channel(gave_card)
			after_draw(card_decks, player_turn, players, player, rand_player, cards, bob)

		else:
			card_decks[rand_player] = card1, card2, new_card
			gave_card = " # Gave %s a %s. => %s, %s, %s" % (player, new_card, card1, card2, new_card)
			"""print gave_card"""
			bob.send_channel(gave_card)
			after_draw(card_decks, player_turn, players, player, rand_player, cards, bob)

	else:
		valid_command=(" # Not a valid command")
		"""print  valid_command"""
		bob.send_channel(valid_command)
		hit(bob, player_turn, rand_player, card_decks, cards, players)

def after_draw(card_decks, player_turn, players, player, rand_player, cards, bob):
	if "\\" in player:
		player = player.split("\\")[0]
	points = count_points(card_decks, rand_player)
	bust = check_bust(points)
	twenty_one = check_21(points)

	if bust:
		busting_nut = " # Bust! R.I.P %s with %s points." % (player, points)
		"""print busting_nut"""
		bob.send_channel(busting_nut)

	elif twenty_one:
		winning = " # 21! %s got 21 points." % player
		"""print winning"""
		bob.send_channel(winning)

	else:
		hit(bob, player_turn, rand_player, card_decks, cards, players)



def make_deck():
	ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
	suite = ['clubs', 'hearts', 'spades', 'diamonds']

	deck = [r + ' ' + s for r in ranks for s in suite]

	random.shuffle(deck)
	return  deck