import nashpy as nash
import numpy as np

Lineup_1 = ['Steelsong', 'Green Purple Diablo', 'Red Blue Shark']
Lineup_2 = ['Amber Steel Aggro', 'Green Purple Tempo', 'Red Blue Items']

Winprob_play = {
	('Steelsong', 'Amber Steel Aggro'): 0.67,
	('Steelsong', 'Green Purple Tempo'): 0.64,
	('Steelsong', 'Red Blue Items'): 0.51,
	('Green Purple Diablo', 'Amber Steel Aggro'): 0.60,
	('Green Purple Diablo', 'Green Purple Tempo'): 0.57,
	('Green Purple Diablo', 'Red Blue Items'): 0.61,
	('Red Blue Shark', 'Amber Steel Aggro'): 0.62,
	('Red Blue Shark', 'Green Purple Tempo'): 0.55,
	('Red Blue Shark', 'Red Blue Items'): 0.48
} 
	
Winprob_draw = {
	('Steelsong', 'Amber Steel Aggro'): 0.46,
	('Steelsong', 'Green Purple Tempo'): 0.47,
	('Steelsong', 'Red Blue Items'): 0.27,
	('Green Purple Diablo', 'Amber Steel Aggro'): 0.40,
	('Green Purple Diablo', 'Green Purple Tempo'): 0.41,
	('Green Purple Diablo', 'Red Blue Items'): 0.45,
	('Red Blue Shark', 'Amber Steel Aggro'): 0.43,
	('Red Blue Shark', 'Green Purple Tempo'): 0.39,
	('Red Blue Shark', 'Red Blue Items'): 0.36
} 

best_winrates_for_ban = {}
avg_winrate = 0

print("Lineup 1: ", Lineup_1)
print("Lineup 2: ", Lineup_2)
print("")

# Strategy name to index mappings
Lineup_1_index = {name: i for i, name in enumerate(Lineup_2)}
Lineup_2_index = {name: j for j, name in enumerate(Lineup_1)}

def set_payoff(strat_1, strat_2, payoff):
    """Set the payoff for a given strategy pair."""
    i = Lineup_1_index[strat_1]
    j = Lineup_2_index[strat_2]
    Lineup_1_payoffs_for_bans[i, j] = payoff[0] 
    Lineup_2_payoffs_for_bans[i, j] = payoff[1] 

