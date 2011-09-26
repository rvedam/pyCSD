#!/usr/bin/env python
# encoding: utf-8
"""
umls_db.py

Created by Jorge Herskovic on 2011-09-20.
Copyright (c) 2011 UTHealth School of Biomedical Informatics. All rights reserved.
"""

import sys
import os.path
from sqlite_dict import *

# Modify to fit your system - if the db doesn't exist, it'll be created using this
# file. 
#MRDEF_RRF="/Volumes/More Ocho/UMLS/umls/2010AA/META/MRDEF.RRF"
MRDEF_RREF="/home/vedam/data_disk/UMLS/2011AA/META/MRDEF.RRF"

# The actual location of the DB
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("~/data_disk/umlsdb.sqlite3"))

def generate_umls_db(mrdef, db_dest):
    original=open(mrdef, 'rU')
    db=SQLiteDict(UMLS_DB_LOCATION)
    db.commits_enabled=False # TO speed it up a bit
    
    last_CUI=None
    these_definitions=[]
    progress=0
    
    for line in original:
        split_line=line.split('|')
        CUI,definition=split_line[0],split_line[5]
        if last_CUI!=CUI:
            if last_CUI is not None:
                db[last_CUI]=these_definitions
            these_definitions=[]
            last_CUI=CUI
        these_definitions.append(definition)
        progress+=1
        if (progress % 10000)==0:
            print "%d lines processed." % progress
    # Catch any stragglers
    if len(these_definitions)>0:
        db[last_CUI]=these_definitions
    return
    
def main():
    # Test for existence
    try:
        dummy=open(UMLS_DB_LOCATION, 'rb')
        dummy.close()
        umls=SQLiteDict(UMLS_DB_LOCATION)
        print "The definitions for C0006160 are:", umls['C0006160']
    except IOError:
        print "BUILDING UMLS DB FOR THE FIRST TIME."
        generate_umls_db(MRDEF_RRF, UMLS_DB_LOCATION)
        print "Done."

if __name__ == '__main__':
	main()

