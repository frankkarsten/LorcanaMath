def binom(n, k):
	"""	
	Parameters:
		n - Number of elements of the entire set
		k - Number of elements in the subset
	It should hold that 0 <= k <= n
	Returns - The binomial coefficient n choose k that represents the number of ways of picking k unordered outcomes from n possibilities
	For example, for n=4 and k=2, the resulting binomial coefficient is 6. 
	Indeed, there are 6 ways to choose 2 cards from a library consisting of 4 different cards labeled A, B, C, and D: you have {A, B}, {A, C}, {A, D}, {B, C}, {B, D}, and {C, D}.
	"""
	answer = 1
	for i in range(1, min(k, n - k) + 1):
		answer = answer * (n + 1 - i) / i
	return int(answer)

def multivariate_hypgeom(deck, needed):
	"""	
	Parameters:
		deck - A dictionary of cardname : number of copies
		needed - A dictionary of cardname : number of copies
	It should hold that the cardname keys of deck and needed are identical
	Returns - the multivariate hypergeometric probability of drawing exactly the cards in 'needed' from 'deck' when drawing without replacement 
	"""
	answer = 1
	sum_deck = 0
	sum_needed = 0
	for card in deck.keys():
		answer *= binom(deck[card], needed[card])
		sum_deck += deck[card]
		sum_needed += needed[card]
	return answer / binom(sum_deck, sum_needed)

def determine_ramp_prob_given_opening_hand_on_play(hand):
	if hand["Ramp"] >= 1 and hand["Uninkable"] <= 4:
		return 1
	if hand["Ramp"] >= 1 and hand["Uninkable"] == 5:
		#We'll ink the other card, then hope to draw any inkable
		return 1 - (uninkable_in_deck - 5) / 53
	if hand["Ramp"] >= 1 and hand["Uninkable"] == 6:
		return 0
	if hand["Ramp"] == 0 and hand["Uninkable"] <= 5 and hand["Develop"] == 0:
		#We gotta topdeck
		return ramp_in_deck / 53
	if hand["Ramp"] == 0 and hand["Uninkable"] >= 6 and hand["Develop"] == 0:
		return 0
	if hand["Ramp"] == 0 and hand["Uninkable"] <= 4 and hand["Develop"] >= 1:
		#We have three looks
		return 1 - ( (53 - ramp_in_deck) / 53 ) * ( (52 - ramp_in_deck) / 52 ) * ( (51 - ramp_in_deck) / 51 ) 
	if hand["Ramp"] == 0 and hand["Uninkable"] == 5 and hand["Develop"] >= 1:
		#While this can be determined analytically, it's hellishly time-intensive and error-prone to do so...
		#...so let's approximate by ignoring uninks and just give three looks
		return 1 - ( (53 - ramp_in_deck) / 53 ) * ( (52 - ramp_in_deck) / 52 ) * ( (51 - ramp_in_deck) / 51 ) 
	if hand["Ramp"] == 0 and hand["Uninkable"] >= 6 and hand["Develop"] >= 1:
		return 0

def determine_ramp_prob_given_opening_hand_on_draw(hand):
	inkable_remaining_in_deck = 53 - (uninkable_in_deck - hand["Uninkable"])
	uninkable_remaining_in_deck = uninkable_in_deck - hand["Uninkable"]
	if hand["Ramp"] >= 1 and hand["Uninkable"] <= 4:
		return 1
	if hand["Ramp"] >= 1 and hand["Uninkable"] == 5:
		#We'll ink the other card, then hope to draw any inkable
		return 1 - (uninkable_remaining_in_deck / 53) * ((uninkable_remaining_in_deck - 1) / 52)
	if hand["Ramp"] >= 1 and hand["Uninkable"] == 6:
		#We'll need to draw ink into ink
		return (inkable_remaining_in_deck / 53) * ((inkable_remaining_in_deck - 1) / 52)
	if hand["Ramp"] == 0 and hand["Uninkable"] <= 5 and hand["Develop"] == 0:
		#We gotta topdeck
		return ramp_in_deck / 53 + (1 - ramp_in_deck / 53) * ramp_in_deck / 52
	if hand["Ramp"] == 0 and hand["Uninkable"] == 6 and hand["Develop"] == 0:
		#Ramp, then any ink; or any non-ramp ink, then ramp
		return (ramp_in_deck / 53) * ((inkable_remaining_in_deck - 1) / 52) + ((inkable_remaining_in_deck - ramp_in_deck) / 53) * (ramp_in_deck / 52)
	if hand["Ramp"] == 0 and hand["Uninkable"] == 7 and hand["Develop"] == 0:
		return 0
	if hand["Ramp"] == 0 and hand["Uninkable"] <= 4 and hand["Develop"] >= 1:
		#We have four looks
		return 1 - ( (53 - ramp_in_deck) / 53 ) * ( (52 - ramp_in_deck) / 52 ) * ( (51 - ramp_in_deck) / 51 ) * ( (50 - ramp_in_deck) / 50 ) 
	if hand["Ramp"] == 0 and hand["Uninkable"] >= 5 and hand["Develop"] >= 1:
		#While this can be determined analytically, it's hellishly time-intensive and error-prone to do so...
		#...so let's approximate by ignoring uninks and just give four looks
		return 1 - ( (53 - ramp_in_deck) / 53 ) * ( (52 - ramp_in_deck) / 52 ) * ( (51 - ramp_in_deck) / 51 ) * ( (50 - ramp_in_deck) / 50 ) 

