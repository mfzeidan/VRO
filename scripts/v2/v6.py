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
p1_BR = 10
p1_setter = 0

p2_name = "Mark2"
p2_FR = 10
p2_BR = 1
p2_setter = 0

p3_name =  "Mark3"
p3_FR = 1
p3_BR = 2
p3_setter = 0

p4_name =  "Mark4"
p4_FR = 1
p4_BR = 1
p4_setter = 1

p5_name =  "Mark5"
p5_FR = 1
p5_BR = 1
p5_setter = 0

p6_name =  "Mark6"
p6_FR = 1
p6_BR = 1
p6_setter = 1


names = [p1_name,p2_name,p3_name,p4_name,p5_name,p6_name]
FR_skills = [p1_FR,p2_FR,p3_FR,p4_FR,p5_FR,p6_FR]
BR_skills = [p1_BR,p2_BR,p3_BR,p4_BR,p5_BR,p5_BR]
setters = [p1_setter,p2_setter,p3_setter,p4_setter,p5_setter,p6_setter]

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
     'BR': pd.Series(BR_skills, index=idx),
     'setter': pd.Series(setters, index=idx),					}

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

print "#####----------####"
print FR_FINAL
print BR_FINAL

print "FR: 4:3:2"
print "BR: 5:6:1"





full_initial_rotation = FR_FINAL + BR_FINAL

full_initial_rotation_names = []








for p_number in full_initial_rotation:
	full_initial_rotation_names.append(names[p_number-1])



print "initial rotation"
print full_initial_rotation_names

###### going to create a function here that creates a dict that stores players by their spot on the court
## the layout will be player_name =  player number,floor_spot


def complete_rotation(pulp_rotation):

	complete_dict = {}

	#print "HERE IS THE INITIAL ROTATION THAT PULP MAKES"
	player_index_location = 0
	for player_name in pulp_rotation:
		#print "each players info"
		#print player_name ##name
		#print player_index_location ### spot in rotation
		
		

		### find what index this player name is in our name list


	
	#lets find this players index in our list
		#print "SPOT IN NAME INDEX"
		name_index = names.index(player_name) ##spot in name list


		#complete_dict[player_name]= [names.index(player_name),player_index_location]

		complete_dict[player_name] = {}

		print complete_dict

		complete_dict[player_name]["player_Name_Index"]= [name_index][0]


		name_index = names.index(player_name)
		#print "NAME INDEX"
		#print name_index

		complete_dict[player_name]["rotation_Spot"] = [player_index_location][0]

		setter_var = skill_levels.lookup([name_index + 1],["setter"])[0]

		complete_dict[player_name]["setter_Flag"] = setter_var

		#print "setter variable here"
		#print setter_var

		player_index_location +=1
	#print full_initial_rotation_names
	print "layout for this dict is name = spot in name index/rotation spot"
	pp.pprint(complete_dict)

	find_setters(complete_dict)


### find where the setters are


	


def find_setters(overall_dict):
	BR_set_list = []
	FR_set_list = []

	for x,y in overall_dict.iteritems():


		r_spot = y['rotation_Spot']
		p_name_index = y['player_Name_Index']
		setter_flag = y['setter_Flag']

		if setter_flag == 1:
			
			if r_spot > 2:
				BR_set_list.append(x)
			else:
				FR_set_list.append(x)

	print BR_set_list
	print FR_set_list

	move_setters(BR_set_list,FR_set_list,overall_dict)


### this function prints out the final rotation to the webpage
def visualize_rotation(new_dict):
	### lets make a small dict that we'll use to story player name and rotation spot on floor
	viz_rotation = {}
	for x,y in new_dict.iteritems():
		viz_rotation[x] = y['rotation_Spot']
	print viz_rotation
	sorted_rotation = sorted(viz_rotation.items(),key=operator.itemgetter(1))

	FR_FINAL = [sorted_rotation[0][0],sorted_rotation[1][0],sorted_rotation[2][0]]
	BR_FINAL = [sorted_rotation[3][0],sorted_rotation[4][0],sorted_rotation[5][0]]

	print FR_FINAL
	print BR_FINAL

	print "<br>"
	print "<center><h1>"
	print "----------------"
	print "<br>"
	print FR_FINAL[0]


	print FR_FINAL[1]

	print FR_FINAL[2]

	print "</h1></center>"


	print "<br>"
	print "<center><h1>"
	print BR_FINAL[0]


	print BR_FINAL[1]


	print BR_FINAL[2]

	print "</h1></center>"


