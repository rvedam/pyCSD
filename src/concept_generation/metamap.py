#!/usr/local/bin/python -Wall

import os, subprocess, sys, nltk

metamap_path = '/opt/public_mm/bin/metamap11'

def filter_candidate_concepts(sys_output): 
    # rewrite the filter to deal with candidates in MMI format
    split_output = sys_output.split('\n')
    result = []
    for line in split_output:
        if '|MM|' in line:
            result.append(line)
    return result

def retrieve_concepts(query): 
    process = subprocess.Popen(['echo', query], shell=False, stdout=subprocess.PIPE) 
    mm_process = subprocess.Popen([metamap_path, '-A -N -y'], shell=False, stdin=process.stdout, stdout=subprocess.PIPE)
    # allow mm_process to receive SIGPIPE if p2 exits. 
    process.stdout.close() 
    metamap_output = mm_process.communicate()[0]
    # print metamap_output 
    return filter_candidate_concepts(metamap_output)

if __name__ == '__main__':
    if sys.argv[0] == 'python':
        query = "".join(sys.argv[2:])
        print query
        print retrieve_concepts(query)
    else:
        query = "".join(["".join([w, ' ']) for w in sys.argv[1:]])
        print query
        print retrieve_concepts(query)