ramp_in_deck = 8
uninkable_in_deck = 12
mull_strat = "keep develop"
print("We now determine the probability of hitting ramp on turn two in a 60-card deck containing a certain number of Develop Your Brain, 8 ramp effects, 12 irrelevant uninkables, and the rest all inkable cards.")

for mull_strat in ["full mull", "keep develop"]:
	for playdraw in ["play", "draw"]:
		
		for develop_in_deck in [0,1,2,3,4,5,6,7,8]:
			other_in_deck = 60 - ramp_in_deck - uninkable_in_deck - develop_in_deck
			ramp_prob = 0
		
			for ramp_in_opening_7 in range(min (7, ramp_in_deck) + 1): #Due to zero-indexing, range(5) is [0, 1, 2, 3, 4]
				for develop_in_opening_7 in range( min(develop_in_deck, 7 - ramp_in_opening_7) + 1):
					for uninkable_in_opening_7 in range( min(uninkable_in_deck, 7 - ramp_in_opening_7 - develop_in_opening_7) + 1):
						other_in_opening_7 = 7 - ramp_in_opening_7 - develop_in_opening_7 - uninkable_in_opening_7
						deck = {
							'Ramp': ramp_in_deck,
							'Develop': develop_in_deck,
							'Uninkable': uninkable_in_deck,
							'Other': other_in_deck
							}
						needed = {
							'Ramp': ramp_in_opening_7,
							'Develop': develop_in_opening_7,
							'Uninkable': uninkable_in_opening_7,
							'Other': other_in_opening_7
							}
						opening_hand_prob = multivariate_hypgeom(deck, needed)
						ramp_on_bottom = 0
						uninkable_on_bottom = uninkable_in_opening_7
						develop_on_bottom = 0 if ramp_in_opening_7 > 0 else (develop_in_opening_7 if mull_strat == "full mull" else max(develop_in_opening_7 - 1, 0))
						other_on_bottom = 0 if ramp_in_opening_7 > 0 else other_in_opening_7
						mulligan_draws = uninkable_on_bottom + develop_on_bottom + other_on_bottom
						for ramp_in_mull in range(min (mulligan_draws, ramp_in_deck - ramp_in_opening_7) + 1): #Due to zero-indexing, range(5) is [0, 1, 2, 3, 4]
							for develop_in_mull in range( min(mulligan_draws - ramp_in_mull, develop_in_deck - develop_in_opening_7) + 1):
								for uninkable_in_mull in range( min(mulligan_draws - ramp_in_mull - develop_in_mull, uninkable_in_deck - uninkable_in_opening_7) + 1):
									other_in_mull = mulligan_draws - ramp_in_mull - develop_in_mull - uninkable_in_mull
									deck = {
										'Ramp': ramp_in_deck - ramp_in_opening_7,
										'Develop': develop_in_deck - develop_in_opening_7,
										'Uninkable': uninkable_in_deck - uninkable_in_opening_7,
										'Other': other_in_deck - other_in_opening_7
										}
									needed = {
										'Ramp': ramp_in_mull,
										'Develop': develop_in_mull,
										'Uninkable': uninkable_in_mull,
										'Other': other_in_mull
										}
									mulligan_prob = multivariate_hypgeom(deck, needed)
			
									hand_after_mull = {
										'Ramp': ramp_in_opening_7 + ramp_in_mull - ramp_on_bottom,
										'Develop': develop_in_opening_7 + develop_in_mull - develop_on_bottom,
										'Uninkable': uninkable_in_opening_7 + uninkable_in_mull - uninkable_on_bottom,
										'Other': other_in_opening_7 + other_in_mull - other_on_bottom
										}
									if sum(hand_after_mull.values()) != 7:
										print("ERROR:", hand_after_mull)
									if playdraw == "play":
										ramp_prob += opening_hand_prob * mulligan_prob * determine_ramp_prob_given_opening_hand_on_play(hand_after_mull)
									if playdraw == "draw":
										ramp_prob += opening_hand_prob * mulligan_prob * determine_ramp_prob_given_opening_hand_on_draw(hand_after_mull)
	
			print(f"For {mull_strat} with {develop_in_deck} Develop on {playdraw}: {ramp_prob*100:.2f}")

