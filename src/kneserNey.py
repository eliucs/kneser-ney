"""

    kneserNey.py

    This module is for the Kneser-Ney Smoothing algorithm.

"""


START_TOKEN = '<START>'
END_TOKEN = '<END>'
NUM_WORDS = '<NUM_WORDS>'
NUM_BIGRAMS = '<NUM_BIGRAMS>'


class KneserNey:

    def __init__(self, bigramFreqDist, discount):
        self.bigramFreqDist = bigramFreqDist
        self.discount = discount

    def getBigramFreqDist(self):
        return self.bigramFreqDist

    def getWordFreqDist(self):
        return self.wordFreqDist

    def __interpolate(self, w):
        return (self.discount/self.bigramFreqDist[w]['count']) * \
               len(list(self.bigramFreqDist[w]['preceding'].keys()))

    def __continuation(self, w):
        return len(list(self.bigramFreqDist[w]['following'].keys()))/\
               self.bigramFreqDist[NUM_BIGRAMS]

    def __predictBigram(self, w1, w2):
        interpolation = self.__interpolate(w2)
        continuation = self.__continuation(w1)
        return max(self.bigramFreqDist[w1]['following'].get(w2, 0) -
                   self.discount, 0)/self.bigramFreqDist[w2]['count'] + \
               interpolation * continuation

    def predictNextWord(self, w):
        if w not in self.bigramFreqDist:
            return []

        probabilityDist = []

        for key in self.bigramFreqDist[w]['preceding'].keys():
            probability = self.__predictBigram(key, w)
            probabilityDist.append((key, probability))

        probabilityDist.sort(key=lambda x: x[1])

        if len(probabilityDist) > 5:
            probabilityDist = probabilityDist[:5]

        probabilityDist.reverse()

        return probabilityDist
