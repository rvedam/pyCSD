import multiprocessing 
import sys, cPickle as pickle, cStringIO as StringIO, math, csv
import os.path   # Platform-independent path manipulation
import time
import smtplib
from email.mime.text import MIMEText
from analysis.ambig_dict import ContextSpanAmbigDict

# some tracker global variables used to populate AmbigDict Instance

context_span_dict  = dict()

def find_span_ambiguities(data_dir):
    '''
    function will find ambiguities for each span within a given context. This function
    assumes the context is the actual sentence that has been passed into Metamap.
    '''
    sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
    output_file_dir = os.path.join(data_dir, 'concept_files')
    sent_map = dict()
    sentMapData = open(sent_file_path, 'rU')
    for sentData in sentMapData.readlines():
        sentence = sentData.split('|')
        sent_map[sentence[0]] = sentence[1]
    sentMapData.close()

    cur_sentence = ''
    completed_file_num = 0
    for document in os.listdir(output_file_dir):
        phrase_cui_file = open(os.path.join(output_file_dir, document), 'rU')
        for phrase_cui_line in phrase_cui_file.readlines():
            if '|' not in phrase_cui_line:
                continue
            phrase_cui_comp = phrase_cui_line.split('|')
            cui = ''
            try:
                cui = phrase_cui_comp[2]
            except IndexError:
                print 'phrase_cui_comp: ', phrase_cui_comp
                sys.exit(1)
            
            # find the sentence where the phrase is located and keep track of it
            sent_no = phrase_cui_comp[0].zfill(10)
            sentence = sent_map[sent_no]
            
            if cur_sentence == '' or cur_sentence != sent_no:
                cur_sentence = sent_no

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
                if sent_no not in context_span_dict:
                    context_span_dict[sent_no] = dict() # sent_no indicates context

                # add dictionary of   
                if phrase not in context_span_dict[sent_no]:
                    context_span_dict[sent_no][phrase] = set()
                    #sent_no_dict[phrase] = set()
 
                context_span_dict[sent_no][phrase].add(cui)
                #sent_no_dict[phrase].add(sent_no)
        completed_file_num += 1
        if completed_file_num % 100 == 0:
            print 'PROCESSED %d DOCUMENTS' % completed_file_num
        phrase_cui_file.close()

    final_context_span_dict = ContextSpanAmbigDict()
    for sentKey in context_span_dict.keys():
        for phrase in context_span_dict[sentKey].keys():
            if len(context_span_dict[sentKey][phrase]) > 1:
                # create the dictionary for the given sentence since NOW there exists at least a
                # single phrase that has an ambiguity
                #if sentKey not in final_context_span_dict:
                #    final_context_span_dict[sentKey] = dict()
                #final_context_span_dict[sentKey][phrase] = context_span_dict[sentKey][phrase]
                final_context_span_dict.add_entry(phrase, sentKey, context_span_dict[sentKey][phrase])
    return final_context_span_dict

if __name__ == "__main__":
    data_dir = '/data/ram/14k_collection/'
    pickle_fname = 'ambiguities_context_spans.pkl'
    print 'FINDING AMIBIGUITIES INSIDE DATASET PROVIDED IN DATA_DIR: ', data_dir
    # pickle the final set of ambiguities to a file
    ambig_file_path = os.path.join(data_dir, pickle_fname)

    # grab all ambiguities in the corpus
    ambig_word_concept_dict = find_span_ambiguities(data_dir)
    print 'pickling data'
    ambig_file = open(ambig_file_path, 'wb+')
    try:
        pickle.dump(ambig_word_concept_dict, ambig_file)
    finally:
        ambig_file.close()
    print 'pickling data complete'
    print 'PROCESS COMPLETE'
    fromaddr = 'Ramnarayan.Vedam@uth.tmc.edu'
    toaddrs = "Ramnarayan.Vedam@uth.tmc.edu"

    Subject = 'Span Context Ambiguities detection program completed'
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
    