print("\nWe next determine the probability of hitting ramp on turn two in a 60-card deck containing a certain number of Develop Your Brain, a certain number of ramp effects, 12 irrelevant uninkables, and the rest all inkable cards.")
mull_strat = "keep develop"

for playdraw in ["play", "draw"]:
	for develop_in_deck in [0,1,2,3,4]:
		for ramp_in_deck in [8, 9, 10, 11]:
			other_in_deck = 60 - ramp_in_deck - uninkable_in_deck - develop_in_deck
			ramp_prob = 0
		
			for ramp_in_opening_7 in range(min (7, ramp_in_deck) + 1): #Due to zero-indexing, range(5) is [0, 1, 2, 3, 4]
				for develop_in_opening_7 in range( min(develop_in_deck, 7 - ramp_in_opening_7) + 1):
					for uninkable_in_opening_7 in range( min(uninkable_in_deck, 7 - ramp_in_opening_7 - develop_in_opening_7) + 1):
						other_in_opening_7 = 7 - ramp_in_opening_7 - develop_in_opening_7 - uninkable_in_opening_7
						deck = {
							'Ramp': ramp_in_deck,
							'Develop': develop_in_deck,
							'Uninkable': uninkable_in_deck,
							'Other': other_in_deck
							}
						needed = {
							'Ramp': ramp_in_opening_7,
							'Develop': develop_in_opening_7,
							'Uninkable': uninkable_in_opening_7,
							'Other': other_in_opening_7
							}
						opening_hand_prob = multivariate_hypgeom(deck, needed)
						ramp_on_bottom = 0
						uninkable_on_bottom = uninkable_in_opening_7
						develop_on_bottom = 0 if ramp_in_opening_7 > 0 else (develop_in_opening_7 if mull_strat == "full mull" else max(develop_in_opening_7 - 1, 0))
						other_on_bottom = 0 if ramp_in_opening_7 > 0 else other_in_opening_7
						mulligan_draws = uninkable_on_bottom + develop_on_bottom + other_on_bottom
						for ramp_in_mull in range(min (mulligan_draws, ramp_in_deck - ramp_in_opening_7) + 1): #Due to zero-indexing, range(5) is [0, 1, 2, 3, 4]
							for develop_in_mull in range( min(mulligan_draws - ramp_in_mull, develop_in_deck - develop_in_opening_7) + 1):
								for uninkable_in_mull in range( min(mulligan_draws - ramp_in_mull - develop_in_mull, uninkable_in_deck - uninkable_in_opening_7) + 1):
									other_in_mull = mulligan_draws - ramp_in_mull - develop_in_mull - uninkable_in_mull
									deck = {
										'Ramp': ramp_in_deck - ramp_in_opening_7,
										'Develop': develop_in_deck - develop_in_opening_7,
										'Uninkable': uninkable_in_deck - uninkable_in_opening_7,
										'Other': other_in_deck - other_in_opening_7
										}
									needed = {
										'Ramp': ramp_in_mull,
										'Develop': develop_in_mull,
										'Uninkable': uninkable_in_mull,
										'Other': other_in_mull
										}
									mulligan_prob = multivariate_hypgeom(deck, needed)
			
									hand_after_mull = {
										'Ramp': ramp_in_opening_7 + ramp_in_mull - ramp_on_bottom,
										'Develop': develop_in_opening_7 + develop_in_mull - develop_on_bottom,
										'Uninkable': uninkable_in_opening_7 + uninkable_in_mull - uninkable_on_bottom,
										'Other': other_in_opening_7 + other_in_mull - other_on_bottom
										}
									if sum(hand_after_mull.values()) != 7:
										print("ERROR:", hand_after_mull)
									if playdraw == "play":
										ramp_prob += opening_hand_prob * mulligan_prob * determine_ramp_prob_given_opening_hand_on_play(hand_after_mull)
									if playdraw == "draw":
										ramp_prob += opening_hand_prob * mulligan_prob * determine_ramp_prob_given_opening_hand_on_draw(hand_after_mull)
	
			print(f"For {mull_strat} with {develop_in_deck} Develop and {ramp_in_deck} Ramp on {playdraw}: {ramp_prob*100:.2f}")
	



