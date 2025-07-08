Winprob_play = {
	'Deck A': 0.8,
	'Deck B': 0.6,
	'Deck C': 0.5
}

Winprob_draw = {
	'Deck A': 0.2,
	'Deck B': 0.4,
	'Deck C': 0.5
}


list_of_decks = ['Deck A', 'Deck B', 'Deck C']

best_winrates_for_ban = {}
avg_winrate = 0

for die_roll in ['Play first', 'Draw first']:
	print("==========Die roll: ", die_roll)
	
	for deck in list_of_decks:
		best_winrates_for_ban[deck] = 0

	for banned_deck in ['Deck A', 'Deck B', 'Deck C']:
		print("---Opponent banned", banned_deck)
		list_of_decks = ['Deck A', 'Deck B', 'Deck C']
		list_of_decks.remove(banned_deck)
		best_match_win_prob = 0
		best_text = ""
		for first_deck in list_of_decks:
			second_deck = (set(list_of_decks) - {first_deck}).pop()
			for in_case_of_game_1_loss in ['Switch', 'Stay']:
				text = ""
				text += "Best strategy: First deck " + first_deck
				text += ". In case of game 1 loss: " + in_case_of_game_1_loss
				if die_roll == 'Play first':
					WW = Winprob_play[first_deck] * Winprob_draw[second_deck]
					WLW = Winprob_play[first_deck] * (1 - Winprob_draw[second_deck]) * Winprob_play[second_deck]
					if in_case_of_game_1_loss == 'Switch':
						LWW = (1 - Winprob_play[first_deck] ) * Winprob_play[second_deck] * Winprob_draw[first_deck]
					elif in_case_of_game_1_loss == 'Stay':
						LWW = (1 - Winprob_play[first_deck] ) * Winprob_play[first_deck] * Winprob_draw[second_deck]
				if die_roll == 'Draw first':
					WW = Winprob_draw[first_deck] * Winprob_draw[second_deck]
					WLW = Winprob_draw[first_deck] * (1 - Winprob_draw[second_deck]) * Winprob_play[second_deck]
					if in_case_of_game_1_loss == 'Switch':
						LWW = (1 - Winprob_draw[first_deck] ) * Winprob_play[second_deck] * Winprob_draw[first_deck]
					elif in_case_of_game_1_loss == 'Stay':
						LWW = (1 - Winprob_draw[first_deck] ) * Winprob_play[first_deck] * Winprob_draw[second_deck]
				match_win_prob = WW + WLW + LWW
				text += "\nMATCH WIN PROB: " + str(round(match_win_prob, 5))
				if match_win_prob >= best_match_win_prob:
					best_match_win_prob = match_win_prob
					best_text = text
		print(best_text)
		best_winrates_for_ban[banned_deck] = best_match_win_prob

	print("")	
	print("Conclusion when", die_roll)
	if best_winrates_for_ban['Deck A'] <= best_winrates_for_ban['Deck B'] and best_winrates_for_ban['Deck A'] <= best_winrates_for_ban['Deck C']:
		print("Opponent will ban Deck A, giving winrate", best_winrates_for_ban['Deck A'])
		avg_winrate += best_winrates_for_ban['Deck A'] * 0.5
	elif best_winrates_for_ban['Deck B'] <= best_winrates_for_ban['Deck C']:
		print("Opponent will ban Deck B, giving winrate", best_winrates_for_ban['Deck B'])
		avg_winrate += best_winrates_for_ban['Deck B'] * 0.5
	else:
		print("Opponent will ban Deck C, giving winrate", best_winrates_for_ban['Deck C'])
		avg_winrate += best_winrates_for_ban['Deck C'] * 0.5
	print("")	
	
print("")	
print("CONCLUSION OVERALL: Average win rate (play/draw) with this lineup is ", round(avg_winrate,3))
