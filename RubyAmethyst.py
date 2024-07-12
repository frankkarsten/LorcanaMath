#===We do the calculations via five million simulations, using random number generators
#===For more complicated situations, this is far easier and less error-prone to code
import random

def choose_ink_and_adjust_hand(hand, turn):
	#We take a hand and, according to a step-by-step logic, pick a card to ink
	#Returns true if we indeed chose a card for ink, and False in the rare case where we can't
	if hand['Inkable Other'] >= 1:
		hand['Inkable Other'] -= 1
		return True
	if hand['Mim Snake'] >= 1:
		hand['Mim Snake'] -= 1
		return True
	if hand ['Friends on the Other Side'] >= 2:
		hand['Friends on the Other Side'] -= 1
		return True
	if hand ['Chernabog Followers'] >= 2:
		hand['Chernabog Followers'] -= 1
		return True
	if hand['Castle'] >= 2:
		hand['Castle'] -= 1
		return True
	if hand['Sisu'] >= 2:
		hand['Sisu'] -= 1
		return True
	if hand['Flynn Rider'] >= 2:
		hand['Flynn Rider'] -= 1
		return True
	if hand['Flynn Rider'] >= 1 and turn > 2:
		hand['Flynn Rider'] -= 1
		return True
	if hand['Sisu'] >= 1 and turn > 3:
		hand['Sisu'] -= 1
		return True
	if hand['Friends on the Other Side'] >= 1:
		hand['Friends on the Other Side'] -= 1
		return True
	if hand['Chernabog Followers'] >= 1:
		hand['Chernabog Followers'] -= 1
		return True	
	if hand['Castle'] >= 1:
		hand['Castle'] -= 1
		return True	
	return False


