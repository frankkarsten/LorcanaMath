#===We do the calculations via five million simulations, using random number generators
#===For more complicated situations, this is far easier and less error-prone to code
import random

def choose_ink_and_adjust_hand(hand, turn):
	#We take a hand and, according to a step-by-step logic, pick a card to ink
	#Returns true if we indeed chose a card for ink, and False in the rare case where we can't
	if hand['Inkable Other'] >= 1:
		hand['Inkable Other'] -= 1
		return True
	if hand['Inkable Action'] >= 2:
		hand['Inkable Action'] -= 1
		return True
	if hand['Two-drop Ursula'] >= 1:
		hand['Two-drop Ursula'] -= 1
		return True
	if hand['Small Robin'] >= 1:
		hand['Small Robin'] -= 1
		return True
	if hand['Small Diablo'] >= 2 and turn == 1:
		hand['Small Diablo'] -= 1
		return True
	if hand['Small Diablo'] >= 1 and turn == 2:
		hand['Small Diablo'] -= 1
		return True
	if hand['Bucky'] >= 2:
		hand['Bucky'] -= 1
		return True
	if hand['Inkable Action'] >= 1:
		hand['Inkable Action'] -= 1
		return True
	if hand['Small Diablo'] == 1 and turn == 1:
		hand['Small Diablo'] -= 1
		return True
	if hand['Bucky'] >= 1 and turn == 1:
		hand['Bucky'] -= 1
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
		'Small Diablo': 0,
		'Small Robin': 0,
		'Bucky': 0,
		'Two-drop Ursula': 0,
		'Big Diablo': 0,
		'Inkable Action': 0,
		'Uninkable Action': 0,
		'Inkable Other': 0,
		'Uninkable Other': 0
	}
    for _ in range(7):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1

    #Adjust the hand by figuring out what to put on the bottom
	#Mulligan strategy: first figure out if our hand is already perfect (save potentially for having enough ink)
    WeAlreadyHaveCharacterNuts = True if hand['Small Diablo'] >= 1 and hand['Bucky'] >= 1 and hand['Big Diablo'] >= 1 else False
    WeAlsoHaveAction = True if hand['Inkable Action'] + hand['Inkable Action'] >= 1 else False
    WeGotItAll = WeAlreadyHaveCharacterNuts and WeAlsoHaveAction
	#1. We keep one Small Diablo if possible and, unless we already have the character nuts, mulligan excess copies.
    SmallDiablo_on_bottom = 0 if hand['Small Diablo'] == 0 else (hand['Small Diablo'] - 1 if not WeGotItAll else 0)
	#2. If there was no Small Diablo, we try to secure a one-drop by keeping one small Robin if possible
    SmallRobin_on_bottom = hand['Small Robin'] if hand['Small Diablo'] >= 1 else max(0, hand['Small Robin'] - 1)
	#3. We keep one Bucky if possible and, unless we already have the character nuts, mulligan excess copies
    Bucky_on_bottom = 0 if hand['Bucky'] == 0 else (hand['Bucky'] - 1 if not WeGotItAll else 0)
	#4. If there was no Bucky, we try to secure a two-drop by keeping a small Ursula if possible
    TwoDropUrsula_on_bottom = hand['Two-drop Ursula'] if hand['Bucky'] >= 1 else max(0, hand['Two-drop Ursula'] - 1)
	#5. We keep one Big Diablo if possible and mulligan excess copies.
    BigDiablo_on_bottom = 0 if hand['Big Diablo'] == 0 else hand['Big Diablo'] - 1
	#6. If we already have all characters for the nuts, we keep an action and two ink if possible. Otherwise, we mulligan them all in search of characters.
    InkableAction_on_bottom = hand['Inkable Action'] if not WeAlreadyHaveCharacterNuts else max(0, hand['Inkable Action'] - 3)
    UninkableAction_on_bottom = hand['Uninkable Action'] if not WeAlreadyHaveCharacterNuts else max(0, hand['Uninkable Action'] - 1)
    InkableOther_on_bottom = hand['Inkable Other'] if not WeGotItAll else 0
    UninkableOther_on_bottom = hand['Uninkable Other']
    hand['Small Diablo'] -= SmallDiablo_on_bottom
    hand['Small Robin'] -= SmallRobin_on_bottom
    hand['Bucky'] -= Bucky_on_bottom
    hand['Two-drop Ursula'] -= TwoDropUrsula_on_bottom
    hand['Big Diablo'] -= BigDiablo_on_bottom
    hand['Inkable Action'] -= InkableAction_on_bottom
    hand['Uninkable Action'] -= UninkableAction_on_bottom
    hand['Inkable Other'] -= InkableOther_on_bottom
    hand['Uninkable Other'] -= UninkableOther_on_bottom

    library += ['Small Diablo'] * SmallDiablo_on_bottom + ['Small Robin'] * SmallRobin_on_bottom + ['Bucky'] * Bucky_on_bottom + ['Two-drop Ursula'] * TwoDropUrsula_on_bottom
    library += ['Big Diablo'] * BigDiablo_on_bottom + ['Inkable Action'] * InkableAction_on_bottom + ['Uninkable Action'] * UninkableAction_on_bottom
    library += ['Inkable Other'] * InkableOther_on_bottom + ['Uninkable Other'] * UninkableOther_on_bottom 
	
    nr_cards_adjusted = SmallDiablo_on_bottom + SmallRobin_on_bottom + Bucky_on_bottom + TwoDropUrsula_on_bottom + BigDiablo_on_bottom + InkableAction_on_bottom + UninkableAction_on_bottom + InkableOther_on_bottom + UninkableOther_on_bottom
    for _ in range(nr_cards_adjusted):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
    random.shuffle(library)
	
    #Draw potential card for turn 1
    if play_or_draw == "draw":
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
		
    #Check if we have Small Diablo on turn one
    InkThisTurn = choose_ink_and_adjust_hand(hand, 1)
    SmallDiablo_on_turn_one = hand['Small Diablo'] >= 1 and InkThisTurn
    if SmallDiablo_on_turn_one:
        hand['Small Diablo'] -= 1
	
    #Draw card for turn 2
    card_drawn = library.pop(0)
    hand[card_drawn] += 1

    #Check if we have everything for turn two
    InkThisTurn = choose_ink_and_adjust_hand(hand, 2)
    Bucky_on_turn_two = hand['Bucky'] >= 1 and InkThisTurn
    Nuts_on_turn_two = hand['Bucky'] >= 1 and hand['Big Diablo'] >= 1 and hand['Inkable Action'] + hand['Uninkable Action'] >= 1 and InkThisTurn
	
    return [SmallDiablo_on_turn_one and Nuts_on_turn_two, Bucky_on_turn_two, nr_cards_adjusted]

num_simulations = 5000000

decklist = {
	'Small Diablo': 4,
	'Small Robin': 4,
	'Bucky': 4,
	'Two-drop Ursula': 4,
	'Big Diablo': 4,
	'Inkable Action': 10,
	'Uninkable Action': 5,
	'Inkable Other': 22,
	'Uninkable Other': 3
}

nr_cards_adjusted = 0
for play_draw in ["play", "draw"]:
	succesful_games_nuts = 0
	succesful_games_Bucky = 0
	for _ in range(num_simulations):
		[nuts_result, Bucky_result, cards_result] = run_one_sim(play_draw)
		succesful_games_nuts += nuts_result
		succesful_games_Bucky += Bucky_result
		nr_cards_adjusted += cards_result
		
	print(f"Simulated nuts probability on the {play_draw} ={succesful_games_nuts/num_simulations * 100: .1f}%")
	print(f"Simulated Bucky probability on the {play_draw} ={succesful_games_Bucky/num_simulations * 100: .1f}%")

print("----")
print(f"Expected cards adjusted ={nr_cards_adjusted/(num_simulations * 2) : .2f}")
