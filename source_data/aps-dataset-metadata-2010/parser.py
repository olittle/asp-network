#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : parser.py
#
# Purpose : parse the xml  
#
# Creation Date : 12-09-2013
#
# Last Modified : Fri 13 Sep 2013 01:31:26 PM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu) 
#
#_._._._._._._._._._._._._._._._._._._._._.


import xml.etree.ElementTree as ET

doi_dict = {} 
doi_fout = open("../../rawdata/doi_paper.txt", "w") 
year_dict = {} 

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

doi_id = 0
author_id = 0 
venue_id = 0 
org_id = 0 

files = ["./PRA.xml"]
#files = ["./PR.xml", "./PRA.xml", "./PRB.xml", "./PRC.xml", "./PRD.xml", "./PRE.xml", "./PRI.xml", "./PRL.xml", "./PRSTAB.xml", "./PRSTPER.xml", "./RMP.xml"]
for f in files:
    tree = ET.parse(f)
    root = tree.getroot()

    for article in root:    
        print "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-", f
        print article.tag, article.attrib
        for feature in article:
            print feature.tag, feature.attrib, feature.text
            if feature.tag == "doi":
                doi = feature.text
                print doi
                if doi not in doi_dict:
                    doi_id += 1
                    doi_dict[doi] = doi_id 
                
            if feature.tag == "journal":
                venue = feature.attrib['jcode'] 
                full = feature.text
                print venue, full
                if (venue, full) not in venue_dict:
                    venue_id += 1
                    venue_dict[(venue, full)] = venue_id
                    venue_fout.write(str(venue_id) + "\t" + venue + "\t" + full + "\n") 
                paper_venue.write(str(doi_id) + "\t" + str(venue_dict[(venue, full)]) + "\n")
                
            if feature.tag == 'issue':
                time = feature.attrib['printdate']
                year = (time.split("-")[0])

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
                                        name_text += cc
                                author_name += name_text
                            else:
                                name_text = ''
                                for cc in name.text:
                                    if ord(cc) < 128:
                                        name_text += cc
                                author_name += " " + name_text
                            print name.text, name_text
                        if author_name == '':
                            continue 
                        
                        print "author-", author_name
                        author_set.append(author_name)
                        print "author.attrib", author.attrib
                        try:
                            author_sec[author_name] = author.attrib['affref']
                        except:
                            author_sec[author_name] = ""
                    
                    if author.tag == 'aff':
                        org_1 = author.text
                        if org_1 is None:
                            continue
                        
			print "org_1", org_1
                        print "author.attrib", author.attrib
                        
                        try:
                            org_sec = author.attrib['affid']
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
                            if author_name not in author_dict:
                                author_id += 1
                                author_dict[author_name] = author_id
                                author_fout.write(str(author_id) + "\t" + author_name + "\n")
                            
                            if author_sec[author_name] == org_sec:
                                author_org.write(str(author_dict[author_name]) + "\t" + str(org_dict[org]) + "\n")
                                author_check.write(author_name + "\t" + org + "\n")
                                paper_author.write(str(doi_id) + "\t" + str(author_dict[author_name]) + "\n")
                                
            if feature.tag == 'title':
                title_org = feature.text
                title = ""
                for cc in title_org:
                    if ord(cc) < 128:
                        title += cc
                print title 
                
        doi_fout.write(str(doi_id) + "\t" + str(doi) + "\t" + year + "\t" + title + "\n") 

doi_fout.close() 
venue_fout.close() 
paper_venue.close() 
org_fout.close() 
author_org.close() 
author_check.close() 

