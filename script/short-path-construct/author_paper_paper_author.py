#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : author-paper-paper-author.py
#
# Purpose : calculate the citation importance 
#
# Creation Date : 18-09-2013
#
# Last Modified : Wed 18 Sep 2013 11:06:02 AM CDT
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

def author_cite_author(year):
    length = {}
    length['paper'] = 463348
    length['author'] = 323675
    length['org'] = 314185
    
    STARTYEAR = 1893
   
    paper_author = coo_matrix((length['paper'], length['author'])) 
    
    fout = open("../../network/" + str(year) + "/author_paper_paper", "w")
    
    
    data = []
    row = []
    column = []
    cited = set() 
    data_f = open("../../network/" + str(year) + "/paper_paper")
    for line in data_f:
        value = line.split("\n")[0].split("\t")
        pid_1 = int(value[0]) 
        pid_2 = int(value[1]) 
        cited.add(pid_2) 
        
        row.append(pid_1) 
        column.append(pid_2) 
        data.append(1.0)
    paper_paper = coo_matrix((data, (row, column)), (length['paper'], length['paper'])).tocsr()
    
    data = []
    row = []
    column = []
    data_f = open("../../network/" + str(year) + "/paper_author")
    for line in data_f:
        value = line.split("\n")[0].split("\t")
        pid = int(value[0])
        if pid not in cited:
            continue 
        aid = int(value[1]) 
        row.append(pid) 
        column.append(aid) 
        data.append(1.0)
        
    paper_author = coo_matrix((data, (row, column)), (length['paper'], length['author'])).tocsr()
    
    data = []
    row = []
    column = []
    for y in range(STARTYEAR, year + 1):
        data_f = open("../../network/" + str(y) + "/paper_author")
        for line in data_f:
            value = line.split("\n")[0].split("\t")
            pid = int(value[0])
            if pid not in cited:
                continue 
            aid = int(value[1]) 
            row.append(pid) 
            column.append(aid) 
            data.append(1.0)
        
    paper_author_cite = coo_matrix((data, (row, column)), (length['paper'], length['author'])).tocsr()
    

    APPA = paper_author.T * paper_paper * paper_author_cite 
    
    rows = APPA.nonzero()[0]
    cols = APPA.nonzero()[1]
    
    for i in range(len(cols)):
        r = rows[i]
        c = cols[i]
#        print r, c, APPA[r, c]     
        fout.write(str(r) + "\t" + str(c) + "\t" + str(APPA[r, c]) + "\n")
    
    fout.close() 
    
if __name__ == "__main__":
    author_cite_author(1934)
        
