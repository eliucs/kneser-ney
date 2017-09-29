"""

    buildBigramFreqDist.py

    This module is used for building up the word and bigram frequency
    distribution dictionaries, with the option of the following NLTK
    corpora:
        - Reuters
        - Brown
        - Webtext
        - Inaugural

"""


import os
import pickle
from nltk import sent_tokenize
from nltk.corpus import reuters, brown, webtext, inaugural
from utils import *


START_TOKEN = '<START>'
END_TOKEN = '<END>'
NUM_WORDS = '<NUM_WORDS>'
NUM_BIGRAMS = '<NUM_BIGRAMS>'
FILTERS = ['<', '>', '(', ')', '[', ']', '&lt;', ':', ';', '-', '--', '*',
           '!', '?', '.', '\t', '\n', '\r', ',', '/', '"']
FILTERS_SINGLE_SYMBOL = ['<', '>', '(', ')', ',', '"', ':', '.', '`', '``',
                         "'", '.', '?', '!', "''", '-', '--', '---', ';']

bigramFreqDist = {}

# Initialize bigramFreqDist with START_TOKEN, END_TOKEN, NUM_WORDS, NUM_BIGRAMS:
bigramFreqDist[START_TOKEN] = {
    'preceding': {},
    'following': {},
    'count': 0
}

bigramFreqDist[END_TOKEN] = {
    'preceding': {},
    'following': {},
    'count': 0
}

bigramFreqDist[NUM_WORDS] = 0
bigramFreqDist[NUM_BIGRAMS] = 0


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
                elif w.endswith('.'):
                    w = w[:-1]
                for ft in FILTERS:
                    w = w.replace(ft, '')

                # The filtering step may have reduced the word
                # down to the null string:
                if not w:
                    continue

                if isNumber(w):
                    continue

                if '-' in w:
                    continue

                # print(w)

                words.append(w)

                if not bigramFreqDist.get(w):
                    bigramFreqDist[w] = {
                        'preceding': {},
                        'following': {},
                        'count': 1
                    }
                    bigramFreqDist[NUM_WORDS] += 1
                else:
                    bigramFreqDist[w]['count'] += 1

            if len(words) == 0:
                continue

            words.insert(0, START_TOKEN)
            words.append(END_TOKEN)

            bigramFreqDist[START_TOKEN]['count'] += 1
            bigramFreqDist[END_TOKEN]['count'] += 1

            # Add bigrams to bigramFreqDist:
            for i in range(len(words) - 2):
                bigramFreqDist[words[i]]['preceding'][words[i+1]] = \
                    bigramFreqDist[words[i]]['preceding'].get(words[i+1], 0) + 1
                bigramFreqDist[words[i+1]]['following'][words[i]] = \
                    bigramFreqDist[words[i+1]]['following'].get(words[i], 0) + 1
                bigramFreqDist[NUM_BIGRAMS] += 1


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

                if not bigramFreqDist.get(w):
                    bigramFreqDist[w] = {
                        'preceding': {},
                        'following': {},
                        'count': 1
                    }
                    bigramFreqDist[NUM_WORDS] += 1
                else:
                    bigramFreqDist[w]['count'] += 1

            if len(words) == 0:
                continue

            words.insert(0, START_TOKEN)
            words.append(END_TOKEN)

            bigramFreqDist[START_TOKEN]['count'] += 1
            bigramFreqDist[END_TOKEN]['count'] += 1

            # Add bigrams to bigramFreqDist:
            for i in range(len(words) - 2):
                bigramFreqDist[words[i]]['preceding'][words[i+1]] = \
                    bigramFreqDist[words[i]]['preceding'].get(words[i+1], 0) + 1
                bigramFreqDist[words[i+1]]['following'][words[i]] = \
                    bigramFreqDist[words[i+1]]['following'].get(words[i], 0) + 1
                bigramFreqDist[NUM_BIGRAMS] += 1


def main():

    processCorpora(inaugural)

    for key in list(bigramFreqDist.keys())[:5]:
        print(key, bigramFreqDist[key])

    print('  Num Words: ', bigramFreqDist[NUM_WORDS])
    print('Num Bigrams: ', bigramFreqDist[NUM_BIGRAMS])

    bigramFreqDistFile = open(os.path.abspath('data/bigram-freq-dist/bigramFreqDist.pkl'), 'wb')
    pickle.dump(bigramFreqDist, bigramFreqDistFile)
    bigramFreqDistFile.close()

main()
