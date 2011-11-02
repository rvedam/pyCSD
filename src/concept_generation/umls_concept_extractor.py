# umls_concept_extractor
#
# Given a document or a corpus of text (formatted in a specific way)
# this program will tokenize, and extract UMLS concepts from the texts.
#

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ramnarayan Vedam"
__date__ ="$Sep 11, 2011 9:56:52 PM$"

import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation
import csdutils, metamap
from sqlite_dict import *

# The actual location of the DB
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("/data/ram/umlsdb.sqlite3"))
CUI_DNE_FILE = os.path.normpath(os.path.expanduser('/data/ram/cui_dne_error.log'))

# TODO: need to get rid of hardcoded paths
def generate_concepts(input_dir_path):
    sent_file_path = os.path.join(input_dir_path, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(input_dir_path, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(input_dir_path, 'concept_files')

    print "STEP 1: reading in document-sentence map file"
    docSentMapBinFile = open(pmap_file_path, 'rb')
    map_bin_data = docSentMapBinFile.read()
    sio = StringIO.StringIO(map_bin_data)
    docSentMap = pickle.load(sio)

    doc_sent_data = {}
    sentMapData = open(sent_file_path, 'rU')
    for sentData in sentMapData.readlines():
        sentence = sentData.split('|')
        doc_sent_data[sentence[0]] = sentence[1]
    print "STEP 1 COMPLETE"

    print "STEP 2: Generating concept documents "
    try:
        count = 0
        for document in docSentMap.keys():
            output_file_path = os.path.join(output_file_dir, document)
            output_file = open(output_file_path, 'a+')
            try:
                umls=SQLiteDict(UMLS_DB_LOCATION)
                try:
                    for sentNo in docSentMap[document]: 
                        concepts = metamap.retrieve_concepts(doc_sent_data[str(sentNo).zfill(10)])
                        for concept_output in concepts:
                            split_concept = concept_output.split('|')
                            confidence_score = split_concept[2]
                            cui = split_concept[4]
                            concept_name = split_concept[3]
                            semantic_type = split_concept[5]
                            phrase_span = split_concept[8]
                            concept_dne_file = open(CUI_DNE_FILE, 'a+') 
                            try:
                                concept_definition = umls[cui]
                            except KeyError:
                                concept_dne_file.write(document + '|' + str(sentNo) + '|' + phrase_span + '|' + cui + '\n')
                                continue
                            finally:
                                concept_dne_file.close()
                            output_line = str(sentNo) + '|' + str(confidence_score)  + '|' + cui + '|' + concept_name + '|' + str(concept_definition) + '|' + semantic_type + '|' + phrase_span + '\n'
                            output_file.write(output_line)
                finally:
                    output_file.close()
                    concept_dne_file.close()
                    count = count + 1
            except IOError:
                print "UMLS DB does not exist. PLEASE RUN umls_db.py before running this program"
            print 'PROCESSED %d documents' % count 
    except KeyError:
        print "Key not found"


if __name__ == "__main__":
    data_dir = '/data/ram/14k_collection'
    generate_concepts(data_dir)
