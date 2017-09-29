"""

    buildBigramProbDist.py

    This module is used for preprocessing the bigram probability
    distribution dictionary from the bigram frequency distribution
    dictionary.

"""

import os
import pickle
from src.kneserNey import KneserNey


def main():
    bigramProbDist = {}

    with open(os.path.abspath('data/bigram-freq-dist/bigramFreqDist.pkl'), 'rb') as file:
        bigramFreqDist = pickle.load(file)

    kn = KneserNey(bigramFreqDist, 0.75)

    for key in bigramFreqDist.keys():
        try:
            bigramProbDist[key] = kn.predictNextWord(key)
            print(kn.predictNextWord(key))
        except TypeError:
            continue

    bigramProbDistFile = open('data/bigram-prob-dist/bigramProbDist.pkl', 'wb')
    pickle.dump(bigramProbDist, bigramProbDistFile)
    bigramProbDistFile.close()

main()
