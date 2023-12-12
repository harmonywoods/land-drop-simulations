'''
MULLIGAN RULE:
• A 7-card hand is kept if it has 2, 3, 4, or 5 lands. 
• For a mulligan to 6, we first choose what to put on the bottom and decide keep or mull afterwards. 
	To get a good mix, we bottom the most expensive spell if we drew 3+ spells and we bottom a land if we drew 5+ lands. 	
	Afterwards, we keep if we hold 2, 3, or 4 lands. Otherwise, we mulligan.
• For a mulligan to 5, we try to get close to 3 lands and 2 spells. 
	So we bottom two spells (the most expensive ones) if we drew 4+ spells, we bottom a spell and a land if we drew 3 spells, and we bottom two lands if we drew 2 spells. 
	Afterwards, we keep if we have 2, 3, or 4 lands; otherwise, we mulligan.
• For a mulligan to 4, we try to get close to 3 lands and 1 spell. Then we always keep.
'''

'''
Modified version of a script publicly available on Karsten's github - https://github.com/frankkarsten/MTG-Math/blob/master/NumberLandsProbCalc.py

Outputs to the terminal the following data (in CSV format, for each combination of deck size, number of lands, and turn number specified
deck size, number of lands, turn number, P(success|play), P(success|draw), P(success), expected hand size, chance of keeping a 4-card hand, chance of keeping a 5 card hand, chance of keeping a 6 card hand, chance of keeping a 7 card hand

where success is hitting your land drops up to and including the turn number in column 2

'''
import random
import collections 
import statistics 
from quartiles import quartiles

def run_one_sim(decklist, lands_wanted, onPlay):	
	'''
	Runs a simulation of the mulligan process
	Takes:
	lands_wanted: the turn that you care about
	onPlay: True if wished to be on the play in the simulation, False if not.
	Returns the turn that land drop is hit.
	'''
	#Initialize variables
	lands_in_play = 0
	keephand = False 
	kept_hand_size = None;
	for hand_size in [7, 6, 5, 4]:
		#We may mull 7, 6, or 5 cards and keep every 4-card hand
		#Once we actually keep, the variable keephand will be set to True
		if not keephand:
			
			#Construct library as a list
			library = []
			for card in decklist.keys():
				library += [card] * decklist[card]
			random.shuffle(library)

			#Construct a random opening hand
			hand = {
				'Spell': 0,
				'Land': 0
			}
			for _ in range(7):
				card_drawn = library.pop(0)
				hand[card_drawn] += 1

			if hand_size == 7:
				#Do we keep?
				if (hand['Land'] >= 2 and hand['Land'] <= 5):
					keephand = True
					kept_hand_size = 7

			if hand_size == 6:
				#We have to bottom. Ideal would be 4 land, 2 spells
				if hand['Spell'] > 2:
					hand['Spell'] -= 1
				else:
					#The hand has 0, 1, or 2 spells so we put a land on the bottom
					hand['Land'] -= 1
				#Do we keep?
				if (hand['Land'] >= 2 and hand['Land'] <= 4):
					keephand = True
					kept_hand_size = 6

			if hand_size == 5:
				#We have to bottom. Ideal would be 3 land, 2 spells
				if hand['Spell'] > 3:
					#Two spells on the bottom
					hand['Spell'] -= 2
				elif hand['Spell'] == 3:
					#One land, one spell on the bottom
					hand['Land'] -= 1
					hand['Spell'] -= 1
				else:
					#The hand has 0, 1, or 2 spells so we put two land on the bottom
					hand['Land'] -= 2
				#Do we keep?
				if (hand['Land'] >= 2 and hand['Land'] <= 4):
					keephand = True
					kept_hand_size = 5

			if hand_size == 4:
				#We have to bottom. Ideal would be 3 land, 1 spell
				if hand['Spell'] > 3:
					#Three spells on the bottom
					hand['Spell'] -= 3
				elif hand['Spell'] == 3:
					#One land, two spell on the bottom
					hand['Land'] -= 1
					hand['Spell'] -= 2
				elif hand['Spell'] == 2:
					#Two land, one spell on the bottom
					hand['Land'] -= 2
					hand['Spell'] -= 1
				else:
					#The hand has 0 or 1 spell so we put three land on the bottom
					hand['Land'] -= 3
				#Do we keep?
				keephand = True
				kept_hand_size = 4
	turn = 0 
	while lands_in_play < lands_wanted:
		turn += 1
		draw_a_card = True if (not onPlay) or (turn > 1) else False
		if (draw_a_card):
			if(len(library)==0):
				print('decked')
				break
			card_drawn = library.pop(0)
			hand[card_drawn] += 1

		if (hand['Land'] > 0):
			hand['Land'] -= 1
			lands_in_play += 1
	return turn


num_simulations = 5000000 # for actual runs
#num_simulations=50 # for quick testing
print(num_simulations)
#Uncertainty with five million simulations will be about +/- 0.03% (Karsten gave this number specifically for the chance of hitting land drops - no idea about what the equivalent is for mulligans etc)
land_drops_of_interest = range(1,8)
for land_drop in land_drops_of_interest:
	for deck_size in [40]:
		#print("===> We now consider decks of size " + str(deck_size) + " playing land drops for " + str(turn_num) + " turn(s).")
		land_set = {
			40: range(13,20),
			60: range(21,31),
			80: range(27,41),
			99: range(34,52)
		}
		for num_lands in land_set[deck_size]:
			play_turn_land_drop_made_list = []
			draw_turn_land_drop_made_list = []
			deck = {
				'Spell': deck_size - num_lands,
				'Land': num_lands
			}
			for _ in range(0,num_simulations):
				play_turn_land_drop_made_list.append(run_one_sim(deck,land_drop,True))
				draw_turn_land_drop_made_list.append(run_one_sim(deck,land_drop,False))
			turn_land_drop_made_list = play_turn_land_drop_made_list + draw_turn_land_drop_made_list
			print(f'Total,{deck_size},{num_lands},{land_drop},{','.join(map(str,quartiles(turn_land_drop_made_list)))}')
			print(f'Play,{deck_size},{num_lands},{land_drop},{','.join(map(str,quartiles(play_turn_land_drop_made_list)))}')
			print(f'Draw,{deck_size},{num_lands},{land_drop},{','.join(map(str,quartiles(draw_turn_land_drop_made_list)))}')