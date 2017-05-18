from pulp import *
import numpy as np
import pandas as pd


def list_looper(list):
	for x in list:
		print x

the_list = [1,2,3]

list_looper(the_list)


index_range = range(1,len(the_list) + 1)

print index_range


n1 = 'mz1'
n2 = 'mz2'
n3 = 'mz3'
n4 = 'mz4'
n5 = 'mz5'
n6 = 'mz6'

list_of_names = [n1,n2,n3,n4,n5,n6]

FR_list = [3,3,4,5,6,1] 

BR_list = [4,5,2,1,2,3]

def build_player_skills_df(namelist,fr,br):
	name1 = namelist[0:1]
	name2 = namelist[1:2]
	name3 = namelist[2:3]
	name4 = namelist[3:4]
	name5 = namelist[4:5]
	name6 = namelist[5:6]

	FR1 = fr[0:1]
	FR2 = fr[1:2]
	FR3 = fr[2:3]
	FR4 = fr[3:4]
	FR5 = fr[4:5]
	FR6 = fr[5:6]

	BR1 = br[0:1]
	BR2 = br[1:2]
	BR3 = br[2:3]
	BR4 = br[3:4]
	BR5 = br[4:5]
	BR6 = br[5:6]





	idx = [1,2,3,4,5,6]
	d2 = {'A-Player': pd.Series([name1[0],name2[0],name3[0],name4[0],name5[0],name6[0]], index=idx),
     'FR': pd.Series([FR1[0],FR2[0],FR3[0],FR4[0],FR5[0],FR6[0]], index=idx),
     'BR': pd.Series([BR1[0],BR2[0],BR3[0],BR4[0],BR5[0],BR6[0]], index=idx)}

	skill_levels = pd.DataFrame(d2)
	print skill_levels


print "-------"

build_player_skills_df(list_of_names,FR_list,BR_list)
