#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : author-paper-author.py
#
# Purpose : create a path of author-paper-author
#
# Creation Date : 18-09-2013
#
# Last Modified : Wed 18 Sep 2013 11:06:16 AM CDT
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

def author_paper_author(year):
    length = {}
    length['paper'] = 463348
    length['author'] = 323675
    length['org'] = 314185
   
    paper_author = coo_matrix((length['paper'], length['author'])) 
    
    data = []
    row = []
    column = []
    
    data_f = open("../../network/" + str(year) + "/paper_author")
    fout = open("../../network/" + str(year) + "/author_paper_author", "w")

    for line in data_f:
        value = line.split("\n")[0].split("\t")
        pid = int(value[0]) 
        aid = int(value[1]) 
        row.append(pid) 
        column.append(aid) 
        data.append(1.0)
    
    paper_author = coo_matrix((data, (row, column))).tocsr()
    APA = paper_author.T * paper_author 
    
    rows = APA.nonzero()[0]
    cols = APA.nonzero()[1]
    
    for i in range(len(cols)):
        r = rows[i]
        c = cols[i]
   #     print r, c, APA[r, c]     
        fout.write(str(r) + "\t" + str(c) + "\t" + str(APA[r, c]) + "\n")
    
    fout.close() 
    
if __name__ == "__main__":
    author_paper_author(1893)
        
    
