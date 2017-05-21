

from pulp import *
import numpy as np
import pandas as pd
import operator


vball_model = pulp.LpProblem("marks first attempt",pulp.LpMaximize)


###todo - future goal is to get entire rotation working


##################################################################################################

#### HERE IS WHERE WE SET UP OUR VARIABLES TO ALLOW THE SOLVER TO DECIDE WHO'S IN AND OUT ########

##################################################################################################


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
##################################################################################################

#### HERE IS WHERE WE BUILD THE ROTATION SKELETON ########

#note that for now it is only a 2x2 matrix
##################################################################################################


idx = [1, 2,3,4,5,6]
d3 = {'A-Player': pd.Series(['Player1','Player2','Player3','Player4','Player5','Player6'], index=idx),
     'FR': pd.Series([FR_x1,FR_x2,FR_x3,FR_x4,FR_x5,FR_x6], index=idx),
     'BR': pd.Series([BR_x1,BR_x2,BR_x3,BR_x4,BR_x5,BR_x6], index=idx),
}

small_rotation = pd.DataFrame(d3)

## above df looks like this
#  A-Player    BR    FR
#1  Player1  BRP1  FRP1
#2  Player2  BRP2  FRP2

print small_rotation




#####################################################################################

#### THIS IS THE PLAYER VALUE TABLE CREATION PORTION OF THE SCRIPT########

#####################################################################################

idx = [1,2,3,4,5,6]
d2 = {'A-Player': pd.Series(['Player1', 'Player2','Player3','Player4','Player5','Player6'], index=idx),
     'FR': pd.Series([2,3,7,7,2,4], index=idx),
     'BR': pd.Series([7,7,3,4,3,3], index=idx)}

skill_levels = pd.DataFrame(d2)

print skill_levels

#######note this is what the above dataframe will look like
### named the player column "a-Player" because pandas puts the columns in alphabetical order and i wanted it at front

#  A-Player  BR  FR
#1  Player1   5   2
#2  Player2   3   3



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

vball_model.writeLP("vball.lp")


vball_model.solve()

print("Status:", LpStatus[vball_model.status])


for v in vball_model.variables():
    print(v.name, "=", v.varValue)
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

print "FR: "
print starting_list_FR
print "BR: "
print starting_list_BR

print "BR/FR lookups below"


print skill_levels

print "this is each player in the FR respective BR skillset"

FR_br_skillset_dict = {}

for x in starting_list_FR:
	num = int(x[1:2])
	print "player #" + str(x)
	SL = skill_levels.lookup([num],["BR"])[0]
	FR_br_skillset_dict[num]=SL

print "Front Rows BR Skillset Dict"

print FR_br_skillset_dict


#### now we do it for the backrow


BR_fr_skillset_dict = {}

for x in starting_list_BR:
	num = int(x[1:2])
	print "player #" + str(x)
	SL = skill_levels.lookup([num],["FR"])[0]
	BR_fr_skillset_dict[num]=SL

print "Back Rows FR Skillset Dict"
print BR_fr_skillset_dict



### the player in the BR with the best FR skillset will start in the 5 spot
### the player in the FR with the best BR skillset will start in the 2 spot


#### FR: 4:3:2
#### BR: 5:6:1


## find the player to start in the 5 spot

print "player to start in the 5 spot"
#print BR_fr_skillset_dict
five_spot = max(BR_fr_skillset_dict.iteritems(),key=operator.itemgetter(1))[0]

print five_spot

BR_fr_skillset_dict.pop(five_spot)


two_spot = max(FR_br_skillset_dict.iteritems(),key=operator.itemgetter(1))[0]

print two_spot
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

print FR_FINAL
print BR_FINAL

