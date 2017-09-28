import os
import pickle
from kneserNey import *


def main():
    wordFreqDist = {}
    bigramFreqDist = {}

    with open(os.path.abspath('data/word-freq-dist/wordFreqDist.pkl'), 'rb') as file:
        wordFreqDist = pickle.load(file)

    with open(os.path.abspath('data/bigram-freq-dist/bigramFreqDist.pkl'), 'rb') as file:
        bigramFreqDist = pickle.load(file)

    kn = KneserNey(bigramFreqDist, wordFreqDist, 0.75)
    kn.buildBigramProbabilityDist()


main()
