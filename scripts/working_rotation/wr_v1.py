

from pulp import *
import numpy as np
import pandas as pd


## creating a dummy rotation to test out the model

idx = [1, 2,3,4,5,6]
d = {'channel': pd.Series(['Player1', 'Player2', 'Player3','Player4','Player5','Player6'], index=idx),
     1: pd.Series([0,0,1,0,0,0], index=idx),
     2: pd.Series([1,0,0,0,0,0], index=idx),
     3: pd.Series([0,1,0,0,0,0], index=idx),
     4: pd.Series([0,0,0,1,0,0], index=idx),
     5: pd.Series([0,0,0,0,0,1], index=idx),
     6: pd.Series([0,0,0,0,1,0], index=idx)}
starting_rotation = pd.DataFrame(d)



idx = [1,2,3,4,5,6]
d2 = {'A-Player': pd.Series(['Player1', 'Player2','Player3','Player4','Player5','Player6'], index=idx),
     'FR': pd.Series([2,3,7,7,2,4], index=idx),
     'BR': pd.Series([7,7,3,4,3,3], index=idx)}

skill_levels = pd.DataFrame(d2)

print skill_levels


###### -----------rotation outline----------"
######  p4	p3	p2"
######  p5	p6	p1"
###### --------------------------------------"



###########################


## this function finds where all the players are in a given rotation

def player_court_position(rotation, dict):
	for i in range(1,7):
		for j in range(1,7):
			if rotation.lookup([i],[j]) == 1:
				### this is saying, for example, that player 1 is at the p1 spot
				dict[i] = j


########################


### this function does the skill lookup for each player


def skill_lookup(rotation, dict_name):
	for key in rotation.iteritems():
		#print "this is the player number"
		#print key[0]
		#print "this is the player position"
		#print key[1]

		#### essentially, if the player position is 4 or 3 or 2, do a lookup on that playernumber in the FR column
		#### if the player number is 1,6 or 5 then do a player lookup in the BR column in player values
		if key[1] == 1:
			location = "BR"
		if key[1] == 6:
			location = "BR"
		if key[1] == 5:
			location = "BR"
		if key[1] == 4:
			location = "FR"
		if key[1] == 3:
			location = "FR"
		if key[1] == 2:	
			location = "FR"
		skill_at_spot = skill_levels.lookup([key[0]],[location])
		
		dict_name[key[0]] = skill_at_spot[0]

###############33


	### round 1

R1 = {}
player_court_position(starting_rotation,R1)

print "we find where each player currently starts on the floor"
print "note this is player/location"
print R1

print "now we need to find what each player's skill is at that level"
print "note this is player/skill"

R1_skill = {}

skill_lookup(R1,R1_skill)

print R1_skill












