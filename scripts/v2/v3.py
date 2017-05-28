#!/usr/bin/env python
import json

import sys
from pulp import *
import numpy as np
import pandas as pd
import operator


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
p1_BR = 4
p1_setter = 1

p2_name = "Mark2"
p2_FR = 1
p2_BR = 4
p2_setter = 0

p3_name =  "Mark3"
p3_FR = 3
p3_BR = 5
p3_setter = 1

p4_name =  "Mark4"
p4_FR = 5
p4_BR = 1
p4_setter = 0

p5_name =  "Mark5"
p5_FR = 5
p5_BR = 1
p5_setter = 0

p6_name =  "Mark6"
p6_FR = 5
p6_BR = 1
p6_setter = 0


names = [p1_name,p2_name,p3_name,p4_name,p5_name,p6_name]
FR_skills = [p1_FR,p2_FR,p3_FR,p4_FR,p5_FR,p6_FR]
BR_skills = [p1_BR,p2_BR,p3_BR,p4_BR,p5_BR,p5_BR]

#print names
#print FR_skills
#print BR_skills



FR_x1=LpVariable("FRP1",0,1,LpInteger) ## 0 is the lowerbound, 1 is the upper bound. Only way I know to set up binary variables
FR_x2=LpVariable("FRP2",0,1,LpInteger)
FR_x3=LpVariable("FRP3",0,1,LpInteger)
FR_x4=LpVariable("FRP4",0,1,LpInteger)
FR_x5=LpVariable("FRP5",0,1,LpInteger)
FR_x6=LpVariable("FRP6",0,1,LpInteger)


BR_x1=LpVariable("BRP1",0,1,LpInteger)
BR_x2=LpVariable("BRP2",0,1,LpInteger)
BR_x3=LpVariable("BRP3",0,1,LpInteger)
BR_x4=LpVariable("BRP4",0,1,LpInteger)
BR_x5=LpVariable("BRP5",0,1,LpInteger)
BR_x6=LpVariable("BRP6",0,1,LpInteger)

idx = [1, 2,3,4,5,6]
d3 = {'A-Player': pd.Series(['Player1','Player2','Player3','Player4','Player5','Player6'], index=idx),
     'FR': pd.Series([FR_x1,FR_x2,FR_x3,FR_x4,FR_x5,FR_x6], index=idx),
     'BR': pd.Series([BR_x1,BR_x2,BR_x3,BR_x4,BR_x5,BR_x6], index=idx),
}

small_rotation = pd.DataFrame(d3)


idx = [1,2,3,4,5,6]
d2 = {'A-Player': pd.Series(names, index=idx),
     'FR': pd.Series(FR_skills, index=idx),
     'BR': pd.Series(BR_skills, index=idx)}

skill_levels = pd.DataFrame(d2)






#adding a total column to help with setting up restraints

small_rotation['total'] = small_rotation.sum(axis=1)


# #adding a total variable for the columns to make sure that a player can only be 1 or the other


# #these variables are used for the constraints at the end of the script
BackRow_Total = small_rotation['BR'].sum()
FrontRow_Total = small_rotation['FR'].sum()


# #here is where I need to do a lookup with the dataframes to player values


skill_level_sub = skill_levels[['BR','FR']]

small_rotation_sub = small_rotation[['BR','FR']]


rotation_totals = skill_level_sub * small_rotation_sub

rotation_totals['totals'] = rotation_totals.sum(axis=1)



# ###these are the 2 variables to calculate how much value is in the backrow and front row
BackRow_Total_rotation = rotation_totals['BR'].sum()
FrontRow_Total_rotation = rotation_totals['FR'].sum()

# ## combine the two values and that is what we're trying to maximize
total_rotation_value = BackRow_Total_rotation + FrontRow_Total_rotation





vball_model += total_rotation_value


vball_model += FR_x1 + FR_x2 + FR_x3 + FR_x4 + FR_x5 + FR_x6 == 3
vball_model += BR_x1 + BR_x2+ BR_x3+ BR_x4+ BR_x5+ BR_x6 == 3
vball_model += FR_x1 + BR_x1 == 1
vball_model += FR_x2 + BR_x2 == 1
vball_model += FR_x3 + BR_x3 == 1
vball_model += FR_x4 + BR_x4 == 1
vball_model += FR_x5 + BR_x5 == 1
vball_model += FR_x6 + BR_x6 == 1

#vball_model.writeLP("vball.lp")


vball_model.solve()

#print("Status:", LpStatus[vball_model.status])


#for v in vball_model.variables():
 #   print(v.name, "=", v.varValue)
# print "---------------"


