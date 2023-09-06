print("Let's consider Lilo into Simba, on the play!")

#===We first do the calculations exactly, using probability theory
#===For relatively simple situations, this is preferable

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

Lilo_in_deck = 4
Simba_in_deck = 4
Other_in_deck = 60 - Lilo_in_deck - Simba_in_deck

for mulligan_strategy in ['hyper-aggressive', 'moderate']:
    print("=" * 30)
    print(f"Let's consider a {mulligan_strategy} mulligan strategy!")
    success_prob = 0
    for Lilo_in_opening_7 in range(Lilo_in_deck + 1): #Due to zero-indexing, range(5) is [0, 1, 2, 3, 4]
        for Simba_in_opening_7 in range( min(Simba_in_deck, 7 - Lilo_in_opening_7) + 1):
            Other_in_opening_7 = 7 - Lilo_in_opening_7 - Simba_in_opening_7
            deck = {
                'Lilo': Lilo_in_deck,
                'Simba': Simba_in_deck,
                'Other': Other_in_deck,
                }
            needed = {
                'Lilo': Lilo_in_opening_7,
                'Simba': Simba_in_opening_7,
                'Other': Other_in_opening_7,
                }
            opening_hand_prob = multivariate_hypgeom(deck, needed)
            if mulligan_strategy == 'hyper-aggressive':
                mulligan_draws = Other_in_opening_7 + max(Lilo_in_opening_7 - 1, 0) + max(Simba_in_opening_7 - 1, 0)
            if mulligan_strategy == 'moderate':
                mulligan_draws = 4
            #Let's expand the scenarios
        
            for Lilo_in_mulligan in range(min(mulligan_draws, Lilo_in_deck - Lilo_in_opening_7) + 1):
                for Simba_in_mulligan in range(min(mulligan_draws - Lilo_in_mulligan, Simba_in_deck - Simba_in_opening_7) + 1):
                    #Note that we don't shuffle yet!
                    Other_in_mulligan = mulligan_draws - Lilo_in_mulligan - Simba_in_mulligan
                    deck = {
                        'Lilo': Lilo_in_deck - Lilo_in_opening_7,
                        'Simba': Simba_in_deck - Simba_in_opening_7,
                        'Other': Other_in_deck - Other_in_opening_7
                        }
                    needed = {
                        'Lilo': Lilo_in_mulligan,
                        'Simba': Simba_in_mulligan,
                        'Other': Other_in_mulligan
                    }
                    mulligan_prob = multivariate_hypgeom(deck, needed)
                    
                    if Lilo_in_opening_7 + Lilo_in_mulligan >= 1:
                        if Simba_in_opening_7 + Simba_in_mulligan >= 1:
                            #We don't even need to draw an extra card, we're all set!
                            success_prob += opening_hand_prob * mulligan_prob
                        else:
                            #We hope to topdeck Simba on turn 2. Note that we shuffle
                            topdeck_prob = Simba_in_deck / (60 - 7)
                            success_prob += opening_hand_prob * mulligan_prob * topdeck_prob

    print(f"In a 60-card deck with {Lilo_in_deck} Lilo and {Simba_in_deck} Simba, exact probability ={success_prob * 100: .3f}%")


#===We next do the calculations via one million simulations, using random number generators
#===For more complicated situations, this is far easier and less error-prone to code
import random

def run_one_sim(mulligan_strategy):	
    #Construct library as a list
    library = []
    for card in decklist.keys():
        library += [card] * decklist[card]
    random.shuffle(library)

    #Construct a random opening hand
    hand = {
        'Lilo': 0,
        'Simba': 0,
        'Other': 0,
    }
    for _ in range(7):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1

    Lilo_on_bottom = 0 if hand['Lilo'] == 0 else hand['Lilo'] - 1
    Simba_on_bottom = 0 if hand['Simba'] == 0 else hand['Simba'] - 1
    if mulligan_strategy == 'hyper-aggressive':
        Other_on_bottom = hand['Other']
    if mulligan_strategy == 'moderate':
        Other_on_bottom = max(min(4 - Lilo_on_bottom - Simba_on_bottom, hand['Other']), 0)
    hand['Lilo'] -= Lilo_on_bottom
    hand['Simba'] -= Simba_on_bottom
    hand['Other'] -= Other_on_bottom
    library += ['Lilo'] * Lilo_on_bottom + ['Simba'] * Simba_on_bottom + ['Other'] * Other_on_bottom
    for _ in range(Lilo_on_bottom + Simba_on_bottom + Other_on_bottom):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
    random.shuffle(library)

    #Check if we have Lilo on turn one
    Lilo_on_turn_one = hand['Lilo'] >= 1

    #Draw for the turn
    card_drawn = library.pop(0)
    hand[card_drawn] += 1
    
    Simba_on_turn_two = hand['Simba'] >= 1
    
    return Lilo_on_turn_one and Simba_on_turn_two

num_simulations = 1000000

for mulligan_strategy in ['hyper-aggressive', 'moderate']:
    print("=" * 30)
    print(f"Let's consider a {mulligan_strategy} mulligan strategy!")
    decklist = {
        'Lilo': Lilo_in_deck,
        'Simba': Simba_in_deck,
        'Other': Other_in_deck,
    }
    
    succesful_games = 0
    for _ in range(num_simulations):
        succesful_games += run_one_sim(mulligan_strategy)

    print(f"In a 60-card deck with {Lilo_in_deck} Lilo and {Simba_in_deck} Simba, simulated probability ={succesful_games/num_simulations * 100: .3f}%")
