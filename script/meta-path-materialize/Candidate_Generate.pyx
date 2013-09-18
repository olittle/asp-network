#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Candidate_Generate.pyx
#
# Purpose : Generate Candidate
#
# Creation Date : 27-01-2013
#
# Last Modified : Wed 18 Sep 2013 02:08:20 PM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu)
#
#_._._._._._._._._._._._._._._._._._._._._.

from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
import numpy as np
import sets
import sys
import os
from copy import copy

def C_Gen(year):

    candidate = set() 

    data = open("../../network/" + str(year) + "/paper_author")

    for line in data:
        value = line.split("\n")[0].split("\t")[1]
        candidate.add(int(value))

    return candidate 

