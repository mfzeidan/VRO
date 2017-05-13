



from pulp import *
import numpy as np
import pandas as pd


vball_model = pulp.LpProblem("marks first attempt",pulp.LpMaximize)


###todo - future goal is to get entire rotation working

idx = [1, 2,3,4,5,6]
d = {'channel': pd.Series(['Player1', 'Player2', 'Player3','Player4','Player5','Player6'], index=idx),
     1: pd.Series([1,0,0,0,0,0], index=idx),
     2: pd.Series([0,1,0,0,0,0], index=idx),
     3: pd.Series([0,0,1,0,0,0], index=idx),
     4: pd.Series([0,0,0,1,0,0], index=idx),
     5: pd.Series([0,0,0,0,1,0], index=idx),
     6: pd.Series([0,0,0,0,0,1], index=idx)}
full_rotation = pd.DataFrame(d)

print full_rotation


idx = [1,2,3,4,5,6]
d2 = {'A-Player': pd.Series(['Player1', 'Player2','Player3','Player4','Player5','Player6'], index=idx),
     'FR': pd.Series([2,3,7,7,2,4], index=idx),
     'BR': pd.Series([7,7,3,4,3,3], index=idx)}

skill_levels = pd.DataFrame(d2)

print skill_levels


print "------------rotation outline----------"
print " p4	p3	p2"
print " p5	p6	p1"
print "--------------------------------------"

### now for each player, lets see where they are on the court

###looking up first row, first column
FR_player1_p1_lookup = full_rotation.lookup([1],[1])



player_location = {}

for i in range(1,7):
	for j in range(1,7):
		if full_rotation.lookup([i],[j]) == 1:
			### this is saying, for example, that player 1 is at the p1 spot
			player_location[i] = j

print player_location

### 4,3,2 are all front row spots

### 1, 6, and 5 are all backrow lookups


###this loop collects each players current skillset at each spot

r1_skill = {}

for key in player_location.iteritems():
	print "this is the player number"
	print key[0]
	print "this is the player position"
	print key[1]

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
	
	r1_skill[key[0]] = skill_at_spot[0]


#### this is the total skills for the entire rotation
### if we go through this dict and sum each value, that's the total value of this rotation

print r1_skill




### 4, 3, and 2 are all front row lookups









##### with this we need to find out what each player's skill level is for their respective spots





