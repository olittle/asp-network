#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : parser.py
#
# Purpose : parse the xml  
#
# Creation Date : 12-09-2013
#
# Last Modified : Sun 15 Sep 2013 08:54:13 PM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import xml.etree.ElementTree as ET
import sys
import os 

STARTYEAR = 1893
ENDYEAR = 2009

for year in range(STARTYEAR, ENDYEAR + 1):
    os.system("mkdir ../../network/" + str(year)) 


doi_dict = {} 
doi_fout = open("../../rawdata/doi_paper.txt", "w") 

venue_dict = {} 
venue_fout = open("../../rawdata/vernue_name.txt", "w") 
paper_venue = open("../../rawdata/paper_venue.txt", "w") 

author_dict = {} 
author_fout = open("../../rawdata/author_name.txt", "w")
paper_author = open("../../rawdata/paper_author.txt", "w") 


org_dict = {} 
org_fout = open("../../rawdata/org_name", "w") 
author_org = open("../../rawdata/author_org", "w") 
author_check = open("../../rawdata/author_org.check", "w")


#doi_fout_year = {}
paper_venue_year = {}
paper_author_year = {}
author_org_year = {}

for year in range(STARTYEAR, ENDYEAR + 1):
#    doi_fout_year[year] = open("../../network/" + str(year) + "/")
    paper_venue_year[year] = open("../../network/" + str(year) + "/paper_venue", "w")
    paper_author_year[year] = open("../../network/" + str(year) + "/paper_author", "w") 
    author_org_year[year] = open("../../network/" + str(year) + "/author_organ", "w")

doi_id = 0
author_id = 0 
venue_id = 0 
org_id = 0 

files = ["./temp.xml"]
files = ["./PR.xml", "./PRA.xml", "./PRB.xml", "./PRC.xml", "./PRD.xml", "./PRE.xml", "./PRI.xml", "./PRL.2.xml", "./PRSTAB.xml", "./PRSTPER.xml", "./RMP.xml"]
for f in files:
    tree = ET.parse(f)
    root = tree.getroot()

    for article in root:    
        p_v = ""
        p_a = ""
        a_o = ""
        
        print "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-", f
        for feature in article:
            if feature.tag == "doi":
                doi = feature.text
                print doi
                if doi not in doi_dict:
                    doi_id += 1
                    doi_dict[doi] = doi_id 
                
            if feature.tag == "journal":
                venue = feature.attrib['jcode'] 
                full = feature.text
                full = full.replace("\n", "")
                print venue, full
                if (venue, full) not in venue_dict:
                    venue_id += 1
                    venue_dict[(venue, full)] = venue_id
                    venue_fout.write(str(venue_id) + "\t" + venue + "\t" + full + "\n") 
                paper_venue.write(str(doi_id) + "\t" + str(venue_dict[(venue, full)]) + "\n")
                p_v += str(doi_id) + "\t" + str(venue_dict[(venue, full)]) + "\n"
                
            if feature.tag == 'issue':
                time = feature.attrib['printdate']
                year = (time.split("-")[0])
            
            if feature.tag == 'published':
                year = feature.attrib['date'].split('-')[0]

            if feature.tag == 'authgrp':
                author_set = []
		author_sec = {} 
                for author in feature:
                    if author.tag == 'author':
                        author_name = ''
                        name_text = ''
                        for name in author:
                            if name.text is None:
                                continue
                            
                            if author_name == "":
                                name_text = ''
                                for cc in name.text:
                                    if ord(cc) < 128:
                                        name_text += cc.lower()
                                author_name += name_text
                                
                            else:
                                name_text = ''
                                for cc in name.text:
                                    if ord(cc) < 128:
                                        name_text += cc.lower()
                                author_name += " " + name_text
                            print name.text, name_text
                        if author_name == '':
                            continue 
                        
                        author_set.append(author_name)
                        print "author.attrib", author.attrib
                        try:
                            author_sec[author_name] = author.attrib['affref'].split()
                        except:
                            author_sec[author_name] = ""
                            
                        if author_name not in author_dict:
                            author_id += 1
                            author_dict[author_name] = author_id
                            author_fout.write(str(author_id) + "\t" + author_name + "\n")
                        
                        paper_author.write(str(doi_id) + "\t" + str(author_dict[author_name]) + "\n")
                        p_a += str(doi_id) + "\t" + str(author_dict[author_name]) + "\n"
                    
                    if author.tag == 'aff':
                        org_1 = author.text
                        if org_1 is None:
                            continue
                        org_1 = author.text.lower()
                        
			print "org_1", org_1
                        print "author.attrib", author.attrib
                        
                        try:
                            org_sec = author.attrib['affid'].split()[0].lower()
                        except:
                            org_sec = ""
                            
                        org = ""
                        for cc in org_1:
                            if ord(cc) < 128:
                                org += cc
                        print org_1, org
                        if org not in org_dict:
                            org_id += 1
                            org_dict[org] = org_id
                            org_fout.write(str(org_id) + "\t" + org + "\n")
                            
                        for author_name in author_set:
                            if org_sec in author_sec[author_name]:
                                author_org.write(str(author_dict[author_name]) + "\t" + str(org_dict[org]) + "\n")
                                a_o += str(author_dict[author_name]) + "\t" + str(org_dict[org]) + "\n"
                                author_check.write(author_name + "\t" + org + "\n")
                                
            if feature.tag == 'title':
                title_org = feature.text.lower() 
                title = ""
                for cc in title_org:
                    if ord(cc) < 128:
                        title += cc
                print title 
                
        doi_fout.write(str(doi_id) + "\t" + str(doi) + "\t" + year + "\t" + title + "\n") 
        paper_venue_year[int(year)].write(p_v) 
        paper_author_year[int(year)].write(p_a) 
        author_org_year[int(year)].write(a_o)  

doi_fout.close() 
venue_fout.close() 
paper_venue.close() 
org_fout.close() 
author_org.close() 
author_check.close() 
for year in range(STARTYEAR, ENDYEAR + 1):
#    doi_fout_year[year] = open("../../network/" + str(year) + "/")
    paper_venue_year[year].close() 
    paper_author_year[year].close() 
    author_org_year[year].close() 

