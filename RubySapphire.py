#===We do the calculations via five million simulations, using random number generators
#===For more complicated situations, this is far easier and less error-prone to code
import random

def choose_ink_and_adjust_hand(hand, turn):
	#We take a hand and, according to a step-by-step logic, pick a card to ink
	#Returns true if we indeed chose a card for ink, and False in the rare case where we can't
	if hand['Inkable Other'] >= 1:
		hand['Inkable Other'] -= 1
		return True
	if hand['Hiram'] >= 2:
		hand['Hiram'] -= 1
		return True
	if hand['Pawpsicle'] >= 2:
		hand['Pawpsicle'] -= 1
		return True
	if hand['Fishbone Quill'] >= 1:
		hand['Fishbone Quill'] -= 1
		return True
	if hand['Pawpsicle'] == 1 and turn > 1:
		hand['Pawpsicle'] -= 1
		return True
	if hand ['Vitalisphere'] >= 1 and turn > 1:
		hand['Vitalisphere'] -= 1
		return True
	if hand['Hiram'] == 1:
		hand['Hiram'] -= 1
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
		'Pawpsicle': 0,
		'Ice Block': 0,
		'Vitalisphere': 0,
		'One Jump Ahead': 0,
		'Fishbone Quill': 0,
		'Hiram': 0,
		'Inkable Other': 0,
		'Uninkable Other': 0
	}
	for _ in range(7):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1

	#Adjust the hand by figuring out what to put on the bottom
	#Mulligan strategy: first figure out if our hand is already perfect (save potentially for having enough ink)
	WeAlreadyHaveCardNuts = True if hand['Pawpsicle'] >= 1 and hand['One Jump Ahead'] >= 1 and hand['Hiram'] >= 1 else False
	#1. We keep one Pawpsicle if possible and mulligan excess copies.
	Pawpsicle_on_bottom = 0 if hand['Pawpsicle'] == 0 else (hand['Pawpsicle'] - 1 if not WeAlreadyHaveCardNuts else 0)
	#2. If there was no Pawpsicle, we keep an Ice Block, otherwise a Vitalisphere if possible
	IceBlock_on_bottom = hand['Ice Block'] if hand['Pawpsicle'] >= 1 else max(0, hand['Ice Block'] - 1)
	Vitalisphere_on_bottom = hand['Vitalisphere'] if hand['Pawpsicle'] + hand['Ice Block'] >= 1 else max(0, hand['Vitalisphere'] - 1)
	#3. We keep one One Jump Ahead if possible and mulligan excess copies
	Jump_on_bottom = 0 if hand['One Jump Ahead'] == 0 else hand['One Jump Ahead'] - 1
	#4. If there was no One Jump Ahead, we try to secure a ramp effect by keeping Fishbone Quill if possible
	Quill_on_bottom = hand['Fishbone Quill'] if hand['One Jump Ahead'] >= 1 else max(0, hand['Fishbone Quill'] - 1)
	#5. We keep one Hiramo if possible and mulligan excess copies
	Hiram_on_bottom = 0 if hand['Hiram'] == 0 else (hand['Hiram'] - 1 if not WeAlreadyHaveCardNuts else 0)
	#6. If we already have all cards for the nuts, we keep all ink if possible. Otherwise, we mulligan them all in search of characters.
	InkableOther_on_bottom = hand['Inkable Other'] if not WeAlreadyHaveCardNuts else 0
	UninkableOther_on_bottom = hand['Uninkable Other']
	hand['Pawpsicle'] -= Pawpsicle_on_bottom
	hand['Ice Block'] -= IceBlock_on_bottom
	hand['Vitalisphere'] -= Vitalisphere_on_bottom
	hand['One Jump Ahead'] -= Jump_on_bottom
	hand['Fishbone Quill'] -= Quill_on_bottom
	hand['Hiram'] -= Hiram_on_bottom
	hand['Inkable Other'] -= InkableOther_on_bottom
	hand['Uninkable Other'] -= UninkableOther_on_bottom

	library += ['Pawpsicle'] * Pawpsicle_on_bottom + ['Ice Block'] * IceBlock_on_bottom + ['Vitalisphere'] * Vitalisphere_on_bottom + ['One Jump Ahead'] * Jump_on_bottom
	library += ['Fishbone Quill'] * Quill_on_bottom + ['Hiram'] * Hiram_on_bottom + ['Inkable Other'] * InkableOther_on_bottom + ['Uninkable Other'] * UninkableOther_on_bottom 
	
	nr_cards_adjusted = Pawpsicle_on_bottom + IceBlock_on_bottom + Vitalisphere_on_bottom + Jump_on_bottom + Quill_on_bottom + Hiram_on_bottom + InkableOther_on_bottom + UninkableOther_on_bottom
	for _ in range(nr_cards_adjusted):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
	random.shuffle(library)
	
	#Draw potential card for turn 1
	if play_or_draw == "draw":
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
		
	#Check if we have an item on turn one
	InkThisTurn = choose_ink_and_adjust_hand(hand, 1)
	Pawpsicle_on_turn_one = hand['Pawpsicle'] >= 1 and InkThisTurn
	Other_item_on_turn_one = hand['Ice Block'] + hand['Vitalisphere'] >= 1 and InkThisTurn and not Pawpsicle_on_turn_one
	if Pawpsicle_on_turn_one:
		hand['Pawpsicle'] -= 1
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
	elif Other_item_on_turn_one:
		if hand['Ice Block'] >= 1:
			hand['Ice Block'] -= 1
		elif hand['Vitalisphere'] >= 1:
			hand['Vitalisphere'] -= 1
	
	#Draw card for turn 2
	card_drawn = library.pop(0)
	hand[card_drawn] += 1
	
	#Potentially play One Jump Ahead
	InkThisTurn = choose_ink_and_adjust_hand(hand, 2)
	Jump_on_turn_two = hand['One Jump Ahead'] >= 1 and InkThisTurn
	if Jump_on_turn_two:
		hand['One Jump Ahead'] -= 1
		library.pop(0)
	
	#Draw card for turn 3
	card_drawn = library.pop(0)
	hand[card_drawn] += 1

	#Potentially play Hiram
	InkThisTurn = choose_ink_and_adjust_hand(hand, 3)
	Hiram_on_turn_three = hand['Hiram'] >= 1 and InkThisTurn

	#Check if we have everything
	
	return [Pawpsicle_on_turn_one and Jump_on_turn_two and Hiram_on_turn_three, (Pawpsicle_on_turn_one or Other_item_on_turn_one) and Jump_on_turn_two and Hiram_on_turn_three, nr_cards_adjusted]

num_simulations = 5000000

decklist = {
	'Pawpsicle': 4,
	'Ice Block': 2,
	'Vitalisphere': 2,
	'One Jump Ahead': 4,
	'Fishbone Quill': 4,
	'Hiram': 4,
	'Inkable Other': 23,
	'Uninkable Other': 17
}

total_nr_cards_adjusted = 0

for play_draw in ["play", "draw"]:
	succesful_games_nuts = 0
	succesful_games_item = 0
	for _ in range(num_simulations):
		[nuts_result, item_result, cards_result] = run_one_sim(play_draw)
		succesful_games_nuts += nuts_result
		succesful_games_item += item_result
		total_nr_cards_adjusted += cards_result

	print(f"Simulated nuts probability on the {play_draw} ={succesful_games_nuts/num_simulations * 100: .1f}%")
	print(f"Simulated item probability on the {play_draw} ={succesful_games_item/num_simulations * 100: .1f}%")

print("----")
print(f"Expected cards adjusted ={total_nr_cards_adjusted/(num_simulations * 2) : .3f}")
