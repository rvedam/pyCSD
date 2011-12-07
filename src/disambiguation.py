# disambiguation.py
#
# parent program that tests all the different disambiguation algorithms
#

from concept_generation.sqlite_dict import SQLiteDict
from disambiguation.supervised.naive_bayes import NaiveBayes
import os, sys, cPickle as pickle

# The location of the UMLS CUI DB - maps CUIs to their definitions
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("/data/ram/umlsdb.sqlite3"))
# TODO make FILE to load a command-line parameter
TRAINED_BAYES_FILE = 'trained_bayes_span_set.pkl'

# parent directory of where the data is located
data_dir = '/data/ram/14k_collection'
sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
doc_concepts_dir = os.path.join(data_dir, 'concept_files')  # holds corpus of cui-mapped phrases sorted by document

# following constants is how we split the dataset. for NaiveBayes 
# we use a (train/test) 70/30 scheme.
training_size = 13172

# unpickle ambiguities dictionary (phrase key multiple cuis)
ambigdict = pickle.load(open(os.path.join(data_dir, 'ambiguities_bayes.pkl'), 'rb+'))

# grab the UMLS_DB
umls = SQLiteDict(UMLS_DB_LOCATION)

# TODO: Need to parallelize Training of Naive Bayes
# grab instance of NaiveBayes algorithm (we will be
def create_nb_classifier():
    nbdisambigalgo = NaiveBayes(training_size, sent_file_path)
    tr_file_set = set()
    test_set = set()
    t_count = 0
    for dname, sdname, fnames in os.walk(doc_concepts_dir):
        for fname in fnames:
            fpath = os.path.join(dname, fname)
            if t_count < int(training_size):
                t_count += 1
                tr_file_set.add(fpath)
            else:
                test_set.add(fpath)

    nbdisambigalgo.train(tr_file_set)

    # pickle the trained data model
    print 'WRITING OUT TRAINED MODEL. PLEASE WAIT...'
    nfile = open(os.path.join(data_dir, TRAINED_BAYES_FILE),'wb')
    pickle.dump(nbdisambigalgo, nfile, pickle.HIGHEST)
    nfile.close()
    print 'TRAINED MODEL BACKED UP.\n TRAINING PROCESS COMPLETE'
    return nbdisambigalgo

print 'loading naive bayes model'
nfile = os.path.join(data_dir, TRAINED_BAYES_FILE)
if os.path.isfile(nfile):
    nf = open(nfile, 'rb')
    nb = pickle.load(nf)
    nf.close()
    print 'model loaded'
else:
    print 'Trained model doesn\'t exist. Creating new trained Naive Bayes Model'
    nb = create_nb_classifier()
    print 'TRAINING COMPLETE'

done = False
while not done:
    phrase = raw_input('Enter phrase to disambiguate: ')
    print nb.disambiguation(phrase)
    complete = raw_input('More phrase to disambiguate(y/n)?: ')
    if complete.lower() == 'n':
        done = True

