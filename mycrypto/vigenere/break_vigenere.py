from ngram_score import ngram_score
from vigenere_cipher import vigenere_cipher
import re
from itertools import permutations

qgram = ngram_score('./caesar_break/english_quadgrams.txt')
trigram = ngram_score('./caesar_break/english_trigrams.txt')
ctext = 'kiqpbkxspshwehospzqhoinlgapp'
ctext = 'Im wyeb kxfimo fpo imad amtvw mb neiv. Gmzbov ua msyqxk! Im wyeb kxfimo fpo imad amtvw mb neiv. Gmzbov ua msyqxk!'
ctext = re.sub('[^A-Z]', '', ctext.upper())

# keep a list of the N best things we have seen, discard anything else
class nbest(object):
    def __init__(self,N=1000):
        self.store = []
        self.N = N
        
    def add(self,item):
        self.store.append(item)
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]
    
    def __getitem__(self,k):  # allows indexing into class
        return self.store[k]

    def __len__(self):
        return len(self.store)

#init
N=100
for KLEN in xrange(3,20): # for all keys 3-19
    rec = nbest(N)
    for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ',3): # 26P3 = 26*25*24 = 15600
        key = ''.join(i) + 'A'*(KLEN-len(i))               # A's will enusre we only decrpyt snippits of ct 
        pt = vigenere_cipher(ctext, key, decrypt=True)
        score = 0
        print pt
        for j in range(0,len(ctext),KLEN):    # 0-len(ctext) in increments of KLEN
            score += trigram.score(pt[j:j+3])
            print j, pt[j:j+3], score
        rec.add((score,''.join(i),pt[:30]))
        exit()
    for i in range(0, len(rec)):
        print rec[i]
    exit()
    next_rec = nbest(N)
    for i in range(0,KLEN-3):
        for k in xrange(N):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key = rec[k][1] + c
                fullkey = key + 'A'*(KLEN-len(key))
                pt = vigenere_cipher(ctext, fullkey, decrypt=True)
                score = 0
                for j in range(0,len(ctext),KLEN):
                    score += qgram.score(pt[j:j+len(key)])
                next_rec.add((score,key,pt[:30]))
        rec = next_rec
        next_rec = nbest(N)
    bestkey = rec[0][1]
    pt = vigenere_cipher(ctext, bestkey, decrypt=True)
    bestscore = qgram.score(pt)
    for i in range(N):
        pt = vigenere_cipher(ctext, rec[i][1], decrypt=True)
        score = qgram.score(pt)
        if score > bestscore:
            bestkey = rec[i][1]
            bestscore = score
    print "{0:.2f} klen: {1:2} key: \"{2}\" : {3}".format(bestscore, KLEN, bestkey, vigenere_cipher(ctext, bestkey, decrypt=True))
    #print bestscore,'Vigenere, klen',KLEN,':"'+bestkey+'",',vigenere_cipher(ctext, bestkey, decrypt=True)
    

