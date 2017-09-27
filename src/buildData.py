"""

    buildData.py

    This module is used for building up the word and bigram frequency distribution
    dictionaries from the following NLTK corpora:
        - Reuters
        - Brown
        - Webtext
        - Inaugural Address

"""


import pickle
from nltk import sent_tokenize
from nltk.corpus import brown, reuters, inaugural, webtext
from utils import *


START_TOKEN = '<START>'
END_TOKEN = '<END>'
FILTERS = ['<', '>', '&lt;', '(', ')', ',', '"', ':', '\t', '--', '*',
           '!', '?', '/ul', '\\r']
FILTERS_SINGLE_SYMBOL = ['<', '>', '(', ')', ',', '"', ':', '.', '`', '``',
                         "'", '.', '?', '!', "''", '-', '--', '---', ';']

wordFreqDist = {}
bigramFreqDist = {}
sentTokens = []


def processCorpora(corpora):
    for fileid in corpora.fileids():
        log('Processing', 0, fileid)
        sent = corpora \
            .raw(fileid) \
            .lower() \
            .replace('\n', '') \
            .replace('  ', ' ')
        sent = sent_tokenize(sent)

        for s in sent:
            words = []
            for w in s.split(' '):
                if not w:
                    continue
                elif isNumber(w):
                    continue
                elif w.endswith('.'):
                    w = w[:-1]
                for ft in FILTERS:
                    w = w.replace(ft, '')

                # The filtering step may have reduced the word
                # down to the null string:
                if not w:
                    continue

                words.append(w)

                wordFreqDist[w] = wordFreqDist.get(w, 0) + 1

            if len(words) == 0:
                continue

            words.insert(0, START_TOKEN)
            words.append(END_TOKEN)

            # Add bigram to bigrams
            for i in range(len(words) - 2):
                bigram = words[i], words[i+1]
                bigramFreqDist[bigram] = bigramFreqDist.get(bigram, 0) + 1


def processBrownCorpora():
    for fileid in brown.fileids():
        log('Processing', 0, fileid)
        sent = brown.sents(fileid)

        for s in sent:
            words = []
            for w in s:
                if not w:
                    continue
                elif isNumber(w):
                    continue
                elif w.endswith('.'):
                    w = w[:-1]

                w = w.lower()

                for ft in FILTERS:
                    w = w.replace(ft, '')

                skipSingleSymbol = False
                for ft in FILTERS_SINGLE_SYMBOL:
                    if w == ft:
                        skipSingleSymbol = True

                if skipSingleSymbol:
                    continue

                # The filtering step may have reduced the word
                # down to the null string:
                if not w:
                    continue

                words.append(w)

                wordFreqDist[w] = wordFreqDist.get(w, 0) + 1

            if len(words) < 2:
                continue

            words.insert(0, START_TOKEN)
            words.append(END_TOKEN)

            # Add bigram to bigrams
            for i in range(len(words) - 2):
                bigram = words[i], words[i+1]
                bigramFreqDist[bigram] = bigramFreqDist.get(bigram, 0) + 1


def main():
    # Process corporas, the Brown corpora is done separately because its
    # sentence tokenized format is different from the rest:
    for corpora in [reuters, webtext, inaugural]:
        processCorpora(corpora)
    processBrownCorpora()

    print(wordFreqDist)
    print(bigramFreqDist)

    wordFreqDistFile = open('data/word-freq-dist/wordFreqDist.pkl', 'wb')
    pickle.dump(wordFreqDist, wordFreqDistFile)
    wordFreqDistFile.close()

    bigramFreqDistFile = open('data/bigram-freq-dist/bigramFreqDistFile.pkl', 'wb')
    pickle.dump(bigramFreqDist, bigramFreqDistFile)
    bigramFreqDistFile.close()


main()
