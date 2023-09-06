print("Let's consider SmallTink into BigTink into Grab Your Sword, on the play!")

#===We do the calculations via five million simulations, using random number generators
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
        'SmallTink': 0,
        'BigTink': 0,
        'Sword': 0,
        'Other': 0,
    }
    for _ in range(7):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1

    SmallTink_on_bottom = 0 if hand['SmallTink'] == 0 else hand['SmallTink'] - 1
    BigTink_on_bottom = 0 if hand['BigTink'] == 0 else hand['BigTink'] - 1
    Sword_on_bottom = 0 if hand['Sword'] == 0 else hand['Sword'] - 1
    if mulligan_strategy == 'hyper-aggressive':
        Other_on_bottom = hand['Other']
    if mulligan_strategy == 'moderate':
        Other_on_bottom = max(min(4 - SmallTink_on_bottom - BigTink_on_bottom - Sword_on_bottom, hand['Other']), 0)
    hand['SmallTink'] -= SmallTink_on_bottom
    hand['BigTink'] -= BigTink_on_bottom
    hand['Sword'] -= Sword_on_bottom
    hand['Other'] -= Other_on_bottom
    library += ['SmallTink'] * SmallTink_on_bottom + ['BigTink'] * BigTink_on_bottom + ['Sword'] * Sword_on_bottom + ['Other'] * Other_on_bottom
    for _ in range(SmallTink_on_bottom + BigTink_on_bottom + Other_on_bottom):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
    random.shuffle(library)

    #Draw cards for turn 2 and 3
    for _ in range(2):
        card_drawn = library.pop(0)
        hand[card_drawn] += 1
    
    #Check if we have SmallTink on turn three
    SmallTink_on_turn_three = hand['SmallTink'] >= 1

    #Draw card for turn 4
    card_drawn = library.pop(0)
    hand[card_drawn] += 1

    #Check if we have BigTink and Sword on turn three
    Combo_on_turn_four = hand['BigTink'] >= 1 and hand['Sword'] >= 1

    return SmallTink_on_turn_three and Combo_on_turn_four

num_simulations = 5000000

for mulligan_strategy in ['hyper-aggressive', 'moderate']:
    print("=" * 30)
    print(f"Let's consider a {mulligan_strategy} mulligan strategy!")
    decklist = {
        'SmallTink': 4,
        'BigTink': 4,
        'Sword': 4,
        'Other': 48
    }
    
    succesful_games = 0
    for _ in range(num_simulations):
        succesful_games += run_one_sim(mulligan_strategy)

    print(f"In a 60-card deck with {decklist['SmallTink']} SmallTink / {decklist['BigTink']} BigTink / {decklist['Sword']} Sword, simulated probability ={succesful_games/num_simulations * 100: .3f}%")
