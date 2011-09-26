#
# utils.py
#
# contains a series of functions that would be useful in generating concepts
#

__author__="Ramnarayan Vedam"
__date__ ="$Sep 25, 2011 11:04:27 PM$"

from collections import deque

def generate_ngrams(aString, stopwords, ngram_size, tok_sep=' '):
    '''generate ngrams of size <ngram_size>'''
    ngram=deque()
    all_ngrams = []
    tokens = [word for word in aString.split(tok_sep) if word not in stopwords]
    for token in tokens:
        if len(token):
            ngram.append(token)
        if len(ngram) >= ngram_size:
            all_ngrams.append(tok_sep.join(ngram))
            ngram.popleft()
    return all_ngrams


if __name__ == "__main__":
    stopwords=['the']
    ngrams = generate_ngrams('the cat chased the dog', stopwords, 2)
    print ngrams