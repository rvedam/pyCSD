# umls_cui_extractor_mp.py
#
# multiprocessing implementation of concept extractor
#

import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation
import csdutils, metamap
from sqlite_dict import *
import time

# The actual location of the UMLS CUI DB
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("/data/ram/umlsdb.sqlite3"))

global doc_counter
doc_counter = 0
def completed_cb(r):
    global doc_counter
    doc_counter += 1
    print 'PROCESSED %d documents' % doc_counter

global doc_sent_data # document-sentence map (makes the large data structure across all processes)
doc_sent_data = dict()
def cui_extractor_worker(docSentList, output_file_path):
    '''
    extracts all concepts of a given document
    INPUTS: 
    docSentList - list of sentence ids representing a document
    sentDict - dictionary that holds individual sentences, retrieved based on id.
    output_file_path - output file path.
    ''' 
    output_file = open(output_file_path, 'a+')
    umls = SQLiteDict(UMLS_DB_LOCATION)
    try: 
        for sentNo in docSentList: 
            global doc_sent_data
            query = doc_sent_data[str(sentNo).zfill(10)] 
            concepts = metamap.retrieve_concepts(query)
            for concept_output in concepts: 
                split_concept = concept_output.split('|') 
                confidence_score = split_concept[2] 
                cui = split_concept[4] 
                concept_name = split_concept[3] 
                semantic_type = split_concept[5] 
                phrase_span = split_concept[8] 
                try: 
                    concept_definition = umls[cui]
                except KeyError:
                    continue 
                output_line = str(sentNo) + '|' + str(confidence_score)  + '|' + cui + '|' + concept_name + '|' + str(concept_definition) + '|' + semantic_type + '|' + phrase_span + '\n' 
                output_file.write(output_line)
    finally:
        output_file.close()

def generate_concepts(data_dir):
    ''' main concept generation routine '''
    sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(data_dir, 'concept_files')
    remaining_file_list_path = os.path.join(data_dir, 'remaining.pkl')
    
    print "STEP 1: reading in document-sentence map file"
    docSentMapBinFile = open(pmap_file_path, 'rb')
    map_bin_data = docSentMapBinFile.read()
    sio = StringIO.StringIO(map_bin_data)
    docSentMap = pickle.load(sio)

    sentMapData = open(sent_file_path, 'rU')
    for sentData in sentMapData.readlines():
        sentence = sentData.split('|')
        global doc_sent_data
        doc_sent_data[sentence[0]] = sentence[1]
    print "STEP 1 COMPLETE"
    documents = docSentMap.keys()

    # if the remaining file list path exists then that means then the process
    # was interrupted, needs to continue where it left off.
    if os.path.exists(remaining_file_list_path):
        rfile = open(remaining_file_list_path, 'rb')
        try:
            documents = pickle.load(rfile)
        finally:
            rfile.close()

    process_pool = multiprocessing.Pool(15)
    print "STEP 2: Generating concept documents "
    try:
       for document in documents:
            output_file_path = os.path.join(output_file_dir, document)
            docSentList = docSentMap[document]
            process_pool.apply_async(cui_extractor_worker, (docSentList, output_file_path), callback=completed_cb)
    finally:
        process_pool.close()
        process_pool.join()

if __name__ == '__main__':
    data_dir = '/data/ram/14k_collection'
    generate_concepts(data_dir) 
