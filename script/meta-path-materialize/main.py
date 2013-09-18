#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Meta-path Materialization  
#
# Purpose : Make Multiple Prediction
#
# Creation Date : 27-01-2013
#
# Last Modified : Wed 18 Sep 2013 04:07:41 PM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu)
#
#_._._._._._._._._._._._._._._._._._._._._.

import sys
import os
import copy
from C_Gen import C_Gen
from Ftr_Ext import Ftr_Ext
import numpy as np

data_folder = "../../data/"
out_folder = "../../data-metapath-materialize/"

os.system("mkdir "+out_folder)

target = int(sys.argv[1]) 

for year in range(1970, 2010):
    if year % 10 != target:
        continue
        
    Train_candidate = C_Gen(year)
    print "-- start feature extraction -- ", year 
    Train_Data = Ftr_Ext(Train_candidate, year-1)


