# ambig_dict
#
# module that contains a class that can be use to keep track of
# ambiguities inside a corpus. Right now this has been designed to 
# predefined data format (which will be written in the readme.
#

import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation

class AmbigDict:
    def __init__(self):
        self.word_concept_dict = dict() 
        self.sent_no_dict = dict()
    def add_entry(self, phrase, concept_list, sent_no_list):
        self.word_concept_dict[phrase] = concept_list
        self.sent_no_dict[phrase] = sent_no_list
    def get_concepts(self, phrase):
        return self.word_concept_dict[phrase]
    def get_sentences(self, phrase):
        return self.sent_no_dict[phrase]
    def keys(self):
        return self.word_concept_dict.keys()

