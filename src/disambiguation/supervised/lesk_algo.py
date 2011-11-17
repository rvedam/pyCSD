# lesk_algo.py
#
# This module implements Lesk's algorithm for dictionary-based disambiguation.
#

from concept_generation.sqlite_dict import SQLiteDict
from collections import defaultdict
import math, cPickle as pickle, os, sys

# The location of the UMLS CUI DB - maps CUIs to their definitions
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("/data/ram/umlsdb.sqlite3"))
umls = SQLiteDict(UMLS_DB_LOCATION)

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
        try:
            self.ambigdict = pickle.load(ambig_file)
        finally:
            ambig_file.close()
    def overlap(self, def1, context):
        '''
        checking to see how much overlap there is between two definitions of a sense.
        utilizes bag of words model and computes the cardinality of the intersection 
        set consists of those terms that are in both sets.
        '''
        sdef1 = set(def1)
        oscore = sdef1.intersection(query)
        return oscore
    def disambiguation(self, query):
        '''
        currently this is designed to only deal with the ambiguities found in the corpus.
        '''
        for concept in ambigdict[query]:
            cdef = umls[concept]
            self.concept_scores[concept] = self.overlap(cdef, query)
        cmax_score = -1
        max_cui = ""
        for cui in self.concept_scores.keys():
            if self.concept_scores[cui] > cmax_score:
                max_cui, cmax_score = cui, self.concept_scores[cui]
        return max_cui


