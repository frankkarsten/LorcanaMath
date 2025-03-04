def binom(n, k):
	"""	
	Parameters:
		n - Number of elements of the entire set
		k - Number of elements in the subset
	It should hold that 0 <= k <= n
	Returns - The binomial coefficient n choose k that represents the number of ways of picking k unordered outcomes from n possibilities
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

def determine_probabilities(nr_items):
	"""	
	Parameters: 
		nr_items - Number of items (Pawpsicle or Fortisphere) in the deck
	Returns - a tuple of two probabilities: (succes on the play, success on the draw)
	"""	
	#For simplicity, I'm ignoring uninkable count. The likelihood of adjusting an opening hand into 1 Item, 1 Belle, and 5 uninkables is neglgible.
	deck = {
		'Item': nr_items,
		'Belle': 4,
		'Other': 60 - 4 - nr_items
	}

	cumulative_success_prob_play = 0
	cumulative_success_prob_draw = 0
	
	#Iterate over all possible initial opening hands
	for Item in range(min(deck['Item'], 7) +1):
		for Belle in range(min(deck['Belle'], 7 - Item) +1):
			Other = 7 - Item - Belle
			cards_drawn = Item + Belle + Other
			#I don't think the next if-statement is actually needed, but it's there just in case
			if (cards_drawn == 7):
				#Determine the probability of drawing this many items and Belles
				needed = {
					'Item': Item,
					'Belle': Belle,
					'Other': Other
				}
				initial_opening_hand_prob = multivariate_hypgeom(deck, needed)
				 
				#Check if we already have Belle plus item
				if Belle >= 1 and Item >= 1:
					cumulative_success_prob_play += initial_opening_hand_prob
					cumulative_success_prob_draw += initial_opening_hand_prob
	
				#If not, we'll mulligan
				else:
					#Keep 1 item if we have one; keep 1 Belle if we have one; toss the rest
					Items_to_keep = min(1, Item)
					Belles_to_keep = min(1, Belle)
					cards_to_adjust = 7 - Items_to_keep - Belles_to_keep
					remaining_deck = {
						'Item': deck['Item'] - Item,
						'Belle': deck['Belle'] - Belle,
						'Other': deck['Other'] - Other
					}
					#Iterate over all possible draws for hand adjustment
					for adjustment_Item in range(min(remaining_deck['Item'], cards_to_adjust) +1):
						for adjustment_Belle in range(min(remaining_deck['Belle'], cards_to_adjust - adjustment_Item) +1):
							adjustment_Other = cards_to_adjust - adjustment_Item - adjustment_Belle
							cards_adjusted = adjustment_Item + adjustment_Belle + adjustment_Other
							#I don't think the next if-statement is actually needed, but it's there just in case
							if (cards_adjusted == cards_to_adjust): 
								#Determine the probability of drawing this many items and Belles in the mulligan
								needed = {
									'Item': adjustment_Item,
									'Belle': adjustment_Belle,
									'Other': adjustment_Other
								}
								adjustment_hand_prob = multivariate_hypgeom(remaining_deck, needed)
								
								#Check if we now have Belle plus item
								if Belle + adjustment_Belle >= 1 and Item + adjustment_Item >= 1:
									cumulative_success_prob_play += initial_opening_hand_prob * adjustment_hand_prob
									cumulative_success_prob_draw += initial_opening_hand_prob * adjustment_hand_prob
	
								#If not, then it's a failure on the play, but we still have a chance on the draw
								if Belle + adjustment_Belle >= 1 and Item + adjustment_Item == 0:
									cumulative_success_prob_draw += initial_opening_hand_prob * adjustment_hand_prob * deck['Item'] / (60 - 7 - cards_to_adjust)
								if Belle + adjustment_Belle == 0 and Item + adjustment_Item >= 1:
									cumulative_success_prob_draw += initial_opening_hand_prob * adjustment_hand_prob * deck['Belle'] / (60 - 7 - cards_to_adjust)
									
	return (cumulative_success_prob_play, cumulative_success_prob_draw)

(cumulative_success_prob_play, cumulative_success_prob_draw) = determine_probabilities(8)
print(f'With 8 items, probability of turn one Belle on the play: {cumulative_success_prob_play * 100:.1f}%.')
print(f'With 8 items, probability of turn one Belle on the draw: {cumulative_success_prob_draw * 100:.1f}%.')

(cumulative_success_prob_play, cumulative_success_prob_draw) = determine_probabilities(4)
print(f'With 4 items, probability of turn one Belle on the play: {cumulative_success_prob_play * 100:.1f}%.')
print(f'With 4 items, probability of turn one Belle on the draw: {cumulative_success_prob_draw * 100:.1f}%.')
