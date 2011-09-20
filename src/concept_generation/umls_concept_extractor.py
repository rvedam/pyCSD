# umls_concept_extractor
#
# Given a document or a corpus of text (formatted in a specific way)
# this program will tokenize, and extract UMLS concepts from the texts.
#

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ramnarayan Vedam"
__date__ ="$Sep 11, 2011 9:56:52 PM$"

import sys, cPickle as pickle, cStringIO as StringIO, math, re
from gov.nih.nlm.nls.metamap import Ev
from com.vrn.utils import MetaMapWrapper, NGramFactory, NGram
from java.util import HashMap
import os.path   # Platform-independent path manipulation

# TODO: need to get rid of hardcoded paths
def generate_ngrams(aString, stopwords, tuple_size):
    tokens = [re.sub('\\n|\\.|\\(|\\)|\\-', '', word) for word in aString.split(' ') if word not in stopwords]
    ngrams = NGramFactory.parseNgrams(tokens, tuple_size)
    return ngrams

def generate_concepts(input_dir_path, stopword_file_path):
    sent_file_path = os.path.join(input_dir_path, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(input_dir_path, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(input_dir_path, 'concept_files')
    stopwords_file = open(stopword_file_path, 'r')
    stopwords = [word.replace('\n', '') for word in stopwords_file.readlines() if '#' not in word and word != '\n']
    print stopwords

    print "STEP 0: Making connection to server"
    umls = MetaMapWrapper("localhost", 8066)
    print "STEP 0 COMPLETE"

    print "STEP 1: reading in document-sentence map file"
    docSentMapBinFile = open(pmap_file_path, 'rb')
    map_bin_data = docSentMapBinFile.read()
    sio = StringIO.StringIO(map_bin_data)
    docSentMap = pickle.load(sio)

    sent_file = open(sent_file_path, 'r')
    doc_sent_data = {}
    for sentence in sent_file.readlines():
        splitSent = sentence.split('|')
        doc_sent_data[splitSent[0]] = splitSent[1]
    print "STEP 1 COMPLETE"

    print "STEP 2: Generating concept documents "
    try:
        count = 0
        for document in docSentMap.keys():
            output_file_path = os.path.join(output_file_dir, document)
            print "WRITING OUT CONCEPTS FOR DOCUMENT: ", document
            for sentNo in docSentMap[document]:
                # grab splitted sentence
                key = str(sentNo).zfill(10)
                sentNgrams = generate_ngrams(doc_sent_data[key], stopwords, 3)
                for ngram in sentNgrams:
                    phraseArray = map(lambda x: ''.join([x, ' ']), ngram.getTuple())
                    phrase = ''.join(phraseArray)
                    results = umls.retrieveConcepts(phrase)
                    for candidate in umls.retrieveCandidates(results):
                         if math.fabs(candidate.getScore()) >= 800:
                             # TODO: once database is generated, add query
                             #       to grab concept definition and write
                             #       concept CUI definition out to file as
                             #       well.
                             formatted_output = str(sentNo) + "|" + phrase + "|" + str(candidate.getConceptId()) + "|" + candidate.getConceptName() + '\n'
                             output = open(output_file_path, 'a+')
                             try:
                                 output.write(formatted_output)
                             finally:
                                 output.close()
            count = count + 1
            print "NUM OF DOCS PROCESSED: ", count
        print "STEP 2 COMPLETE"
    finally:
        docSentMapBinFile.close()
        print "PROCESS COMPLETE. PLEASE LOOK INTO ", output_file_dir, " TO EXAMINE FILES"

if __name__ == "__main__":
    data_dir = '/home/vedam/data_disk/HI_classes/HI6002_Jorge'
    stopword_file_path = '/home/vedam/NetBeansProjects/pyCSD/utils/salton_stopwords.txt'
    generate_concepts(data_dir, stopword_file_path)    