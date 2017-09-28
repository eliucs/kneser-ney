"""

    kneserNey.py

    This module is for the Kneser-Ney Smoothing algorithm.

"""


class KneserNey:

    def __init__(self, bigramFreqDist, wordFreqDist, discount):
        self.bigramFreqDist = bigramFreqDist
        self.wordFreqDist = wordFreqDist
        self.discount = discount

    def getBigramFreqDist(self):
        return self.bigramFreqDist

    def getWordFreqDist(self):
        return self.wordFreqDist

    def __wordFreq(self, w):
        return self.wordFreqDist.get(w, 0)

    def __bigramFreq(self, w1, w2):
        w1Preceding = 0
        w1Following = 0
        w2Preceding = 0
        w2Following = 0
        for bigram in self.bigramFreqDist.keys():
            if w1 == bigram[0]:
                w1Preceding += 1
            if w2 == bigram[0]:
                w2Preceding += 1
            if w1 == bigram[1]:
                w1Following += 1
            if w2 == bigram[1]:
                w2Following += 1
        return ((w1Preceding, w1Following), (w2Preceding, w2Following))

    def __interpolate(self, w, bigramsPreceding):
        if w not in self.wordFreqDist:
            return 0
        return (self.discount/self.wordFreqDist[w]) * bigramsPreceding

    def __continuation(self, w, bigramsFollowing):
        if w not in self.wordFreqDist:
            return 0
        return bigramsFollowing/len(self.bigramFreqDist.keys())

    def __predictBigram(self, w1, w2):
        bigramFreq = self.__bigramFreq(w1, w2)
        w1Following = bigramFreq[0][1]
        w2Preceding = bigramFreq[1][0]

        interpolation = self.__interpolate(w2, w2Preceding)
        continuation = self.__continuation(w1, w1Following)

        return max(self.bigramFreqDist.get((w2, w1), 0) - self.discount, 0)/\
            self.__wordFreq(w2) + interpolation * continuation

    def predictNextWord(self, w):
        probabilityDist = []
        wordsFollowing = []

        for bigram in self.bigramFreqDist.keys():
            if w == bigram[0]:
                wordsFollowing.append(bigram[1])

        for word in wordsFollowing:
            probability = self.__predictBigram(word, w)
            probabilityDist.append((word, probability))
            print(word, probability)

        probabilityDist.sort(key=lambda x:x[1])

        if len(probabilityDist) > 5:
            probabilityDist = probabilityDist[:5]

        probabilityDist.reverse()
        print(probabilityDist)

        return probabilityDist