#We can sanity check these numbers through simulation, and also use this to easily run the numbers on a build with 4 Develop and 4 Pawpsicle
import random

def choose_ink_and_adjust_hand(hand, turn):
	#We take a hand and, according to a step-by-step logic, pick a card to ink
	#Returns true if we indeed chose a card for ink, and False in the rare case where we can't
	if hand['Other'] >= 1:
		hand['Other'] -= 1
		return True
	if hand['Pawpsicle'] >= 1:
		hand['Pawpsicle'] -= 1
		return True
	if hand['Develop'] >= 1:
		hand['Develop'] -= 1
		return True
	if hand['Ramp'] >= 1:
		hand['Ramp'] -= 1
		return True
	return False

def run_one_sim(play_or_draw, keep_develop):	
	#Construct library as a list
	library = []
	for card in decklist.keys():
		library += [card] * decklist[card]
	random.shuffle(library)

	#Construct a random opening hand
	hand = {
		'Ramp': 0,
		'Develop': 0,
		'Uninkable': 0,
		'Pawpsicle': 0,
		'Other': 0
	}
	for _ in range(7):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1

	#Adjust the hand by figuring out what to put on the bottom
	uninkable_on_bottom = hand['Uninkable']
	hand['Uninkable'] = 0
	
	other_on_bottom = 0
	develop_on_bottom = 0
	pawp_on_bottom = 0
	
	if hand['Ramp'] == 0:
		other_on_bottom = hand['Other']
		hand['Other'] = 0
		pawp_on_bottom = hand['Pawpsicle']
		hand['Pawpsicle'] = 0
		
	if keep_develop:
		develop_on_bottom = max(hand['Develop'] - 1, 0)
		hand['Develop'] = 1 if hand['Develop'] >= 1 else 0
	else:
		develop_on_bottom = hand['Develop']
		hand['Develop'] = 0

	library += ['Uninkable'] * uninkable_on_bottom + ['Other'] * other_on_bottom + ['Develop'] * develop_on_bottom + ['Pawpsicle'] * pawp_on_bottom
	nr_cards_adjusted = uninkable_on_bottom + other_on_bottom + develop_on_bottom + pawp_on_bottom
	for _ in range(nr_cards_adjusted):
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
	random.shuffle(library)
	
	#Draw potential card for turn 1
	if play_or_draw == "draw":
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
		
	#Check if we have Develop on turn one
	InkTurnOne = choose_ink_and_adjust_hand(hand, 1)
	if hand['Develop'] >= 1:
		hand['Develop'] -= 1
		top_two_cards = [library.pop(0), library.pop(0)]
		if "Ramp" in top_two_cards:
			hand['Ramp'] += 1
		elif 'Develop' in top_two_cards:
			hand['Develop'] += 1
		elif 'Other' in top_two_cards:
			hand['Other'] += 1
		elif 'Uninkable' in top_two_cards:
			hand['Uninkable'] += 1
	elif hand['Pawpsicle'] >= 1:
		hand['Pawpsicle'] -= 1
		card_drawn = library.pop(0)
		hand[card_drawn] += 1
		
	#Draw card for turn 2
	card_drawn = library.pop(0)
	hand[card_drawn] += 1

	#Check if we have everything for turn two
	InkTurnTwo = choose_ink_and_adjust_hand(hand, 1)
	Ramp_on_turn_two = hand['Ramp'] >= 1
	
	return InkTurnOne and InkTurnTwo and Ramp_on_turn_two

num_simulations = 2000000

decklist = {
	'Ramp': 8,
	'Develop': 4,
	'Uninkable': 12,
	'Pawpsicle': 4,
	'Other': 32
}

keep_develop = False
for play_draw in ["play", "draw"]:
	succesful_games_ramp = 0
	for i in range(num_simulations):
		succesful_games_ramp += run_one_sim(play_draw, keep_develop)
		if i > 0 and i % 250000 == 0:
			print("Running simulation number", i)
	print(f"Simulated ramp probability, when keep_develop is {keep_develop}, with {decklist} = {succesful_games_ramp/num_simulations * 100: .2f}%")

