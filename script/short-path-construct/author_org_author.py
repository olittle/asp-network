#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : author-org-author.py
#
# Purpose :
#
# Creation Date : 18-09-2013
#
# Last Modified : Wed 18 Sep 2013 11:06:08 AM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from scipy.sparse import *
import numpy as np
import sets
import sys
import os
import math
import gzip

def author_org_author(year):
    length = {}
    length['paper'] = 463348
    length['author'] = 323675
    length['org'] = 314185
    
    Map = {}
    data = open("../../rawdata/org_map")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        org_1 = int(value[0]) 
        org_2 = int(value[1]) 
        Map[org_1] = org_2 
   
    data = []
    row = []
    column = []
    
    data_f = open("../../network/" + str(year) + "/author_organ")
    fout = open("../../network/" + str(year) + "/author_organ_author", "w")

    for line in data_f:
        value = line.split("\n")[0].split("\t")
        aid = int(value[0]) 
        oid = int(value[1])
        if oid in Map:
            oid = Map[oid] 
        row.append(aid) 
        column.append(oid) 
        data.append(1.0)
    
    author_org = coo_matrix((data, (row, column))).tocsr()
    AOA = author_org * author_org.T
    
    rows = AOA.nonzero()[0]
    cols = AOA.nonzero()[1]
    
    for i in range(len(cols)):
        r = rows[i]
        c = cols[i]
#        print r, c, AOA[r, c]     
        fout.write(str(r) + "\t" + str(c) + "\t" + str(AOA[r, c]) + "\n")
    
    fout.close() 
    
if __name__ == "__main__":
    author_org_author(1893)
        



