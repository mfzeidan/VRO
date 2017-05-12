

import pulp
import numpy as np
import pandas as pd


idx = [1, 2,3,4,5,6]
d = {'channel': pd.Series(['Player1', 'Player2', 'Player3','Player4','Player5','Player6'], index=idx),
     'p1': pd.Series([0,0,0,0,0,0], index=idx),
     'p6': pd.Series([0,0,0,0,0,0], index=idx),
     'p5': pd.Series([0,0,0,0,0,0], index=idx),
     'p4': pd.Series([0,0,0,0,0,0], index=idx),
     'p3': pd.Series([0,0,0,0,0,0], index=idx),
     'p2': pd.Series([0,0,0,0,0,0], index=idx)}
full_rotation = pd.DataFrame(d)




idx = [1, 2]
d3 = {'A-Player': pd.Series(['Player1', 'Player2'], index=idx),
     'FR': pd.Series([0,0], index=idx),
     'BR': pd.Series([0,0], index=idx),
}
small_rotation = pd.DataFrame(d3)




idx = [1, 2]
d2 = {'A-Player': pd.Series(['Player1', 'Player2'], index=idx),
     'FR': pd.Series([2,3], index=idx),
     'BR': pd.Series([5,3], index=idx)}

skill_levels = pd.DataFrame(d2)



#adding a total column to help with setting up restraints

small_rotation['total'] = small_rotation.sum(axis=1)


#adding a total variable for the columns to make sure that a player can only be 1 or the other

BackRow_Total = small_rotation['BR'].sum()
FrontRow_Total = small_rotation['FR'].sum()


#here is where I need to do a lookup with the dataframes to player values


skill_level_sub = skill_levels[['BR','FR']]

small_rotation_sub = small_rotation[['BR','FR']]


rotation_totals = skill_level_sub * small_rotation_sub

rotation_totals['totals'] = rotation_totals.sum(axis=1)




BackRow_Total_rotation = rotation_totals['BR'].sum()
FrontRow_Total_rotation = rotation_totals['FR'].sum()


total_rotation_value = BackRow_Total_rotation + FrontRow_Total_rotation





#constraints to be added
# each row in small_rotation total's column must be one

# BackRow_Total must equal 1

#print BackRow_Total

# FrontRow_Total must equal 1

#print FrontRow_Total

# maximze total_rotation_value

#print total_rotation_value


## create the prob variable to contain the problem data

vball_model = pulp.LpProblem("marks first attempt",pulp.LpMaximize)


vball_model += total_rotation_value
vball_model += sum(BackRow_Total) <= 1
