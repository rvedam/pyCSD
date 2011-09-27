#!/usr/local/bin/python -Wall

import os, subprocess, sys, nltk

def filter_candidate_concepts(sys_output):
#	phraseIdx = [sys_output.index(sent) for sent in sys_output if 'Phrase' in sent][0]
#	metaMapIdx = [sys_output.index(sent) for sent in sys_output if 'Meta Mapping' in sent][0]
	phraseIdx = -1
	metaMapIdx = -1
	mMapFound = False	
	sentences = sys_output.split('\n')
	for sent in sentences:
		if mMapFound:
			break
		if 'Phrase' in sent:
			phraseIdx = sys_output.index(sent)
		if 'Meta Mapping' in sent:
			metaMapIdx = sys_output.index(sent)
			mMapFound = True
	result = [w for w in sys_output[phraseIdx:metaMapIdx].split('\n')[2:]]
	return result	

def retrieve_concepts(query):
	process = subprocess.Popen(['echo', query], shell=False, stdout=subprocess.PIPE)
	mm_process = subprocess.Popen(['data_disk/public_mm/bin/metamap10', '-A'], shell=False, stdin=process.stdout, stdout=subprocess.PIPE)

	# allow mm_process to receive SIGPIPE if p2 exits.
	process.stdout.close()
	metamap_output = mm_process.communicate()[0]
	# print metamap_output
	return filter_candidate_concepts(metamap_output)