starting_list_FR = []
starting_list_BR = []

for v in vball_model.variables():
    	#print(v.name, "=", v.varValue)
	if v.varValue ==1:
		if "FR" in v.name:
			starting_list_FR.append(v.name[2:4])
		if "BR" in v.name:
			starting_list_BR.append(v.name[2:4])







FR_br_skillset_dict = {}

for x in starting_list_FR:
	num = int(x[1:2])
	#print "player #" + str(x)
	SL = skill_levels.lookup([num],["BR"])[0]
	FR_br_skillset_dict[num]=SL




#### now we do it for the backrow


BR_fr_skillset_dict = {}

for x in starting_list_BR:
	num = int(x[1:2])
	#print "player #" + str(x)
	SL = skill_levels.lookup([num],["FR"])[0]
	BR_fr_skillset_dict[num]=SL





### the player in the BR with the best FR skillset will start in the 5 spot
### the player in the FR with the best BR skillset will start in the 2 spot


#### FR: 4:3:2
#### BR: 5:6:1


## find the player to start in the 5 spot


#print BR_fr_skillset_dict
five_spot = max(BR_fr_skillset_dict.iteritems(),key=operator.itemgetter(1))[0]



BR_fr_skillset_dict.pop(five_spot)


two_spot = max(FR_br_skillset_dict.iteritems(),key=operator.itemgetter(1))[0]


FR_br_skillset_dict.pop(two_spot)

p6 = 0
p1 = 0

BR_Counter = 0
for players in BR_fr_skillset_dict.keys():
	if BR_Counter == 0:
		p6 = players
		BR_Counter += 1
	if BR_Counter == 1:
		p1 = players



BR_FINAL = [five_spot,p6,p1]




p4 = 0
p3 = 0

FR_Counter = 0
for players in FR_br_skillset_dict.keys():
	if FR_Counter == 0:
		p4 = players
		FR_Counter += 1
	if FR_Counter == 1:
		p3 = players

FR_FINAL = [p4,p3,two_spot]




setters = {p1_name: p1_setter,p2_name:p2_setter,p3_name:p3_setter,p4_name:p4_setter,p5_name:p5_setter,p6_name:p6_setter}




print "FR: 4:3:2"
print "BR: 5:6:1"

print "HERE IS THE INITIAL ROTATION THAT PULP MAKES"



full_initial_rotation = [names[five_spot-1],names[p6-1],names[p1-1],names[p4-1],names[p3-1],names[two_spot-1]]
print full_initial_rotation	

print "----------------------------------"

rotation_setters_initial = {names[five_spot-1]:setters[names[five_spot-1]],names[p6-1]:setters[names[p6-1]],names[p1-1]:setters[names[p1-1]],names[p4-1]:setters[names[p4-1]],names[p3-1]:setters[names[p3-1]],names[two_spot-1]:setters[names[two_spot-1]]}


### lets loop through the setter dict above and find out where each setter is starting




###### write a function that moves the setters around


def setter_construction(initial_rotation):

	setter_counter = 0
	
	mini_set_dict = {}


	### find out where both setters are
	for key,value in initial_rotation.iteritems():
		setter_counter += 1
		#print(key,value)
		if value == 1:
			#### note that we are adding the values to the dictionary on a 1-6 counter, not the proper vball rotation counter
			#### so if the setter dict is values 4 and 6, that actually means the setters are starting in the 5 and 1 spot

			#print key
			#print setter_counter

			mini_set_dict[key] = setter_counter

	### now the function needs to declare where both setters are

	print mini_set_dict


	BR_set_list = []
	FR_set_list = []


	for key,value in mini_set_dict.iteritems():
		if value > 3:
			BR_set_list.append(value)
		else:
			FR_set_list.append(value)

	print BR_set_list
	print len(BR_set_list)

	print FR_set_list
	print len(FR_set_list)	


	

	### lets figure out what name is what index in the pandas df
	#print "finding range here"

	name_list = {}
	for x in range(1,7):
		new_name = skill_levels.lookup([x],["A-Player"])[0]
		name_list[new_name] = x


	#print name_list


	####if both setters are in BR

	if len(BR_set_list) > 1:
		print "both setters in BR"

		#print initial_rotation

		BR_setters_FR_skill = {}
		for key,value in initial_rotation.iteritems():
			if value == 1:
				## key gives me the setters names
				#print "player name"
				#print key

				#print "player number within the player list"
				#print name_list[key]
				#print name_list[key]


				### now that we found the player name and their respective position in the skill levels dataframe, we can look up their FR skills

				#print "this is each setters FR skill level"
				BR_skill = skill_levels.lookup([name_list[key]],["FR"])[0]
				BR_setters_FR_skill[key] = BR_skill



		print "remember we are looking to see which BR setter is better in the FR"
		print BR_setters_FR_skill

		#### this will need to be fixed if both setters have equal skillsets

		better_FR = max(BR_setters_FR_skill.iteritems(), key=operator.itemgetter(1))[0]
		worse_FR_setter = min(BR_setters_FR_skill.iteritems(), key=operator.itemgetter(1))[0]


		### this is the player of the 2 setters that is better in the FR
		print "new function"
		print BR_setters_FR_skill

		for key, value in BR_setters_FR_skill.iteritems() :
			print key, value

		two_BR_setters(better_FR,worse_FR_setter)





	#### if this is the case, lets do a lookup on each setters FR skillset


	




	if len(FR_set_list) > 1:
		print "both setters in FR"