def setters_in_br_and_fr(br,fr,overall_dict):

	#### lets find where the setter is in the back row (this is the sticky setter)
	back_row_setter_sticky = br[0]
	front_row_setter_moves = fr[0]
	for name,y in overall_dict.iteritems():
		if name == back_row_setter_sticky:
			BR_sticky_spot = y['rotation_Spot']

	print BR_sticky_spot

	#### before we move everyone around, we need to find 2 things
	#### 1 - where is the FR setter
	#### 2 - where does the FR setter nede to move with

	

	for name,y in overall_dict.iteritems():
		if name == front_row_setter_moves:
			FR_setter_spot = y['rotation_Spot']

	print "who is the FR setter"
	print front_row_setter_moves
	print "where is the FR setter"
	print FR_setter_spot

	### now lets find out where the FR setter needs to go, based on where the setter in the BR is
	
	if BR_sticky_spot == 3:
	###FR setter needs to be in the 2
		print "backrow setter is currently in the 3 spot"
		print "this means that the FR setter needs to be in the 2 spot"

		### first lets check if the FR setter is already there
		if FR_setter_spot == 2:
			print "the rotation is set and we are good to go"
		else:
			print "we need to move some peices around"


		### first lets find whos in the 2 spot
			for name,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 2:
					FR_hitter_name = name
					print FR_hitter_name + " must switch with " + front_row_setter_moves + " in the front row"

		### ther person in the 2 spot needs to switch with where the FR setter is
	
			for name,y in overall_dict.iteritems():
				if name == FR_hitter_name:
					y['rotation_Spot'] = FR_setter_spot
				if name == front_row_setter_moves:
					y['rotation_Spot'] = 2

		#pp.pprint(overall_dict)
		visualize_rotation(overall_dict)
	if BR_sticky_spot == 4:
	### FR setter needs to be in the 1
		print "backrow setter is currently in the 4 spot"
		print "this means that the FR setter needs to be in the 1 spot"

		### first lets check if the FR setter is already there
		if FR_setter_spot == 1:
			print "the rotation is set and we are good to go"
		else:
			print "we need to move some peices around"


		### first lets find whos in the 1 spot
			for name,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 1:
					FR_hitter_name = name
					print FR_hitter_name + " must switch with " + front_row_setter_moves + " in the front row"

		### ther person in the 1 spot needs to switch with where the FR setter is
	
			for name,y in overall_dict.iteritems():
				if name == FR_hitter_name:
					y['rotation_Spot'] = FR_setter_spot
				if name == front_row_setter_moves:
					y['rotation_Spot'] = 1
		#pp.pprint(overall_dict)
		visualize_rotation(overall_dict)


		

		



	if BR_sticky_spot == 5:
	#### FR setter needs to be in the 0
		print "backrow setter is currently in the 5 spot"
		print "this means that the FR setter needs to be in the 0 spot"

		### first lets check if the FR setter is already there
		if FR_setter_spot == 0:
			print "the rotation is set and we are good to go"
		else:
			print "we need to move some peices around"


		### first lets find whos in the 1 spot
			for name,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 0:
					FR_hitter_name = name
					print FR_hitter_name + " must switch with " + front_row_setter_moves + " in the front row"

		### ther person in the 1 spot needs to switch with where the FR setter is
	
			for name,y in overall_dict.iteritems():
				if name == FR_hitter_name:
					y['rotation_Spot'] = FR_setter_spot
				if name == front_row_setter_moves:
					y['rotation_Spot'] = 0
		#pp.pprint(overall_dict)
		visualize_rotation(overall_dict)


	


	



def move_setters(br,fr,overall_dict):
	#print br
	#print fr

