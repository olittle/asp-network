#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : main.py
#
# Purpose :
#
# Creation Date : 18-09-2013
#
# Last Modified : Wed 18 Sep 2013 11:12:25 AM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from author_org_author import author_org_author
from author_paper_author import author_paper_author
from author_paper_paper_author import author_cite_author
import sys

STARTYEAR = 1893
ENDYEAR = 2009

target = int(sys.argv[1]) 

for year in range(STARTYEAR, ENDYEAR):
    if year % 10 != target:
        continue 
    
    author_org_author(year) 
    author_paper_author(year) 
    author_cite_author(year) 
    