def two_BR_setters(which_setter,sticky_setter):
	print "this setter moves opposite of the stickey setter"
	print which_setter
	print rotation_setters_initial
	print full_initial_rotation
	print "this is the sticky setter"
	print sticky_setter
	### at this point we need to figure out where the setter that is staying in the backrow is in the rotation


	### note the difference between the vball numbers and the index numbers
		##FR: 4:3:2"
		##BR: 5:6:1"


	### index
		##fr: 0,1,2
		##br: 3,4,5

	dont_move_setter = full_initial_rotation.index(sticky_setter)


	print "DONT MOVE SETTER NUMBER HERE"
	print dont_move_setter

	

	### since we are dealing with 2 backrow setters, we can make the assumption that there are 3 possibilities for the rotation setup
	## if the sticky setter is in 5 (index wise), then the new setter must move to 0
	## else if 4, then 1
	## else if 3, 2

	if dont_move_setter == 5:
		# if the sticky setter is in 5, lets swap the other setter with the player in the 0 spot in the list index
		print "sticky in 5 spot"
		print "this is the setter that moves"
		#lets find where this setter is in the starting lineup
		print which_setter

		where_is_moving_setter = full_initial_rotation[full_initial_rotation.index(which_setter)]
		print where_is_moving_setter
		#now find the player that you gotta move
		
		player_to_switch = full_initial_rotation[2]
		print player_to_switch


		a, b = full_initial_rotation.index(which_setter), full_initial_rotation.index(player_to_switch)

		full_initial_rotation[b], full_initial_rotation[a] = full_initial_rotation[a], full_initial_rotation[b]

		print full_initial_rotation

	if dont_move_setter == 4:
		# if the sticky setter is in 5, lets swap the other setter with the player in the 0 spot in the list index
		print "sticky in 5 spot"
		print "this is the setter that moves"
		#lets find where this setter is in the starting lineup
		print which_setter

		where_is_moving_setter = full_initial_rotation[full_initial_rotation.index(which_setter)]
		print where_is_moving_setter
		#now find the player that you gotta move
		
		player_to_switch = full_initial_rotation[1]
		print player_to_switch


		a, b = full_initial_rotation.index(which_setter), full_initial_rotation.index(player_to_switch)

		full_initial_rotation[b], full_initial_rotation[a] = full_initial_rotation[a], full_initial_rotation[b]

		print full_initial_rotation

	if dont_move_setter == 3:
		# if the sticky setter is in 5, lets swap the other setter with the player in the 0 spot in the list index
		print "sticky in 5 spot"
		print "this is the setter that moves"
		#lets find where this setter is in the starting lineup
		print which_setter

		where_is_moving_setter = full_initial_rotation[full_initial_rotation.index(which_setter)]
		print where_is_moving_setter
		#now find the player that you gotta move
		
		player_to_switch = full_initial_rotation[0]
		print player_to_switch


		a, b = full_initial_rotation.index(which_setter), full_initial_rotation.index(player_to_switch)

		full_initial_rotation[b], full_initial_rotation[a] = full_initial_rotation[a], full_initial_rotation[b]

		print full_initial_rotation

		
		
	

	

setter_construction(rotation_setters_initial)





#print rotation_setters_initial

# print "<br>"
# print "<center><h1>"
# print "----------------"
# print "<br>"
# print names[five_spot-1]
# print setters[names[five_spot-1]]

# print names[p6-1]
# print setters[names[p6-1]]

# print names[p1-1]
# print setters[names[p1-1]]
# print "</h1></center>"


# print "<br>"
# print "<center><h1>"
# print names[p4-1]
# print setters[names[p4-1]]

# print names[p3-1]
# print setters[names[p3-1]]

# print names[two_spot-1]
# print setters[names[two_spot-1]]

# print "</h1></center>"


