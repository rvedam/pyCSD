from disambiguation.supervised.lesk_algo import LeskAlgo
import os, cPickle as pickle

data_dir = '/data/ram/14k_collection'
sent_file_path = os.path.join(data_dir, 'full_text_with_abstract_and_title.metamap')
ambig_file_path = os.path.join(data_dir, 'ambiguities_context_spans.pkl')

# create new Lesk Instance
print 'Loading Lesk\'s algorithm'
lesk = LeskAlgo(sent_file_path, ambig_file_path)
print 'Loaded'

done = False
while not done:
    query = raw_input('Enter phrase to disambiguate: ')
    context = lesk.get_ambig_dict().get_sentence_nos(query)[0]
    print 'DISAMBIGUATING ', query, ' within context "', lesk.get_sentence(context), '"'
    print 'DISAMBIGUATED CUI: ', lesk.disambiguation(query, context)
    finished = raw_input('Any more queries?(y/n): ')
    if 'n' == finished.lower():
        done = True

