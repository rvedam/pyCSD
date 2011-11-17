# find_ambiguities.py
#
# this program will open up every concept file document generated with the umls_cui_extractor_mp module
# and it will count the number of ambiguities a word with a given concept may have

import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation
import csdutils, metamap
from sqlite_dict import *
import time
import smtplib

word_concept_dict = {}
concept_count_dir = {}

def find_ambiguities(data_dir):
    sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(data_dir, 'concept_files')
    # read in the sentence map (we need the actual phrase when finding the concept
    doc_sent_data = dict()
    sentMapData = open(sent_file_path, 'rU')
    for sentData in sentMapData.readlines():
        sentence = sentData.split('|')
        global doc_sent_data
        sent_map[sentence[0]] = sentence[1]

    # for each document, grab the phrase and the CUI (we'll add filtering later) 
    # and store them
    for document in os.listdir(output_file_dir):
        phrase_cui_file = open(document, 'rU')
        for phrase_cui_line in phrase_cui_file.readlines():
            phrase_cui_comp = phrase_cui_line.split('|')
            # grab the phrase information that we have recorded from the metamap output.
            phrase_info = phrase_cui_comp[len(phrase_cui_comp) - 1].split(':')
            phraseStartIdx = int(phrase_info[0])
            phrase_length = int(phrase_info[1])
            phraseEndIdx = phraseStartIdx + phrase_length

            # grab the sentence and phrase
            sentence = self.sent_map[phrase_cui_comp[0].zfill(10)]
            phrase = sentence[phraseStartIdx:phraseEndIdx]
            if phrase not in word_concept_dict:
                word_concept_dict[phrase] = []
            word_concept_dict[phrase].append(phrase_cui_comp[2])

    ambig_word_concept_dict = dict()
    for phrase in word_concept_dict:
        if len(word_concept_dict[phrase]) > 1:
            ambig_word_concept_dict[phrase] = word_concept_dict[phrase]
    return ambig_word_concept_dict
       

if __name__ == '__main__':
    data_dir = '/data/ram/14k_collection/'
    print 'FINDING AMIBIGUITIES INSIDE DATASET PROVIDED IN DATA_DIR: ', data_dir
    # pickle the final set of ambiguities to a file
    ambig_file_path = os.path.join(data_dir, 'ambiguities.pkl')

    # grab all ambiguities in the corpus
    ambig_word_concept_dict = find_ambiguities(data_dir)
    ambig_file = open(ambig_file_path, 'wb+')
    try:
        pickle.dump(ambig_word_concept_dict, ambig_file)
    finally:
        ambig_file.close()
