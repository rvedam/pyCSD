# umls_concept_extractor
#
# Given a document or a corpus of text (formatted in a specific way)
# this program will tokenize, and extract UMLS concepts from the texts.
#

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ramnarayan Vedam"
__date__ ="$Sep 11, 2011 9:56:52 PM$"

import sys, cPickle as pickle, cStringIO as StringIO

from gov.nih.nlm.nls.metamap import Ev
from com.vrn.utils import MetaMapWrapper

data_dir = '/home/vedam/data_disk/HI_classes/HI6002_Jorge'
sent_file_path = data_dir + '/full_text_with_abstract_and_title.metamap'
pmap_file_path = data_dir + '/full_text_with_abstract_and_title.metamap.chunkmap'
output_file_dir = data_dir + '/concept_files'

if __name__ == "__main__":
    print "STEP 0: Making connection to server"
    umls = MetaMapWrapper("localhost", 8066)
    print "STEP 0 COMPLETE"

    print "STEP 1: reading in document-sentence map file"
    docSentMapBinFile = open(pmap_file_path, 'rb')
    map_bin_data = docSentMapBinFile.read()
    sio = StringIO.StringIO(map_bin_data)
    docSentMap = pickle.load(sio)
    print "STEP 1 COMPLETE"

    print "STEP 2: "
    try:
        results = umls.retrieveConcepts("lab culture")
        for result in results:
            for candidate in umls.retrieveCandidates(result):
                print candidate.getConceptId(), " ", candidate.getConceptName()
    finally:
        docSentMapBinFile.close()
        print "DONE"

#if __name__ == "__main__":
#    print "running program"
#    docSentMapBinFile = open(pmap_file_path, 'rb')
#    bin_data = docSentMapBinFile.read()
#    sentMapAsString = StringIO.StringIO(bin_data)
#    sentMap = pickle.load(sentMapAsString)
#    print sentMap['15046638.txt']
    