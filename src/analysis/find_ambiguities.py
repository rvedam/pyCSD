# find_ambiguities.py
#
# this program will open up every concept file document generated with the umls_cui_extractor_mp module
# and it will count the number of ambiguities a word with a given concept may have

import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation
import time
import smtplib
from email.mime.text import MIMEText


word_concept_dict = {}
concept_count_dir = {}

def find_ambiguities(data_dir):
    sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(data_dir, 'concept_files')
    # read in the sentence map (we need the actual phrase when finding the concept
    sent_map = dict()
    sentMapData = open(sent_file_path, 'rU')
    for sentData in sentMapData.readlines():
        sentence = sentData.split('|')
        sent_map[sentence[0]] = sentence[1]

    # for each document, grab the phrase and the CUI (we'll add filtering later) 
    # and store them
    for document in os.listdir(output_file_dir):
        print 'PROCESSING DOCUMENT: ', document
        phrase_cui_file = open(os.path.join(output_file_dir, document), 'rU')
        for phrase_cui_line in phrase_cui_file.readlines():
            phrase_cui_comp = phrase_cui_line.split('|')
            # find the sentence where the phrase is located 
            sentence = sent_map[phrase_cui_comp[0].zfill(10)]
            # grab the phrase information that we have recorded from the metamap output.
            phrase_info = phrase_cui_comp[len(phrase_cui_comp) - 1]
            phraseList = []
            phrase = " "
            if ',' in phrase_info: # we may have a concept mapped to a phrase spanning two words
                for phrase_info_comp in phrase_info.split(','):
                    splited_pinfo_comp = phrase_info_comp.split(':')
                    phraseStartIdx = int(splited_pinfo_comp[0]) 
                    phrase_length = int(splited_pinfo_comp[1]) 
                    phraseEndIdx = phraseStartIdx + phrase_length
                    phraseList.append(sentence[phraseStartIdx:phraseEndIdx])
                phrase = phrase.join(phraseList)
            else:
                if ':' in phrase_info: 
                    pinfo_comp = phrase_info.split(':')
                    phraseStartIdx = int(pinfo_comp[0]) 
                    phrase_length = int(pinfo_comp[1]) 
                    phraseEndIdx = phraseStartIdx + phrase_length
                    phrase = sentence[phraseStartIdx:phraseEndIdx]
                
            # grab the sentence and phrase
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
    
    print 'PROCESS COMPLETED'
    fromaddr = 'Ramnarayan.Vedam@uth.tmc.edu'
    toaddrs = ['Ramnarayan.Vedam@uth.tmc.edu', 'Jorge.R.Herskovic@uth.tmc.edu']

    Subject = 'Word Ambiguities detection program completed'
    msg = MIMEText('The program that would find all ambiguities from running metamap with wsd turned on has been completed.\
Please look at the pickled file ambiguities.pkl located in /data/ram/14k_collection/ directory')

    msg['Subject'] = Subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    # send email to both Jorge and I (TODO: create a file holding list of emails that program should email to)
    server = smtplib.SMTP('smtp.uth.tmc.edu')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
    
