# ambig_dict
#
# module that contains a class that can be use to keep track of
# ambiguities inside a corpus. Right now this has been designed to 
# predefined data format (which will be written in the readme.
#
# This file contains two objects: AmbigDict and ContextSpanAmbigDict.

import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation

class AmbigDict:
    '''
    Object is set up to keep track of Corpus-related Ambiguities.  Since it is 
    necessary only to keep track based where a phrase (i.e. span) occurs and 
    the CUIs associated with a given span, this object keeps data is much more 
    granular and higher level than the ContextSpanAmbigDict.
    '''
    def __init__(self):
        self.span_concept_dict = dict() 
        self.sent_no_dict = dict()
    def add_entry(self, phrase, concept_list, sent_no_list):
        self.span_concept_dict[phrase] = concept_list
        self.sent_no_dict[phrase] = sent_no_list
    def get_concepts(self, phrase):
        return self.span_concept_dict[phrase]
    def get_sentences(self, phrase):
        return self.sent_no_dict[phrase]
    def keys(self):
        return self.span_concept_dict.keys()

class ContextSpanAmbigDict:
    '''
    Finer grained ambiguity dictionary that keeps track of span ambiguities w.r.t. a specific context.
    '''
    def __init__(self):
        self.context_span_dict = dict()
        self.sent_no_dict = dict()
    def add_entry(self, span, context, cui_set):
        '''
        adds entry to ambiguity dictionary map w.r.t. context passed in.
        '''
        if context not in self.context_span_dict:
            self.context_span_dict[context] = dict()
        if span in self.context_span_dict[context]:
            self.context_span_dict[context][span].add(cui_list)
        else:
            self.context_span_dict[context][span] = cui_set
        if span not in self.sent_no_dict:
            self.sent_no_dict[span] = list()
        self.sent_no_dict[span].append(context)
    def get_concepts(self, context, span):
        '''
        returns all cuis related to a given span
        '''
        return self.context_span_dict[context][span]
    def get_sentence_nos(self, span):
        return self.sent_no_dict[span]
    def get_spans(self):
        return self.sent_no_dict.keys()    