####################### 2 BACKROW PORTION OF FUNCTION #####################################
	if len(br) > 1:
		print "two in the BR"
		print br

		BRs_frontrow_skills = {}

	### both setters are in the back row. this means we need to move the better of the two setters FR skillsets into the front row
	### we need to change him with whatever player is opposite of the sticky setter
		for x in br:
			for name,y in overall_dict.iteritems():
				if name == x:
					print name
					setter_name_index =  y['player_Name_Index'] + 1
					FR_skill = skill_levels.lookup([setter_name_index],["FR"])[0]
					print FR_skill
					#print skill_levels
					BRs_frontrow_skills[name] = FR_skill
			print BRs_frontrow_skills

			setter_to_front = max(BRs_frontrow_skills.iteritems(),key=operator.itemgetter(1))[0]

			sticky_setter = min(BRs_frontrow_skills.iteritems(),key=operator.itemgetter(1))[0]
			
			print "setter to move to front is " + setter_to_front
			print "sticky setter is " + sticky_setter


	

		#### now that we know who the sticky setter is, we need to replace the setter we want to move
		#### to the front with the person opposite of the sticky setter
		#### at this point lets try building just a list 

		pp.pprint(overall_dict)

		### lets find where the sticky setter is currently in the rotation

		
		for x,y in overall_dict.iteritems():
			if x == sticky_setter:
				sticky_setter_spot = y['rotation_Spot']

		if sticky_setter_spot == 3:
			print "sticky setter is in the " + str(sticky_setter_spot) + " spot"
			print "this means that the setter to move needs to move to the 2 spot"
			## lets find whos currently in the 2 spot
			for x,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 2:
					FR_to_move_for_setter = x
			print FR_to_move_for_setter + " needs to be replaced with " + setter_to_front

			for x,y in overall_dict.iteritems():
				if x == setter_to_front:
					setter_to_front_spot = y["rotation_Spot"]
				if x == FR_to_move_for_setter:
					FR_to_move_for_setter_spot = y["rotation_Spot"]
					

			### now we need go change the spots in the dictionary
			

			for x,y in overall_dict.iteritems():
				if x == setter_to_front:
					y["rotation_Spot"] = FR_to_move_for_setter_spot
				if x == FR_to_move_for_setter:
					y["rotation_Spot"] = setter_to_front_spot

			print pp.pprint(overall_dict)
			print "test"
			visualize_rotation(overall_dict)

		if sticky_setter_spot == 4:
			print "sticky setter is in the " + str(sticky_setter_spot) + " spot"
			print "this means that the setter to move needs to move to the 1 spot"
			## lets find whos currently in the 1 spot
			for x,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 1:
					FR_to_move_for_setter = x
			print FR_to_move_for_setter + " needs to be replaced with " + setter_to_front

			for x,y in overall_dict.iteritems():
				if x == setter_to_front:
					setter_to_front_spot = y["rotation_Spot"]
				if x == FR_to_move_for_setter:
					FR_to_move_for_setter_spot = y["rotation_Spot"]
					

			### now we need go change the spots in the dictionary
			

			for x,y in overall_dict.iteritems():
				if x == setter_to_front:
					y["rotation_Spot"] = FR_to_move_for_setter_spot
				if x == FR_to_move_for_setter:
					y["rotation_Spot"] = setter_to_front_spot

			print pp.pprint(overall_dict)
			print "test"
			visualize_rotation(overall_dict)
			


		if sticky_setter_spot == 5:
			print "sticky setter is in the " + str(sticky_setter_spot) + " spot"
			print "this means that the setter to move needs to move to the 0 spot"
			## lets find whos currently in the 2 spot
			for x,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 0:
					FR_to_move_for_setter = x
			print FR_to_move_for_setter + " needs to be replaced with " + setter_to_front

			for x,y in overall_dict.iteritems():
				if x == setter_to_front:
					setter_to_front_spot = y["rotation_Spot"]
				if x == FR_to_move_for_setter:
					FR_to_move_for_setter_spot = y["rotation_Spot"]
					

			### now we need go change the spots in the dictionary
			

			for x,y in overall_dict.iteritems():
				if x == setter_to_front:
					y["rotation_Spot"] = FR_to_move_for_setter_spot
				if x == FR_to_move_for_setter:
					y["rotation_Spot"] = setter_to_front_spot

			print pp.pprint(overall_dict)
			print "test"
			visualize_rotation(overall_dict)


