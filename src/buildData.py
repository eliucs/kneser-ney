import pickle
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import reuters
from utils import *

bigramFreqDist = {}
wordFreqDist = {}
sentTokens = []
countSentences = 0

START_TOKEN = '<START>'
END_TOKEN = '<END>'
FILTERS = ['<', '>', '&lt;', '(', ')', ',', '"', ':', '\t']

# For processing from Reuters corpora
for fileid in reuters.fileids():
    log('Processing', 0, fileid)
    sent = reuters\
        .raw(fileid)\
        .lower()\
        .replace('\n', '')\
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

        words.insert(0, START_TOKEN)
        words.append(END_TOKEN)

        # Add bigrams to bigrams
        for i in range(len(words) - 2):
            bigram = words[i], words[i+1]
            bigramFreqDist[bigram] = bigramFreqDist.get(bigram, 0) + 1

print(wordFreqDist)
print(bigramFreqDist)

wordFreqDistFile = open('data/word-freq-dist/wordFreqDist.pkl', 'wb')
pickle.dump(wordFreqDist, wordFreqDistFile)
wordFreqDistFile.close()

bigramFreqDistFile = open('data/bigram-freq-dist/bigramFreqDistFile.pkl', 'wb')
pickle.dump(bigramFreqDist, bigramFreqDistFile)
bigramFreqDistFile.close()