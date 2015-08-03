'''
CREDIT: http://practicalcryptography.com/media/cryptanalysis/files/ngram_score_1.py
Allows scoring of text using n-gram probabilities
17/07/12
'''
from math import log10

class ngram_score(object):
    def __init__(self, ngramfile, sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        for line in file(ngramfile):
            seq,count = line.split(sep) 
            self.ngrams[seq] = int(count)
        self.L = len(seq)                       # length of char sequences (bigram=2, trigram=3, etc.)
        self.N = sum(self.ngrams.itervalues())  # Sums values in dict. Result is sum of # of occurances of each ngram
        # calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)  # log(count/total)
        self.floor = log10(0.01/self.N)         # Default score to give if the sequence was not found in the dict

    # Sums log probabilities already stored in dict. Based off of basic probability:
    # p(ATTA) = count(ATTA) / N   ;  count(ATTA) = number of times ATTA was found in sample, N = total number of ngrams
    # p(ATTACK) = p(ATTA) * p(TTAC) * p(TACK)
    # log(p(ATTACK)) = log(p(ATTA)) + log(p(TTAC)) + log(p(TACK))
    def score(self, text):
        ''' compute the score of text '''
        score = 0
        getLogScore = self.ngrams.__getitem__
        for i in xrange(len(text)-self.L+1):    # xrange wont actually create the list in memory. Lazily iterates instead.
            if text[i:i+self.L] in self.ngrams: 
                score += getLogScore(text[i:i+self.L])
            else: 
                score += self.floor
        return score
       