####################### 2 FRONTROW PORTION OF FUNCTION #####################################
	if len(fr) > 1:
		print "TWO IN THE FRONT ROW :)"
		print "two in the frontrow"

		print fr

		FRs_backrow_skills = {}

	### both setters are in the back row. this means we need to move the better of the two setters FR skillsets into the front row
	### we need to change him with whatever player is opposite of the sticky setter
		for x in fr:
			for name,y in overall_dict.iteritems():
				if name == x:
					print name
					setter_name_index =  y['player_Name_Index'] + 1
					BR_skill = skill_levels.lookup([setter_name_index],["BR"])[0]
					print BR_skill
					#print skill_levels
					FRs_backrow_skills[name] = BR_skill
			print FRs_backrow_skills

			setter_to_back = max(FRs_backrow_skills.iteritems(),key=operator.itemgetter(1))[0]

			sticky_setter = min(FRs_backrow_skills.iteritems(),key=operator.itemgetter(1))[0]
			
			print "setter to move to back is " + setter_to_back
			print "sticky setter is " + sticky_setter


	

		#### now that we know who the sticky setter is, we need to replace the setter we want to move
		#### to the front with the person opposite of the sticky setter
		#### at this point lets try building just a list 

		#pp.pprint(overall_dict)

		### lets find where the sticky setter is currently in the rotation

		
		for x,y in overall_dict.iteritems():
			if x == sticky_setter:
				sticky_setter_spot = y['rotation_Spot']

		if sticky_setter_spot == 0:
			print "sticky setter is in the " + str(sticky_setter_spot) + " spot"
			print "this means that the setter to move needs to move to the 5 spot"
			## lets find whos currently in the 5 spot
			for x,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 5:
					BR_to_move_for_setter = x
			#print BR_to_move_for_setter + " needs to be replaced with " + setter_to_back

			for x,y in overall_dict.iteritems():
				if x == setter_to_back:
					setter_to_back_spot = y["rotation_Spot"]
				if x == BR_to_move_for_setter:
					BR_to_move_for_setter_spot = y["rotation_Spot"]
					

			### now we need go change the spots in the dictionary
			

			for x,y in overall_dict.iteritems():
				if x == setter_to_back:
					y["rotation_Spot"] = BR_to_move_for_setter_spot
				if x == BR_to_move_for_setter:
					y["rotation_Spot"] = setter_to_back_spot

			#print pp.pprint(overall_dict)
			#print "test"
			visualize_rotation(overall_dict)

		if sticky_setter_spot == 1:
			print "sticky setter is in the " + str(sticky_setter_spot) + " spot"
			print "this means that the setter to move needs to move to the 4 spot"
			## lets find whos currently in the 4 spot
			for x,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 4:
					BR_to_move_for_setter = x
			#print BR_to_move_for_setter + " needs to be replaced with " + setter_to_back

			for x,y in overall_dict.iteritems():
				if x == setter_to_back:
					setter_to_back_spot = y["rotation_Spot"]
				if x == BR_to_move_for_setter:
					BR_to_move_for_setter_spot = y["rotation_Spot"]
					

			### now we need go change the spots in the dictionary
			

			for x,y in overall_dict.iteritems():
				if x == setter_to_back:
					y["rotation_Spot"] = BR_to_move_for_setter_spot
				if x == BR_to_move_for_setter:
					y["rotation_Spot"] = setter_to_back_spot

			#print pp.pprint(overall_dict)
			#print "test"
			visualize_rotation(overall_dict)
			


		if sticky_setter_spot == 2:
			print "sticky setter is in the " + str(sticky_setter_spot) + " spot"
			print "this means that the setter to move needs to move to the 5 spot"
			## lets find whos currently in the 3 spot
			for x,y in overall_dict.iteritems():
				if y['rotation_Spot'] == 3:
					BR_to_move_for_setter = x
			#print BR_to_move_for_setter + " needs to be replaced with " + setter_to_back

			for x,y in overall_dict.iteritems():
				if x == setter_to_back:
					setter_to_back_spot = y["rotation_Spot"]
				if x == BR_to_move_for_setter:
					BR_to_move_for_setter_spot = y["rotation_Spot"]
					

			### now we need go change the spots in the dictionary
			

			for x,y in overall_dict.iteritems():
				if x == setter_to_back:
					y["rotation_Spot"] = BR_to_move_for_setter_spot
				if x == BR_to_move_for_setter:
					y["rotation_Spot"] = setter_to_back_spot

			#print pp.pprint(overall_dict)
			#print "test"
			visualize_rotation(overall_dict)
####### IF THERE IS ONE SETTER IN THE FRONT AND ONE IN THE BACK ###########
	if len(fr) == 1:
		setters_in_br_and_fr(br,fr,overall_dict)

	


complete_rotation(full_initial_rotation_names)






#### lets find out where the setters are in relation to their position on the court










