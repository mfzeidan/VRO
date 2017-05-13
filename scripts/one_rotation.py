

from pulp import *
import numpy as np
import pandas as pd


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
FR_x7=LpVariable("FRP7",0,1,LpInteger)

BR_x1=LpVariable("BRP1",0,1,LpInteger)
BR_x2=LpVariable("BRP2",0,1,LpInteger)
BR_x3=LpVariable("BRP3",0,1,LpInteger)
BR_x4=LpVariable("BRP4",0,1,LpInteger)
BR_x5=LpVariable("BRP5",0,1,LpInteger)
BR_x6=LpVariable("BRP6",0,1,LpInteger)
BR_x7=LpVariable("BRP7",0,1,LpInteger)
##################################################################################################

#### HERE IS WHERE WE BUILD THE ROTATION SKELETON ########

##################################################################################################


idx = [1, 2,3,4,5,6,7]
d3 = {'A-Player': pd.Series(['Player1','Player2','Player3','Player4','Player5','Player6','Player7'], index=idx),
     'FR': pd.Series([FR_x1,FR_x2,FR_x3,FR_x4,FR_x5,FR_x6,FR_x7], index=idx),
     'BR': pd.Series([BR_x1,BR_x2,BR_x3,BR_x4,BR_x5,BR_x6,BR_x7], index=idx),
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

idx = [1,2,3,4,5,6,7]
d2 = {'A-Player': pd.Series(['Player1', 'Player2','Player3','Player4','Player5','Player6','Player7'], index=idx),
     'FR': pd.Series([2,3,7,7,2,4,1], index=idx),
     'BR': pd.Series([7,7,3,4,3,3,1], index=idx)}

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



#################################################


idx = [1, 2,3,4,5,6]
d = {'channel': pd.Series(['Player1', 'Player2', 'Player3','Player4','Player5','Player6'], index=idx),
     'p1': pd.Series([0,0,0,0,0,0], index=idx),
     'p6': pd.Series([0,0,0,0,0,0], index=idx),
     'p5': pd.Series([0,0,0,0,0,0], index=idx),
     'p4': pd.Series([0,0,0,0,0,0], index=idx),
     'p3': pd.Series([0,0,0,0,0,0], index=idx),
     'p2': pd.Series([0,0,0,0,0,0], index=idx)}
full_rotation = pd.DataFrame(d)



print full_rotation







##########################




vball_model += total_rotation_value


vball_model += FR_x1 + FR_x2 + FR_x3 + FR_x4 + FR_x5 + FR_x6+ FR_x7 == 3
vball_model += BR_x1 + BR_x2+ BR_x3+ BR_x4+ BR_x5+ BR_x6+ BR_x7 == 3
vball_model += FR_x1 + BR_x1 <= 1
vball_model += FR_x2 + BR_x2 <= 1
vball_model += FR_x3 + BR_x3 <= 1
vball_model += FR_x4 + BR_x4 <= 1
vball_model += FR_x5 + BR_x5 <= 1
vball_model += FR_x6 + BR_x6 <= 1
vball_model += FR_x7 + BR_x7 <= 1
vball_model.writeLP("vball.lp")


vball_model.solve()

print("Status:", LpStatus[vball_model.status])


rotation_one_list = dict()

for v in vball_model.variables():
	print(v.name, "=", v.varValue)
	rotation_one_list.update({v.name:v.varValue})

print rotation_one_list







#### create a rule that takes out a player in the front row and replaces them with the sub.

### FR must drop a player and add one player from the back row
## the BR must drop a player to the front row and add a player to the backrow

sub_list = []

if rotation_one_list['FRP1'] == 0 and rotation_one_list['BRP1'] == 0:
	sub_list.append('BRP1')
if rotation_one_list['FRP2'] == 0 and rotation_one_list['BRP2'] == 0:
	sub_list.append('BRP2')
if rotation_one_list['FRP3'] == 0 and rotation_one_list['BRP3'] == 0:
	sub_list.append('BRP3')
if rotation_one_list['FRP4'] == 0 and rotation_one_list['BRP4'] == 0:
	sub_list.append('BRP4')
if rotation_one_list['FRP5'] == 0 and rotation_one_list['BRP5'] == 0:
	sub_list.append('BRP5')
if rotation_one_list['FRP6'] == 0 and rotation_one_list['BRP6'] == 0:
	sub_list.append('BRP6')
if rotation_one_list['FRP7'] == 0 and rotation_one_list['BRP7'] == 0:
	sub_list.append('BRP7')


###########  note one of the FR players will need to come out, one BR goes to FR and sub replaces a BR

br_list_r1 = []
fr_list_r1 = []


#### this loop is figuring out whos in FR and whos in the BR for rotation 1


for v in vball_model.variables():
	if v.varValue == 1:
		if "FR" in v.name:
			fr_list_r1.append(v.name)
		if "BR" in v.name:
			br_list_r1.append(v.name)

print br_list_r1
print fr_list_r1


### this person needs to come in

print "this person needs to come in"

print sub_list




print "---------------"
