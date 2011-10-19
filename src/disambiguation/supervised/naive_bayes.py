# naive_bayes.py
#
# naive bayes classification for concept sense disambiguation
#

from collections import defaultdict
import math, cPickle as pickle, os, sys

class NaivesBayes:
    def __init__(self, tr_size, sent_file_path):
        self.concept_prob = {}  # will hold the concept sense probabilities
        self.tr_size = tr_size
        # the following hashtable that will number of times words occur in 
        # corpus
        self.corpus_word_count = {}         
        # the following hashtable that will number of times words occurs in 
        # phrase that contains a particular concept
        self.corpus_word_concept_count = {} 
        # this will keep track for each phrase, the list of CUIs mapped to it. 
        self.word_concept_map = {}
        self.sent_map = {}
        sent_file = open(sent_file_path, 'rU')
        for sentData in sent_file.readlines():
            sentence = sentData.split('|')
            self.sent_map[sentence[0]] = sentence[1]

    def training(self, training_data_files):
        '''trains bayesian model for concept sense disambiguation.'''
        # assign all concept's probabilities their appropriate mapping probability as returned
        # by metamap.
        fcount = 0
        for fname in training_data_files:
            fcount = fcount + 1
            per_complete = (fcount*1.0/580)*100
            if per_complete % 10 == 0:
                print per_complete, '% complete'
            data_file = open(fname, 'rU')
            for line in data_file.readlines():
                split_line = line.split(',')
                cui = split_line[2]
                # make the first confidence score metamap uses the initial probability of the sense
                if cui not in self.concept_prob.keys():
                    self.concept_prob[cui] = split_line[1]
                # create a dictionary to keep track of word counts for a given sense.
                if cui not in self.corpus_word_concept_count.keys():
                    self.corpus_word_concept_count[cui] = {}
                # count the words inside the phrase for which the context has been extracted
                for word in split_line[3].split(' '):
                    if word in self.corpus_word_count.keys():
                        self.corpus_word_count[word] = self.corpus_word_count[word] + 1
                    else:
                        self.corpus_word_count[word] = 1
                    if word in self.corpus_word_concept_count[cui]:
                        self.corpus_word_concept_count[cui][word] += 1
                    else:
                        self.corpus_word_concept_count[cui][word] = 1
                if split_line[3] not in self.word_concept_map.keys():
                    self.word_concept_map[split_line[3]] = []
                self.word_concept_map[split_line[3]].append(cui)
    def disambiguation(self, phrase):
        '''
        disambiguates set of concepts for a given input with 
        multiple mappings.
        '''
        try:
            c_scores = {}
            for cui in self.word_concept_map[phrase]:
                c_scores[cui] = math.log(concept_prob[cui])
                for word in phrase.split(' '):
                    c_scores[concept] += math.log(self.corpus_word_concept_count[cui][word]/self.corpus_word_count[word])
            # find the maximum concept
            disamb_concept, cur_max = "", 0
            for concept in c_scores.keys():
                if c_scores[concept] > cur_max:
                    disamb_concept, cur_max = concept, c_scores[concept]
            return max_concept
        except KeyError:
            print 'phrase never encountered in corpus'

if __name__ == "__main__":
    dir_path = ""
    tr_size = -1
    dir_path = sys.argv[1]
    tr_size = sys.argv[2]
    training_set_paths = []
    test_set_paths = []
    
    # define documents that will go into training set and documents that will
    # be used for the testing of the naive bayes method.
    t_count = 0
    for dname, sdname, fnames in os.walk(dir_path):
        for fname in fnames:
            fpath = os.path.join(dname, fname)
            if t_count < int(tr_size):
                t_count = t_count + 1
                training_set_paths.append(fpath)
            else:
                test_set_paths.append(fpath)
    
    classifier = NaivesBayes(tr_size)
    print 'TRAINING AGENT'
    classifier.training(training_set_paths)
    print 'TRAINING AGENT COMPLETED'
    print classifier.disambiguation('Environmental Protection Agency')
