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
p1_BR = 0
p1_setter = 1

p2_name = "Mark2"
p2_FR = 1
p2_BR = 0
p2_setter = 0

p3_name =  "Mark3"
p3_FR = 1
p3_BR = 0
p3_setter = 1

p4_name =  "Mark4"
p4_FR = 0
p4_BR = 1
p4_setter = 0

p5_name =  "Mark5"
p5_FR = 0
p5_BR = 1
p5_setter = 0

p6_name =  "Mark6"
p6_FR = 0
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
d2 = {'A-Player': pd.Series(['Player1', 'Player2','Player3','Player4','Player5','Player6'], index=idx),
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





rotation_setters_initial = {names[five_spot-1]:setters[names[five_spot-1]],names[p6-1]:setters[names[p6-1]],names[p1-1]:setters[names[p1-1]],names[p4-1]:setters[names[p4-1]],names[p3-1]:setters[names[p3-1]],names[two_spot-1]:setters[names[two_spot-1]]}


print rotation_setters_initial

print "<br>"
print "<center><h1>"
print "----------------"
print "<br>"
print names[five_spot-1]
print setters[names[five_spot-1]]

print names[p6-1]
print setters[names[p6-1]]

print names[p1-1]
print setters[names[p1-1]]
print "</h1></center>"


print "<br>"
print "<center><h1>"
print names[p4-1]
print setters[names[p4-1]]

print names[p3-1]
print setters[names[p3-1]]

print names[two_spot-1]
print setters[names[two_spot-1]]

print "</h1></center>"


