"""

    buildBigramProbabilityDist.py

    This module is to precompute the bigram probability distribution table,
    where for each word, the probabilities of the top 5 following words
    are computed.

"""


import os
import pickle
from kneserNey import *


def main():
    wordFreqDist = {}
    bigramFreqDist = {}
    bigramProbDist = {}

    with open(os.path.abspath('data/word-freq-dist/wordFreqDist.pkl'), 'rb') as file:
        wordFreqDist = pickle.load(file)

    with open(os.path.abspath('data/bigram-freq-dist/bigramFreqDist.pkl'), 'rb') as file:
        bigramFreqDist = pickle.load(file)

    kn = KneserNey(bigramFreqDist, wordFreqDist, 0.75)

    for w in wordFreqDist.keys():
        bigramProbDist[w] = kn.predictNextWord(w)

    bigramProbDistFile = open(os.path.abspath('data/bigram-prob-dist/bigramProbDist.pkl'), 'wb')
    pickle.dump(bigramProbDist, bigramProbDistFile)
    bigramProbDistFile.close()

main()
