# find_corpus_ambiguities.py
#
# this program will open up every concept file document generated with the umls_cui_extractor_mp module
# and it will count the number of ambiguities a word with a given concept may have

import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation
import time
import smtplib
from email.mime.text import MIMEText
from analysis.ambig_dict import AmbigDict

word_concept_dict  = dict()
sent_no_dict = dict()

def find_corpus_ambiguities(data_dir):
    sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
    pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
    output_file_dir = os.path.join(data_dir, 'concept_files')
    # read in the sentence map (we need the actual phrase when finding the concept
    sent_map = dict()
    sentMapData = open(sent_file_path, 'rU')
    for sentData in sentMapData.readlines():
        sentence = sentData.split('|')
        sent_map[sentence[0]] = sentence[1]
    sentMapData.close()

    # for each document, grab the phrase and the CUI (we'll add filtering later) 
    # and store them
    num = 1
    for document in os.listdir(output_file_dir):
        phrase_cui_file = open(os.path.join(output_file_dir, document), 'rU')
        for phrase_cui_line in phrase_cui_file.readlines():
            if '|' not in phrase_cui_line:
                continue
            phrase_cui_comp = phrase_cui_line.split('|')
            cui = ""
            try:
                cui = phrase_cui_comp[2]
            except IndexError:
                print 'phrase_cui_comp: ', phrase_cui_comp
                sys.exit(1)

            # find the sentence where the phrase is located 
            sent_no = phrase_cui_comp[0].zfill(10)
            sentence = sent_map[sent_no]
            # grab the phrase information that we have recorded from the metamap output.
            phrase_info = phrase_cui_comp[len(phrase_cui_comp) - 1]
            phraseList = []
            phrase = " "
            if ',' in phrase_info: # we may have a concept mapped to a phrase spanning two words
                for phrase_info_comp in phrase_info.split(','):
                    splited_pinfo_comp = phrase_info_comp.split(':')
                    if isinstance(splited_pinfo_comp[0], (int ,long)) and isinstance(splited_pinfo_comp[1], (int, long)):
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
                    word_concept_dict[phrase] = set()
                    sent_no_dict[phrase] = set()
 
                word_concept_dict[phrase].add(cui)
                sent_no_dict[phrase].add(sent_no)
        phrase_cui_file.close()

    final_ambig_dict = AmbigDict()
    ambig_word_concept_dict = dict()
    for phrase in word_concept_dict:
        if len(word_concept_dict[phrase]) > 1:
#            ambig_word_concept_dict[phrase] = list(word_concept_dict[phrase])
            final_ambig_dict.add_entry(phrase, list(word_concept_dict[phrase]), list(sent_no_dict[phrase]))
#    return ambig_word_concept_dict
    return final_ambig_dict
       

if __name__ == '__main__':
    data_dir = '/data/ram/14k_collection/'
    pickle_fname = 'ambiguities_corpus.pkl'
    print 'FINDING AMIBIGUITIES INSIDE DATASET PROVIDED IN DATA_DIR: ', data_dir
    # pickle the final set of ambiguities to a file
    ambig_file_path = os.path.join(data_dir, pickle_fname)

    # grab all ambiguities in the corpus
    ambig_word_concept_dict = find_corpus_ambiguities(data_dir)
    print 'pickling data'
    ambig_file = open(ambig_file_path, 'wb+')
    try:
        pickle.dump(ambig_word_concept_dict, ambig_file)
    finally:
        ambig_file.close()
    print 'pickling data complete'
    
    print 'PROCESS COMPLETED'
    fromaddr = 'Ramnarayan.Vedam@uth.tmc.edu'
    toaddrs = "Ramnarayan.Vedam@uth.tmc.edu"

    Subject = 'Word Ambiguities detection program completed'
    msg = MIMEText('The program that would find all ambiguities from running metamap with wsd turned on has been completed.\
Please look at the pickled file ' + pickle_fname + ' located in /data/ram/14k_collection/ directory')

    msg['Content-type'] = 'text/plain'
    msg['Subject'] = Subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    # send email to both Jorge and I (TODO: create a file holding list of emails that program should email to)
    server = smtplib.SMTP('smtp.uth.tmc.edu')
#    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
    
