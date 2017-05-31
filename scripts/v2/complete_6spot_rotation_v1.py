#!/usr/bin/env python
import json

import sys
from pulp import *
import numpy as np
import pandas as pd
import operator
import pprint

pp = pprint.PrettyPrinter(indent=4)

####	4/3/2	
####	5/6/1


##### CURRENT HURISTICS BEING SET IN THE PROBLEM SO FAR
#
# Of the 3 players that will start in the backrow, the best FR of the Backrow starts in 5
# Of the 3 players in the front row, the best backrow player will start in the 2
#
# ### being implemented in this script
#	The 2 setters will start opposite of each other 
#		If the package sets 2 setters in the BR. the code moves the better of the (FR skillset) setter into the front
#		Same goes if 2 start in the FR, code will move the better of the BR skillset setter into the back
#		They then will be set as complete opposites on the court


vball_model = pulp.LpProblem("marks first attempt",pulp.LpMaximize)

#data = sys.argv[1]

#data = '{"p1": "apple","sport":"football"}'
#data2  = json.loads(data)

#listy = json.dumps(data)

key_list = []





p1_name =  "Mark1"
p1_FR = 1
p1_BR = 1
p1_setter = 0

p2_name = "Mark2"
p2_FR = 2
p2_BR = 2
p2_setter = 0

p3_name =  "Mark3"
p3_FR = 3
p3_BR = 3
p3_setter = 0

p4_name =  "Mark4"
p4_FR = 4
p4_BR = 4
p4_setter = 0

p5_name =  "Mark5"
p5_FR = 5
p5_BR = 5
p5_setter = 1

p6_name =  "Mark6"
p6_FR = 6
p6_BR = 6
p6_setter = 1


names = [p1_name,p2_name,p3_name,p4_name,p5_name,p6_name]
FR_skills = [p1_FR,p2_FR,p3_FR,p4_FR,p5_FR,p6_FR]
BR_skills = [p1_BR,p2_BR,p3_BR,p4_BR,p5_BR,p6_BR]
setters = [p1_setter,p2_setter,p3_setter,p4_setter,p5_setter,p6_setter]

#print names
#print FR_skills
#print BR_skills



