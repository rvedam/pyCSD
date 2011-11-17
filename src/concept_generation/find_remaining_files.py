# 
# find_remaining_files.py
#
# Utility program based on the same representation input files that 
# is used for UMLS CUI Extraction from the medline data.
# this module specifically holds a function that will read in the full text 
# dictionary to find the files that need to be generated and do a filter on 
# the list based on what has already been generated.
#

import os
import sys, cPickle as pickle, cStringIO as StringIO, math, csv

def find_remaining_files(data_dir):
    ''' 
    function that will, based on what needs to be process still from the parent 
    set of documents read in from the medline abstract main dictionary, it will compute
    how many more files need to be processed
    '''
    sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(data_dir, 'concept_files')
    complete_set = set()
    current_completed_set = set()
    print "STEP 1: reading in document-sentence map file"
    docSentMapBinFile = open(pmap_file_path, 'rb')
    map_bin_data = docSentMapBinFile.read()
    sio = StringIO.StringIO(map_bin_data)
    docSentMap = pickle.load(sio)

    complete_set = set(docSentMap.keys())
    for filename in os.listdir(output_file_dir):
        current_completed_set.add(filename)
    return complete_set - current_completed_set

if __name__ == '__main__':
    data_dir = '/data/ram/14k_collection'
    rfile_path = os.path.join(data_dir, 'remaining.pkl')
   
    if os.path.exists(rfile_path):
        rfile = open(rfile_path, 'rb+')
        try:
            rfile_list = pickle.load(rfile)
        finally:
            rfile.close()
        # let's test to see if we successfully pickled the data
        print 'length of list: ', len(rfile_list)
    else:
        remaining_filenames = find_remaining_files(data_dir) 
        rfile = open(rfile_path, 'wb+')
        # pickle with protocol 0.
        pickle.dump(remaining_filenames, rfile)
        rfile.close()

    
