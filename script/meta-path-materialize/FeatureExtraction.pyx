#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : FeatureExtraction.pyx
#
# Purpose : Extract Feature
#
# Creation Date : 27-01-2013
#
# Last Modified : Wed 18 Sep 2013 04:12:23 PM CDT
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

def Ftr_Ext(Train_Candidate, year):

    out_folder = "../../data-metapath-materialize/" + str(year + 1) + "/"
    os.system("mkdir " + out_folder) 
    data_folder = "../../network/"

    YearInterval = 3
    LoopS = year - YearInterval
    LoopE = year  
    
    length = {}
    length['paper'] = 463348
    length['author'] = 323675
    length['org'] = 314185

    AXN = {}
    AXNT = {}
    for year1 in range(LoopS, LoopE):
        AXfile = data_folder + str(year1) + "/author_paper_author"
        AXfin = open(AXfile)
        ai = year1 - LoopS
        row = []
        col = []
        data = []

        for lines in AXfin:
            value = lines.split("\n")[0].split("\t")
            a1 = int(value[0])
            a2 = int(value[1])
            s = float(value[2])
            row.append(a1)
            col.append(a2) 
            data.append(s) 
        AXN[ai] = coo_matrix((data, (row, col)), (length['author'], length['author'])).tocsr()
        AXNT[ai] = coo_matrix((data, (col, row)), (length['author'], length['author'])).tocsr()


    fout = open(out_folder +  "APAPA.txt", "w")

    for author in Train_Candidate:
        for i in range( YearInterval):
            SAX = AXN[i].getrow(author)
            SAX = csr_matrix(SAX)
            if i == 0:
                SAAN = SAX * AXNT[i]
            else:
                SAAN_1 = SAAN + SAX * AXNT[i]
                SAAN = SAAN_1

        inf_aut = SAAN.nonzero()[1]
        for i in inf_aut:
            fout.write(str(author) + "\t" + str(i) + "\t" + str(SAAN[0, i]) + "\n")
    fout.close()

    return 0