BR_x1_1=LpVariable("BRP1_1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
BR_x1_2=LpVariable("BRP1_2",0,1,LpInteger)
BR_x1_3=LpVariable("BRP1_3",0,1,LpInteger)
BR_x1_4=LpVariable("BRP1_4",0,1,LpInteger)
BR_x1_5=LpVariable("BRP1_5",0,1,LpInteger)
BR_x1_6=LpVariable("BRP1_6",0,1,LpInteger)

BR_x5_1=LpVariable("BRP5_1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
BR_x5_2=LpVariable("BRP5_2",0,1,LpInteger)
BR_x5_3=LpVariable("BRP5_3",0,1,LpInteger)
BR_x5_4=LpVariable("BRP5_4",0,1,LpInteger)
BR_x5_5=LpVariable("BRP5_5",0,1,LpInteger)
BR_x5_6=LpVariable("BRP5_6",0,1,LpInteger)

BR_x6_1=LpVariable("BRP6_1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
BR_x6_2=LpVariable("BRP6_2",0,1,LpInteger)
BR_x6_3=LpVariable("BRP6_3",0,1,LpInteger)
BR_x6_4=LpVariable("BRP6_4",0,1,LpInteger)
BR_x6_5=LpVariable("BRP6_5",0,1,LpInteger)
BR_x6_6=LpVariable("BRP6_6",0,1,LpInteger)


FR_x2_1=LpVariable("FRP2_1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
FR_x2_2=LpVariable("FRP2_2",0,1,LpInteger)
FR_x2_3=LpVariable("FRP2_3",0,1,LpInteger)
FR_x2_4=LpVariable("FRP2_4",0,1,LpInteger)
FR_x2_5=LpVariable("FRP2_5",0,1,LpInteger)
FR_x2_6=LpVariable("FRP2_6",0,1,LpInteger)
FR_x3_1=LpVariable("FRP3_1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
FR_x3_2=LpVariable("FRP3_2",0,1,LpInteger)
FR_x3_3=LpVariable("FRP3_3",0,1,LpInteger)
FR_x3_4=LpVariable("FRP3_4",0,1,LpInteger)
FR_x3_5=LpVariable("FRP3_5",0,1,LpInteger)
FR_x3_6=LpVariable("FRP3_6",0,1,LpInteger)
FR_x4_1=LpVariable("FRP4_1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
FR_x4_2=LpVariable("FRP4_2",0,1,LpInteger)
FR_x4_3=LpVariable("FRP4_3",0,1,LpInteger)
FR_x4_4=LpVariable("FRP4_4",0,1,LpInteger)
FR_x4_5=LpVariable("FRP4_5",0,1,LpInteger)
FR_x4_6=LpVariable("FRP4_6",0,1,LpInteger)


idx = [1,2,3,4,5,6]
d2 = {'A-Player': pd.Series(names, index=idx),
     'FR': pd.Series(FR_skills, index=idx),
     'BR': pd.Series(BR_skills, index=idx),
     'setter': pd.Series(setters, index=idx),					}

skill_levels = pd.DataFrame(d2)



#print small_rotation

#print skill_levels

def expounded_skills(df):
	overall_skills = []

	for player in range(1,7):
		player_list = []
		for spot in range(1,7):
			#print "PLAYER"
			#print player
			#print "SPOT"
			#print spot
			if spot == 1 or spot == 5 or spot == 6:
				#print df.lookup([player],["BR"])[0]
				player_list.append(df.lookup([player],["BR"])[0])


			elif spot == 2 or spot == 3 or spot == 4:
				#print df.lookup([player],["FR"])[0]
				player_list.append(df.lookup([player],["FR"])[0])
			#print len(player_list)
			if len(player_list) == 6:
				#print player_list
				overall_skills.append(player_list)
	
	return overall_skills


skill_list_2 = expounded_skills(skill_levels)




def transverse_list(list):
	transversed_list = []
	for step_1 in range(0,6):
		step_1_list = []
		for step_2 in range(0,6):
			step_1_list.append(list[step_2][step_1])
			if step_2 == 5:
				transversed_list.append(step_1_list)

	return transversed_list
trans_list = transverse_list(skill_list_2)




#print skill_list_2[0][0]

FR_x2_1,FR_x2_2,FR_x2_3,FR_x2_4,FR_x2_5,FR_x2_6
FR_x3_1,FR_x3_2,FR_x3_3,FR_x3_4,FR_x3_5,FR_x3_6
FR_x4_1,FR_x4_2,FR_x4_3,FR_x4_4,FR_x4_5,FR_x4_6

#print mark_1_expounded_skills

idx = [1,2,3,4,5,6]
d4 = {'A-Player': pd.Series(names, index=idx),
     'p1': pd.Series([BR_x1_1,BR_x1_2,BR_x1_3,BR_x1_4,BR_x1_5,BR_x1_6], index=idx),
     'p2': pd.Series([FR_x2_1,FR_x2_2,FR_x2_3,FR_x2_4,FR_x2_5,FR_x2_6], index=idx),
     'p3': pd.Series([FR_x3_1,FR_x3_2,FR_x3_3,FR_x3_4,FR_x3_5,FR_x3_6], index=idx),
     'p4': pd.Series([FR_x4_1,FR_x4_2,FR_x4_3,FR_x4_4,FR_x4_5,FR_x4_6], index=idx),
     'p5': pd.Series([BR_x5_1,BR_x5_2,BR_x5_3,BR_x5_4,BR_x5_5,BR_x5_6], index=idx),
     'p6': pd.Series([BR_x6_1,BR_x6_2,BR_x6_3,BR_x6_4,BR_x6_5,BR_x6_6], index=idx),
}

big_rotation = pd.DataFrame(d4)

idx = [1, 2,3,4,5,6]
d5 = {'A-Player': pd.Series(names, index=idx),
     'p1': pd.Series(trans_list[0], index=idx),
     'p2': pd.Series(trans_list[1], index=idx),
     'p3': pd.Series(trans_list[2], index=idx),
     'p4': pd.Series(trans_list[3], index=idx),
     'p5': pd.Series(trans_list[4], index=idx),
     'p6': pd.Series(trans_list[5], index=idx),
}

big_skills = pd.DataFrame(d5)


print big_rotation
print big_skills



p1_rot = big_rotation['p1']
p1_skills = big_skills['p1']

p2_rot =big_rotation['p2']
p2_skills =big_skills['p2']

p3_rot =big_rotation['p3']
p3_skills =big_skills['p3']

p4_rot =big_rotation['p4']
p4_skills =big_skills['p4']

p5_rot =big_rotation['p5']
p5_skills =big_skills['p5']

p6_rot = big_rotation['p6']
p6_skills = big_skills['p6']


rotation_total = np.dot(big_rotation['p1'],big_skills['p1']) + np.dot(big_rotation['p2'],big_skills['p2']) + np.dot(big_rotation['p3'],big_skills['p3'])+np.dot(big_rotation['p4'],big_skills['p4'])+np.dot(big_rotation['p5'],big_skills['p5'])+np.dot(big_rotation['p6'],big_skills['p6']) 	

print rotation_total




vball_model += rotation_total


vball_model += BR_x1_1 + BR_x1_2 + BR_x1_3 + BR_x1_4 + BR_x1_5 + BR_x1_6 == 1
vball_model += BR_x5_1 + BR_x5_2 + BR_x5_3 + BR_x5_4 + BR_x5_5 + BR_x5_6 == 1
vball_model += BR_x6_1 + BR_x6_2 + BR_x6_3 + BR_x6_4 + BR_x6_5 + BR_x6_6 == 1

vball_model += BR_x1_6 + BR_x5_6 + BR_x6_6 <= 1
vball_model += BR_x1_5 + BR_x5_5 + BR_x6_5 <= 1
vball_model += BR_x1_4 + BR_x5_4 + BR_x6_4 <= 1
vball_model += BR_x1_3 + BR_x5_3 + BR_x6_3 <= 1
vball_model += BR_x1_2 + BR_x5_2 + BR_x6_2 <= 1
vball_model += BR_x1_1 + BR_x5_1 + BR_x6_1 <= 1

vball_model += FR_x2_1 + FR_x2_2 + FR_x2_3 + FR_x2_4 + FR_x2_5 + FR_x2_6 == 1
vball_model += FR_x3_1 + FR_x3_2 + FR_x3_3 + FR_x3_4 + FR_x3_5 + FR_x3_6 == 1
vball_model += FR_x4_1 + FR_x4_2 + FR_x4_3 + FR_x4_4 + FR_x4_5 + FR_x4_6 == 1
vball_model += FR_x2_6 + FR_x3_6 + FR_x4_6 <= 1
vball_model += FR_x2_5 + FR_x3_5 + FR_x4_5 <= 1
vball_model += FR_x2_4 + FR_x3_4 + FR_x4_4 <= 1
vball_model += FR_x2_3 + FR_x3_3 + FR_x4_3 <= 1
vball_model += FR_x2_2 + FR_x3_2 + FR_x4_2 <= 1
vball_model += FR_x2_1 + FR_x3_1 + FR_x4_1 <= 1

vball_model += BR_x1_1 + FR_x2_1 + FR_x3_1 + FR_x4_1 + BR_x5_1 + BR_x6_1 == 1
vball_model += BR_x1_2 + FR_x2_2 + FR_x3_2 + FR_x4_2 + BR_x5_2 + BR_x6_2 == 1
vball_model += BR_x1_3 + FR_x2_3 + FR_x3_3 + FR_x4_3 + BR_x5_3 + BR_x6_3 == 1
vball_model += BR_x1_4 + FR_x2_4 + FR_x3_4 + FR_x4_4 + BR_x5_4 + BR_x6_4 == 1
vball_model += BR_x1_5 + FR_x2_5 + FR_x3_5 + FR_x4_5 + BR_x5_5 + BR_x6_5 == 1
vball_model += BR_x1_6 + FR_x2_6 + FR_x3_6 + FR_x4_6 + BR_x5_6 + BR_x6_6 == 1

# #vball_model.writeLP("vball.lp")


vball_model.solve()

initial_rotation_dict = {}

print("Status:", LpStatus[vball_model.status])
for v in vball_model.variables():
	if v.varValue == 1:
		#print v.name
		### player index
		player_index = v.name[3]
		### player spot
		player_spot = v.name[5]
		initial_rotation_dict[int(player_index)] = int(player_spot)

print "player name index/players spot"
print initial_rotation_dict

sorted_rotation = sorted(initial_rotation_dict.items(), key=operator.itemgetter(1))
### need to move the tuple list thing created above to just list of lists
sorted_rotation_list = []

for x in sorted_rotation:
	sorted_rotation_list.append(list(x))

print sorted_rotation_list


### check for where setters are

def find_setters(rotation):

	FR_setter = []
	BR_setter = []

	for x in rotation:
		#print names[x[0]-1]
		#print x	
		if skill_levels.lookup([x[0]],["setter"])[0] == 1:
			print names[x[0]-1]
			print x[1]
			#now lets find out where each player is on the court
			if x[1] >= 4:
				#BR_setter.append(names[x[0]-1])
				BR_setter.append(x[0])
			if x[1] < 4:
				#FR_setter.append(names[x[0]-1])
				FR_setter.append(x[0])
	#print FR_setter
	#print BR_setter


	#### lets decide here where both setters are
	#### we will create a seperate function for each potential outcome

	if len(FR_setter) == 1:
		print "1 setter in front, one in back"
		final_rot = mixed_setters(FR_setter,BR_setter)
		return final_rot
		
	if len(FR_setter) == 2:
		print "2 fr setters"
		two_fr_setters(FR_setter)
	if len(BR_setter) == 2:
		print "2 backrow setters"
		two_fr_setters(BR_setters)


def two_fr_setters(fr_Setters):
	#### if there are 2 setters in the front row, we move the worse of the 2 FR players to the back
	print fr_Setters
	setter_FR_skillset = {}
	for setter in fr_Setters:
		
		setter_FR_skillset[setter] = skill_levels.lookup([setter],["FR"])[0]
	print setter_FR_skillset

	### find out which setter is worse of the 2
	moving_setter = min(setter_FR_skillset.iteritems(),key=operator.itemgetter(1))[0]
	print moving_setter

	for player_info in sorted_rotation_list:
		if player_info[0] == moving_setter:
			moving_setter_spot = player_info[1]
	
	### we need to find out where the "sticky setter" is
	sticky_setter = max(setter_FR_skillset.iteritems(),key=operator.itemgetter(1))[0]

	for player_info in sorted_rotation_list:
		if player_info[0] == sticky_setter:
			sticky_setter_spot = player_info[1]

	if sticky_setter_spot == 1:
		# if the sticky setter is in the 1 we need to move the other setter to the 4 spot
		# lets make the player in the 4 spot go to where the moving setter is
		for player_info in sorted_rotation_list:
			if player_info[1] == 4:
				player_info[1] = sticky_setter_spot

		for player_info in sorted_rotation_list:
			if player_info[0] == moving_setter:
				player_info[1] = 4

	if sticky_setter_spot == 2:
		# if the sticky setter is in the 2 we need to move the other setter to the 5 spot
		# lets make the player in the 5 spot go to where the moving setter is
		for player_info in sorted_rotation_list:
			if player_info[1] == 5:
				player_info[1] = sticky_setter_spot

		for player_info in sorted_rotation_list:
			if player_info[0] == moving_setter:
				player_info[1] = 5

	if sticky_setter_spot == 3:
		# if the sticky setter is in the 3 we need to move the other setter to the 6 spot
		# lets make the player in the 6 spot go to where the moving setter is
		for player_info in sorted_rotation_list:
			if player_info[1] == 6:
				player_info[1] = sticky_setter_spot

		for player_info in sorted_rotation_list:
			if player_info[0] == moving_setter:
				player_info[1] = 6
	print sorted_rotation_list


		

def two_br_setters(br_Setters):
	#### if there are 2 setters in the back row, we move the worse of the 2 BR players to the front
	print br_Setters
	setter_BR_skillset = {}
	for setter in br_Setters:
		
		setter_BR_skillset[setter] = skill_levels.lookup([setter],["BR"])[0]
	print setter_FR_skillset

	### find out which setter is worse of the 2
	moving_setter = min(setter_BR_skillset.iteritems(),key=operator.itemgetter(1))[0]
	print moving_setter

	for player_info in sorted_rotation_list:
		if player_info[0] == moving_setter:
			moving_setter_spot = player_info[1]
	
	### we need to find out where the "sticky setter" is
	sticky_setter = max(setter_FR_skillset.iteritems(),key=operator.itemgetter(1))[0]

	for player_info in sorted_rotation_list:
		if player_info[0] == sticky_setter:
			sticky_setter_spot = player_info[1]

	if sticky_setter_spot == 4:
		# if the sticky setter is in the 4 we need to move the other setter to the 1 spot
		# lets make the player in the 1 spot go to where the moving setter is
		for player_info in sorted_rotation_list:
			if player_info[1] == 1:
				player_info[1] = sticky_setter_spot

		for player_info in sorted_rotation_list:
			if player_info[0] == moving_setter:
				player_info[1] = 1

	if sticky_setter_spot == 5:
		# if the sticky setter is in the 2 we need to move the other setter to the 5 spot
		# lets make the player in the 5 spot go to where the moving setter is
		for player_info in sorted_rotation_list:
			if player_info[1] == 2:
				player_info[1] = sticky_setter_spot

		for player_info in sorted_rotation_list:
			if player_info[0] == moving_setter:
				player_info[1] = 2

	if sticky_setter_spot == 6:
		# if the sticky setter is in the 3 we need to move the other setter to the 6 spot
		# lets make the player in the 6 spot go to where the moving setter is
		for player_info in sorted_rotation_list:
			if player_info[1] == 3:
				player_info[1] = sticky_setter_spot

		for player_info in sorted_rotation_list:
			if player_info[0] == moving_setter:
				player_info[1] = 3
	print sorted_rotation_list


def mixed_setters(fr_Setter,br_Setter):
	### if there is one in the front and one in the back, we move the front player to align with the backrow setter
	### that is, the backrow setter is considered "sticky"

	### note that the players "name index" is what is in the list. We will use this to find out where the players are on the court
	print fr_Setter[0]
	print br_Setter[0]
	print "player name index/players spot"
	print sorted_rotation_list

	####lets find where the BR setter is to figure out where to move the FR setter within the FR
	for player_info in sorted_rotation:
		 if player_info[0] == br_Setter[0]:
			print player_info
			BR_setter_rotation_spot = player_info[1]

	if BR_setter_rotation_spot == 4:
		print "we need to move the FR setter to the 3 spot"
		### now lets check where the FR setter is

		for player_info in sorted_rotation_list:
			if player_info[0] == fr_Setter[0]:
				print "match found"
				print player_info
				FR_setter_rotation_spot = player_info[1]
		#print FR_setter_rotation_spot
		if FR_setter_rotation_spot == 3:
			print "rotation is already set, we can stop here"
			final_rotation = sorted_rotation_list
			return final_rotation
		
		else:
			print "rotation needs to be adjusted and the setter needs to be moved to the 3 spot"
			### before we do this we need to move whoever is in the 3 spot to wherever the FR setter is

			for player_info in sorted_rotation_list:
				## this is to find out where the FR setter is
				if player_info[0] == fr_Setter[0]:
					FR_setter_spot = player_info[1]


			### find the player that needs to move and move him to where the FR setter is
			for player_info in sorted_rotation_list:
				if player_info[1] == 3:
					player_info[1] = FR_setter_spot

			for player_info in sorted_rotation_list:
				if player_info[0] == fr_Setter[0]:
					player_info[1] = 3
			final_rotation = sorted_rotation_list
			return final_rotation



	if BR_setter_rotation_spot == 5:
		print "we need to move the FR setter to the 2 spot"
		### now lets check where the FR setter is

		for player_info in sorted_rotation_list:
			if player_info[0] == fr_Setter[0]:
				print "match found"
				print player_info
				FR_setter_rotation_spot = player_info[1]
		#print FR_setter_rotation_spot
		if FR_setter_rotation_spot == 2:
			print "rotation is already set, we can stop here"
			final_rotation = sorted_rotation_list
			return final_rotation
		
		else:
			print "rotation needs to be adjusted and the setter needs to be moved to the 2 spot"
			### before we do this we need to move whoever is in the 2 spot to wherever the FR setter is

			for player_info in sorted_rotation_list:
				## this is to find out where the FR setter is
				if player_info[0] == fr_Setter[0]:
					FR_setter_spot = player_info[1]
					print FR_setter_spot


			### find the player that needs to move and move him to where the FR setter is
			for player_info in sorted_rotation_list:
				if player_info[1] == 2:
					player_info[1] = FR_setter_spot
			print sorted_rotation_list

			for player_info in sorted_rotation_list:
				if player_info[0] == fr_Setter[0]:
					player_info[1] = 2
			final_rotation = sorted_rotation_list
			return final_rotation
		



	if BR_setter_rotation_spot == 6:
		print "we need to move the FR setter to the 1 spot"
		### now lets check where the FR setter is

		for player_info in sorted_rotation_list:
			if player_info[0] == fr_Setter[0]:
				print "match found"
				print player_info
				FR_setter_rotation_spot = player_info[1]
		#print FR_setter_rotation_spot
		if FR_setter_rotation_spot == 1:
			print "rotation is already set, we can stop here"
			final_rotation = sorted_rotation_list
			return final_rotation
		
		else:
			print "rotation needs to be adjusted and the setter needs to be moved to the 3 spot"
			### before we do this we need to move whoever is in the 3 spot to wherever the FR setter is

			for player_info in sorted_rotation_list:
				## this is to find out where the FR setter is
				if player_info[0] == fr_Setter[0]:
					FR_setter_spot = player_info[1]


			### find the player that needs to move and move him to where the FR setter is
			for player_info in sorted_rotation_list:
				if player_info[1] == 1:
					player_info[1] = FR_setter_spot

			for player_info in sorted_rotation_list:
				if player_info[0] == fr_Setter[0]:
					player_info[1] = 1
			final_rotation = sorted_rotation_list
			return final_rotation

find_setters(sorted_rotation)

#final_info = find_setters(sorted_rotation)
# print "-----"
# print final_info
# ###

# final_rotation = {}

# for x in final_info:
	# final_rotation[x[0]] = x[1]

# print final_rotation


	
# sorted_final_rotation = sorted(final_rotation.items(), key=operator.itemgetter(1))

# rotation_list_2 = []

# for tup in sorted_final_rotation:
	# rotation_list_2.append(tup[0])
# print rotation_list_2

# ### 4 spot / 0 spot
# print names[rotation_list_2[0]-1]

# ### 3 spot / 1 spot
# print names[rotation_list_2[1]-1]

# ### 2 spot / 2 spot
# print names[rotation_list_2[2]-1]

# ### 5 spot / 3 spot
# print names[rotation_list_2[3]-1]

# ### 6 spot / 4 spot
# print names[rotation_list_2[4]-1]

# ### 1 spot / 5 spot
# print names[rotation_list_2[5]-1]

# # print "---------------"