def run_one_sim(play_or_draw):	
	#Construct library as a list
	library = []
	for card in decklist.keys():
		library += [card] * decklist[card]
	random.shuffle(library)

	#Construct a random opening hand
	hand = {
		'Chernabog Followers': 0,
		'Flynn Rider': 0,
		'Mim Snake': 0,
		'Sisu': 0,
		'Castle': 0,
		'Friends on the Other Side': 0,
		'Inkable Other': 0,
		'Uninkable Other': 0
	}
	for _ in range(7):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1

	#Adjust the hand by figuring out what to put on the bottom
	#Mulligan strategy: first figure out if our hand is already perfect (save potentially for having enough ink)
	WeAlreadyHaveCardNuts = True if hand['Flynn Rider'] >= 1 and hand['Sisu'] >= 1 and hand['Castle'] >= 1 else False
	#1. We keep one Chernabog Followers if possible and mulligan excess copies.
	Chernabog_on_bottom = 0 if hand['Chernabog Followers'] == 0 else (hand['Chernabog Followers'] - 1 if not WeAlreadyHaveCardNuts else 0)
	#2. We keep one Flynn if possible and mulligan excess copies.
	Flynn_on_bottom = 0 if hand['Flynn Rider'] == 0 else (hand['Flynn Rider'] - 1 if not WeAlreadyHaveCardNuts else 0)
	#3. If there is no Flynn but we did have Chernabog Followers, we try to secure a two-drop effect by keeping Mim Snake if possible
	if WeAlreadyHaveCardNuts:
		MimSnake_on_bottom = 0
	elif hand['Flynn Rider'] == 0 and hand['Chernabog Followers'] >= 1:
		MimSnake_on_bottom = 0 if hand['Mim Snake'] == 0 else hand['Mim Snake'] - 1
	else:
		MimSnake_on_bottom = hand['Mim Snake']
	#4. We keep one Sisu if possible and mulligan excess copies
	Sisu_on_bottom = 0 if hand['Sisu'] == 0  else (hand['Sisu'] - 1 if not WeAlreadyHaveCardNuts else 0)
	#5. We keep one Castle if possible and mulligan excess copies
	Castle_on_bottom = 0 if hand['Castle'] == 0  else (hand['Castle'] - 1 if not WeAlreadyHaveCardNuts else 0)
	#6. If we already have Flynn and Sisu, we keep one Friends on the Other Side
	if WeAlreadyHaveCardNuts:
		Friends_on_bottom = 0
	elif hand['Flynn Rider'] >= 1 and hand['Sisu'] >= 1:
		Friends_on_bottom = 0 if hand['Friends on the Other Side'] == 0 else hand['Friends on the Other Side'] - 1
	else:
		Friends_on_bottom = hand['Friends on the Other Side']
	#7. If we already have all cards for the nuts, we keep all ink if possible. Otherwise, we mulligan them all in search of key cards.
	InkableOther_on_bottom = hand['Inkable Other'] if not WeAlreadyHaveCardNuts else 0
	UninkableOther_on_bottom = hand['Uninkable Other']
	hand['Chernabog Followers'] -= Chernabog_on_bottom
	hand['Flynn Rider'] -= Flynn_on_bottom
	hand['Mim Snake'] -= MimSnake_on_bottom
	hand['Sisu'] -= Sisu_on_bottom
	hand['Castle'] -= Castle_on_bottom
	hand['Friends on the Other Side'] -= Friends_on_bottom
	hand['Inkable Other'] -= InkableOther_on_bottom
	hand['Uninkable Other'] -= UninkableOther_on_bottom

	library += ['Chernabog Followers'] * Chernabog_on_bottom + ['Flynn Rider'] * Flynn_on_bottom + ['Mim Snake'] * MimSnake_on_bottom + ['Sisu'] * Sisu_on_bottom
	library += ['Castle'] * Castle_on_bottom + ['Friends on the Other Side'] * Friends_on_bottom + ['Inkable Other'] * InkableOther_on_bottom + ['Uninkable Other'] * UninkableOther_on_bottom 
	
	nr_cards_adjusted = Chernabog_on_bottom + Flynn_on_bottom + MimSnake_on_bottom + Sisu_on_bottom + Castle_on_bottom + Friends_on_bottom + InkableOther_on_bottom + UninkableOther_on_bottom
	for _ in range(nr_cards_adjusted):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
	random.shuffle(library)
	
	#Draw potential card for turn 1
	if play_or_draw == "draw":
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
		
	#Make a play on turn one
	InkTurnOne = choose_ink_and_adjust_hand(hand, 1)
	Followers_on_turn_one = hand['Chernabog Followers'] >= 1
	if Followers_on_turn_one:
		hand['Chernabog Followers'] -= 1
		#We'll skip ahead to next turn, where we'll use it to draw a card
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
	
	#Draw card for turn 2
	card_drawn = library.pop(0)
	hand[card_drawn] += 1
	
	#Potentially play Flynn
	InkTurnTwo = choose_ink_and_adjust_hand(hand, 2)
	Flynn_on_turn_two = hand['Flynn Rider'] >= 1
	if Flynn_on_turn_two:
		hand['Flynn Rider'] -= 1

	#Draw card for turn 3
	card_drawn = library.pop(0)
	hand[card_drawn] += 1

	#Potentially play Sisu
	InkTurnThree = choose_ink_and_adjust_hand(hand, 3)
	Sisu_on_turn_three = hand['Sisu'] >= 1
	if Sisu_on_turn_three:
		hand['Sisu'] -= 1

	#Draw card for turn 4
	card_drawn = library.pop(0)
	hand[card_drawn] += 1

	#Potentially play Friends on the Other Side
	if Sisu_on_turn_three and hand['Friends on the Other Side'] >= 1 and not hand['Castle'] >= 1:
		hand['Friends on the Other Side'] -= 1
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
		card_drawn = library.pop(0)
		hand[card_drawn] += 1

	#Potentially play Castle
	InkTurnFour = choose_ink_and_adjust_hand(hand, 4)
	Castle_on_turn_four = hand['Castle'] >= 1

	#Check if we have everything
	EnoughInkTurnThree = InkTurnOne and InkTurnTwo and InkTurnThree
	EnoughInkTurnFour = InkTurnOne and InkTurnTwo and InkTurnThree and InkTurnFour
	FlynnSisu = Flynn_on_turn_two and Sisu_on_turn_three
	Nuts = Flynn_on_turn_two and Sisu_on_turn_three and Castle_on_turn_four
	return [EnoughInkTurnThree and FlynnSisu, EnoughInkTurnFour and Nuts, Nuts and not EnoughInkTurnFour, nr_cards_adjusted]

num_simulations = 5000000

decklist = {
	'Chernabog Followers': 4,
	'Flynn Rider': 4,
	'Mim Snake': 4,
	'Sisu': 4,
	'Castle': 4,
	'Friends on the Other Side': 4,
	'Inkable Other': 20,
	'Uninkable Other': 16
}

nr_cards_adjusted = 0

for play_draw in ["play", "draw"]:
	succesful_games_nuts = 0
	succesful_games_FlynnSisu = 0
	games_ink_failure = 0
	for _ in range(num_simulations):
		[FlynnSisu_result, nuts_result, ink_failure_result, cards_result] = run_one_sim(play_draw)
		succesful_games_nuts += nuts_result
		succesful_games_FlynnSisu += FlynnSisu_result
		games_ink_failure += ink_failure_result
		nr_cards_adjusted += cards_result

	print(f"Simulated nuts probability on the {play_draw} ={succesful_games_nuts/num_simulations * 100: .1f}%")
	print(f"Simulated FlynnSisu probability on the {play_draw} ={succesful_games_FlynnSisu/num_simulations * 100: .1f}%")
	print(f"Probability of not having enough ink for nuts on the {play_draw} ={games_ink_failure/succesful_games_nuts * 100: .3f}%")
	
print("----")
print(f"Expected cards adjusted ={nr_cards_adjusted/(num_simulations * 2) : .2f}")
	
	