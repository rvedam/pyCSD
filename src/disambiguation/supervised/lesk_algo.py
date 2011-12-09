# lesk_algo.py
#
# This module implements Lesk's algorithm for dictionary-based disambiguation.
#

from concept_generation.sqlite_dict import SQLiteDict
from collections import defaultdict
import math, cPickle as pickle, os, sys
from analysis.ambig_dict import *

# The location of the UMLS CUI DB - maps CUIs to their definitions
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("/data/ram/umlsdb.sqlite3"))
STOPWORD_FILE = os.path.join(os.path.expanduser("~"), "pyCSD", "utils", "salton_stopwords.txt")

umls = SQLiteDict(UMLS_DB_LOCATION)

# read in stopwords file.
stopwords = set()
sw_file = open(STOPWORD_FILE, 'r+')

for line in sw_file.readlines():
    stopwords.add(line.replace('\n', ''))

sw_file.close()

class LeskAlgo:
    def __init__(self, sent_file_path, ambig_file_path):
        '''constructor'''
        sent_file = open(sent_file_path, 'rU')
        self.sent_map = {}
        self.concept_scores = {} 
        try:
            for sentData in sent_file.readlines():
                sentence = sentData.split('|')
                self.sent_map[sentence[0]] = sentence[1]
        finally:
            sent_file.close()
        ambig_file = open(ambig_file_path, 'rb')
        self.ambigdict = pickle.load(ambig_file)
        ambig_file.close()
    def overlap(self, def1, context):
        '''
        checking to see how much overlap there is between two definitions of a sense.
        utilizes bag of words model and computes the cardinality of the intersection 
        set consists of those terms that are in both sets.
        '''
        # TODO: Strip stopwords from definitions AND from context
        sdef1_combined_defs = "".join(def1)
#        sdef1 = set(def1)
        sdef1 = set(sdef1_combined_defs.lower().split()).difference(stopwords)
        sdef1 = sdef1.difference(stopwords)
        print 'CUI Definition without stopwords\n\n', sdef1, '\n\n'
        context = set(context.lower().split()).difference(stopwords)
        print 'sentence without stopwords\n\n', context, '\n\n'

        # TODO: Think about normalizing the scores in a meaningful way
        oscore = sdef1.intersection(set(context))

        return len(oscore)
    def disambiguation(self, query, context):
        '''
        currently this is designed to only deal with the ambiguities found in 
        the corpus.
        '''
        concept_list = self.ambigdict.get_concepts(context, query)
        for concept in concept_list:
            # find the sentence that this query mapped to.
            sentence = self.sent_map[context]
            cdef = umls[concept]
            self.concept_scores[concept] = self.overlap(cdef, sentence)
        cmax_score = -1
        max_cui = ""
        for cui in self.concept_scores.keys():  
            print 'CANDIDATE CUI: ', cui
            print 'CANDIDATE OVERLAP SCORE: ', self.concept_scores[cui]
            if self.concept_scores[cui] > cmax_score:
                max_cui, cmax_score = cui, self.concept_scores[cui]
        print 'DISAMBIGUATION COMPLETE'
        print 'FINAL CUI: ', max_cui
        print 'FINAL CUI SCORE: ', cmax_score
        return max_cui
    def get_ambig_dict(self):
        return self.ambigdict
    def get_sentence(self, sent_no):
        return self.sent_map[sent_no]
