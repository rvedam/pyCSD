# umls_concept_extractor
#
# Given a document or a corpus of text (formatted in a specific way)
# this program will tokenize, and extract UMLS concepts from the texts.
#

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Ramnarayan Vedam"
__date__ ="$Sep 11, 2011 9:56:52 PM$"

from com.vrn.utils import MetaMapWrapper
from gov.nih.nlm.nls.metamap import Ev

if __name__ == "__main__":
    umls = MetaMapWrapper("localhost", 8066)
    results = umls.retrieveConcepts("lab culture")
    for result in results:
        for candidate in umls.retrieveCandidates(result):
            print candidate.getConceptId(), " ", candidate.getConceptName()