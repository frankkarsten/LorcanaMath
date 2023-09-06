turn_draws = 6 #On the play, turn 1 doesn't count, but turns 2 through 7 draw a card for the turn
inkables_needed = 7 #We want 7 ink by turn 7
print("Let's use a reasonable mulligan strategy!")
print(f"We'll consider the probability of having {inkables_needed} ink by turn {turn_draws +1} on the play")

#===We first do the calculations exactly, using probability theory
#===For relatively simple situations, this is preferable as it's exact and fast

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

for non_inkables_in_deck in range(11, 31):
    inkables_in_deck = 60 - non_inkables_in_deck
    success_prob = 0
    
    #We now enumerate all posssibilities
    for inkables_in_opening_hand in [0, 1, 2, 3, 4, 5, 6, 7]:
        non_inkables_in_opening_hand = 7 - inkables_in_opening_hand
        deck = {
            'Inkables': inkables_in_deck,
            'Non-inkables': non_inkables_in_deck
            }
        needed = {
            'Inkables': inkables_in_opening_hand,
            'Non-inkables': non_inkables_in_opening_hand
            }
        
        #Use a mulligan strategy that aims to get close to 2 non-inkables and 5 inkables
        
        opening_hand_prob = multivariate_hypgeom(deck, needed)
        
        if inkables_in_opening_hand == 7:
            non_inkables_on_bottom = 0
            inkables_on_bottom = 4
        elif inkables_in_opening_hand == 6:
            non_inkables_on_bottom = 0
            inkables_on_bottom = 3
        elif inkables_in_opening_hand == 5:
            non_inkables_on_bottom = 0
            inkables_on_bottom = 0
        elif inkables_in_opening_hand == 4:
            non_inkables_on_bottom = 1
            inkables_on_bottom = 0
        elif inkables_in_opening_hand == 3:
            non_inkables_on_bottom = 2
            inkables_on_bottom = 0
        elif inkables_in_opening_hand == 2:
            non_inkables_on_bottom = 4
            inkables_on_bottom = 0
        elif inkables_in_opening_hand == 1:
            non_inkables_on_bottom = 5
            inkables_on_bottom = 0
        elif inkables_in_opening_hand == 0:
            non_inkables_on_bottom = 7
            inkables_on_bottom = 0
            
        non_inkables_kept = non_inkables_in_opening_hand - non_inkables_on_bottom
        inkables_kept = inkables_in_opening_hand - inkables_on_bottom
        mulligan_draws = non_inkables_on_bottom + inkables_on_bottom
        #Given this opening hand, let's expand the scenarios for the set of cards we could draw in a mulligan
        
        for inkables_in_mulligan_draw in range(mulligan_draws + 1):
            non_inkables_in_mulligan_draw = mulligan_draws - inkables_in_mulligan_draw
            #Note that we don't shuffle yet!
            deck = {
                'Inkables': inkables_in_deck - inkables_in_opening_hand,
                'Non-inkables': non_inkables_in_deck - non_inkables_in_opening_hand
                }
            needed = {
                'Inkables': inkables_in_mulligan_draw,
                'Non-inkables': non_inkables_in_mulligan_draw
                }
            mulligan_prob = multivariate_hypgeom(deck, needed)
    
            #After this mulligan, let's expand the scenarios for the set of cards we could draw over several turns
            for inkables_in_turn_draws in range(turn_draws + 1):
                non_inkables_in_turn_draws = turn_draws - inkables_in_turn_draws
                #Note that we have shuffled the deck now!
                deck = {
                    'Inkables': inkables_in_deck - inkables_kept - inkables_in_mulligan_draw,
                    'Non-inkables': non_inkables_in_deck - non_inkables_kept - non_inkables_in_mulligan_draw
                    }
                needed = {
                    'Inkables': inkables_in_turn_draws,
                    'Non-inkables': non_inkables_in_turn_draws
                    }
                turn_prob = multivariate_hypgeom(deck, needed)
                
                scenario_prob = opening_hand_prob * mulligan_prob * turn_prob
                total_inkables = inkables_kept + inkables_in_mulligan_draw + inkables_in_turn_draws
                if (total_inkables >= inkables_needed):
                    success_prob += scenario_prob
                    
    print(f"In a 60-card deck with {non_inkables_in_deck} non-inkables, exact probability ={success_prob * 100: .3f}%")

#===We next do the calculations via one hundred thousand simulations, using random number generators
#===For more complicated situations, this is far easier and less error-prone to code
import random

def run_one_sim():	
    #Construct library as a list
    library = []
    for card in decklist.keys():
        library += [card] * decklist[card]
    random.shuffle(library)

    #Construct a random opening hand
    hand = {
        'Inkable': 0,
		'Non-inkable': 0,
    }
    for _ in range(7):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1

    #Mulligan
    if hand['Inkable'] == 7:
        non_inkables_on_bottom = 0
        inkables_on_bottom = 4
    elif hand['Inkable'] == 6:
        non_inkables_on_bottom = 0
        inkables_on_bottom = 3
    elif hand['Inkable'] == 5:
        non_inkables_on_bottom = 0
        inkables_on_bottom = 0
    elif hand['Inkable'] == 4:
        non_inkables_on_bottom = 1
        inkables_on_bottom = 0
    elif hand['Inkable'] == 3:
        non_inkables_on_bottom = 2
        inkables_on_bottom = 0
    elif hand['Inkable'] == 2:
        non_inkables_on_bottom = 4
        inkables_on_bottom = 0
    elif hand['Inkable'] == 1:
        non_inkables_on_bottom = 5
        inkables_on_bottom = 0
    elif hand['Inkable'] == 0:
        non_inkables_on_bottom = 7
        inkables_on_bottom = 0
    hand['Inkable'] -= inkables_on_bottom
    hand['Non-inkable'] -= non_inkables_on_bottom
    library += ['Inkable'] * inkables_on_bottom + ['Non-inkable'] * non_inkables_on_bottom
    for _ in range(inkables_on_bottom + non_inkables_on_bottom):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
    random.shuffle(library)

    #Draw for the turns
    for _ in range(turn_draws):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
    
    #Check if we have enough inkables at the end
    return 1 if hand['Inkable'] >= inkables_needed else 0

num_simulations = 100000
        
for non_inkables_in_deck in range(11, 31):
    decklist = {
        'Inkable': 60 - non_inkables_in_deck,
        'Non-inkable': non_inkables_in_deck
    }
    
    succesful_games = 0
    for _ in range(num_simulations):
        succesful_games += run_one_sim()

    print(f"In a 60-card deck with {non_inkables_in_deck} non-inkables, simulated probability ={succesful_games/num_simulations * 100: .3f}%")