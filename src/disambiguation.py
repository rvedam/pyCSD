# disambiguation.py
#
# parent program that tests all the different disambiguation algorithms
#

from concept_generation.sqlite_dict import SQLiteDict
from disambiguation.supervised.naive_bayes import NaiveBayes
import os, sys, cPickle as pickle

# The location of the UMLS CUI DB - maps CUIs to their definitions
UMLS_DB_LOCATION=os.path.normpath(os.path.expanduser("/data/ram/umlsdb.sqlite3"))

# parent directory of where the data is located
data_dir = '/data/ram/14k_collection'
sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
pmap_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap.chunkmap')
doc_concepts_dir = os.path.join(data_dir, 'concept_files')  # holds corpus of cui-mapped phrases sorted by document

# following constants is how we split the dataset. for NaiveBayes 
# we use a (train/test) 70/30 scheme.
# training_size = 9599
training_size = 1000
test_set = 4113

# unpickle ambiguities dictionary (phrase key multiple cuis)
ambigdict = pickle.load(open(os.path.join(data_dir, 'ambiguities.pkl'), 'rb+'))

# grab the UMLS_DB
umls = SQLiteDict(UMLS_DB_LOCATION)

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
    nfile = open(os.path.join(data_dir, 'trained_bayes.pkl'),'wb')
    pickle.dump(nbdisambigalgo, nfile)
    nfile.close()
    return nbdisambigalgo

nfile = os.path.join(data_dir, 'trained_bayes.pkl')
if os.path.isfile(nfile):
    nb = pickle.load(open(nfile, 'rb'))
else:
    print 'Trained model doesn\'t exist. Creating new trained Naive Bayes Model'
    nb = create_nb_classifier()
    print 'TRAINING COMPLETE'

phrase = raw_input('Enter phrase to disambiguate: ')

print nb.disambiguation(phrase)