for die_roll in ['Lineup 1 Play first', 'Lineup 1 Draw first']:
	print("==========Die roll: ", die_roll)
	Lineup_1_payoffs_for_bans = np.zeros((3, 3))
	Lineup_2_payoffs_for_bans = np.zeros((3, 3))
	
	for banned_deck1 in Lineup_1:
		for banned_deck2 in Lineup_2:
			print("")
			print("---In case of bans:", banned_deck1, ", ", banned_deck2)
			list_of_decks_1 = Lineup_1.copy()
			list_of_decks_2 = Lineup_2.copy()
			list_of_decks_1.remove(banned_deck1)
			list_of_decks_2.remove(banned_deck2)
			
			for first_deck_1 in list_of_decks_1:
				second_deck_1 = (set(list_of_decks_1) - {first_deck_1}).pop()
				for first_deck_2 in list_of_decks_2:
					second_deck_2 = (set(list_of_decks_2) - {first_deck_2}).pop()

					#What should player 1 do in case of game 1 loss?
					remaining_chance_if_switch = Winprob_play[(second_deck_1, second_deck_2)] * Winprob_draw[(first_deck_1, second_deck_2)]
					remaining_chance_if_stay = Winprob_play[(first_deck_1, second_deck_2)] * Winprob_draw[(second_deck_1, second_deck_2)]
					player_1_switch_in_case_of_game_1_loss = 'Switch' if remaining_chance_if_switch > remaining_chance_if_stay else 'Stay'
					#What should player 2 do in case of game 1 loss?
					remaining_chance_if_switch = (1 - Winprob_play[(second_deck_1, second_deck_2)]) * (1 - Winprob_draw[(second_deck_1, first_deck_2)])
					remaining_chance_if_stay = (1 - Winprob_play[(second_deck_1, first_deck_2)]) * (1 - Winprob_draw[(second_deck_1, second_deck_2)])
					player_2_switch_in_case_of_game_1_loss = 'Switch' if remaining_chance_if_switch > remaining_chance_if_stay else 'Stay'
			
			
					if die_roll == 'Lineup 1 Play first':
						if player_2_switch_in_case_of_game_1_loss == 'Switch':
							WW = Winprob_play[(first_deck_1, first_deck_2)] * Winprob_draw[(second_deck_1, second_deck_2)]
							WLW = Winprob_play[(first_deck_1, first_deck_2)] * (1 - Winprob_draw[(second_deck_1, second_deck_2)]) * Winprob_play[(second_deck_1, first_deck_2)]
						elif player_2_switch_in_case_of_game_1_loss == 'Stay':
							WW = Winprob_play[(first_deck_1, first_deck_2)] * Winprob_draw[(second_deck_1, first_deck_2)]
							WLW = Winprob_play[(first_deck_1, first_deck_2)] * (1 - Winprob_draw[(second_deck_1, first_deck_2)]) * Winprob_play[(second_deck_1, second_deck_2)]
						if player_1_switch_in_case_of_game_1_loss == 'Switch':
							LWW = (1 - Winprob_play[(first_deck_1, first_deck_2)]  ) * Winprob_play[(second_deck_1, second_deck_2)] * Winprob_draw[(first_deck_1, second_deck_2)]
						elif player_1_switch_in_case_of_game_1_loss == 'Stay':
							LWW = (1 - Winprob_play[(first_deck_1, first_deck_2)]  ) * Winprob_play[(first_deck_1, second_deck_2)] * Winprob_draw[(second_deck_1, second_deck_2)]

					if die_roll == 'Lineup 1 Draw first':
						if player_2_switch_in_case_of_game_1_loss == 'Switch':
							WW = Winprob_draw[(first_deck_1, first_deck_2)] * Winprob_draw[(second_deck_1, second_deck_2)]
							WLW = Winprob_draw[(first_deck_1, first_deck_2)] * (1 - Winprob_draw[(second_deck_1, second_deck_2)]) * Winprob_play[(second_deck_1, first_deck_2)]
						elif player_2_switch_in_case_of_game_1_loss == 'Stay':
							WW = Winprob_draw[(first_deck_1, first_deck_2)] * Winprob_draw[(second_deck_1, first_deck_2)]
							WLW = Winprob_draw[(first_deck_1, first_deck_2)] * (1 - Winprob_draw[(second_deck_1, first_deck_2)]) * Winprob_play[(second_deck_1, second_deck_2)]
						if player_1_switch_in_case_of_game_1_loss == 'Switch':
							LWW = (1 - Winprob_draw[(first_deck_1, first_deck_2)]  ) * Winprob_play[(second_deck_1, second_deck_2)] * Winprob_draw[(first_deck_1, second_deck_2)]
						elif player_1_switch_in_case_of_game_1_loss == 'Stay':
							LWW = (1 - Winprob_play[(first_deck_1, first_deck_2)]  ) * Winprob_play[(first_deck_1, second_deck_2)] * Winprob_draw[(second_deck_1, second_deck_2)]
							
					match_win_prob = WW + WLW + LWW
					
					if first_deck_1 == list_of_decks_1[0] and first_deck_2 == list_of_decks_2[0]:
						payoff00 = match_win_prob
					if first_deck_1 == list_of_decks_1[0] and first_deck_2 == list_of_decks_2[1]:
						payoff01 = match_win_prob
					if first_deck_1 == list_of_decks_1[1] and first_deck_2 == list_of_decks_2[0]:
						payoff10 = match_win_prob
					if first_deck_1 == list_of_decks_1[1] and first_deck_2 == list_of_decks_2[1]:
						payoff11 = match_win_prob

			A = np.array([  [payoff00, payoff01], 
						    [payoff10, payoff11] ])
			B = np.array([  [1-payoff00, 1-payoff01], 
						    [1-payoff10, 1-payoff11] ])
			game = nash.Game(A, B)

			# Compute Nash equilibria
			equilibria = game.support_enumeration()
			for eq_num, (strat1, strat2) in enumerate(equilibria, start=1):
				lineup1_payoff = strat1 @ A @ strat2
				print(f"Equilibrium for first deck choices: {strat1[0]:.2f} {first_deck_1} {strat1[1]:.2f} {second_deck_1}; {strat2[0]:.2f} {first_deck_2} {strat2[1]:.2f} {second_deck_2}.   Payoff for Lineup 1: {str(round(lineup1_payoff, 5))}")
			set_payoff(banned_deck2, banned_deck1, (lineup1_payoff, 1 - lineup1_payoff))

	print("")
	print(" --------- Full solution ")			
	full_game = nash.Game(Lineup_1_payoffs_for_bans, Lineup_2_payoffs_for_bans)
	
	# Print equilibria and expected payoffs
	for eq_num, (alice_strategy, bob_strategy) in enumerate(full_game.support_enumeration(), start=1):
	    print(f"Equilibrium {eq_num}: these are the probabilities for a lineup to ban the opposing deck")
	    for i, p in enumerate(alice_strategy):
	        print(f"  Lineup1 - {Lineup_2[i]}: {p:.2f}")
	    for j, q in enumerate(bob_strategy):
	        print(f"  Lineup2 - {Lineup_1[j]}: {q:.2f}")
	    # Expected payoffs
	    a_payoff = alice_strategy @ Lineup_1_payoffs_for_bans @ bob_strategy
	    b_payoff = alice_strategy @ Lineup_2_payoffs_for_bans @ bob_strategy
	    print(f"  Expected payoff: Lineup1 = {a_payoff:.2f}, Lineup2 = {b_payoff:.2f}\n")		
	    avg_winrate += a_payoff / 2

print("")
print(f"Average payoff between play/draw for Lineup 1: {avg_winrate:.2f}")
		