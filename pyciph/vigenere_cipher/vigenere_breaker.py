from pyciph.break_util.ngram_score import ngram_score
from pyciph.vigenere_cipher.vigenere import Vigenere
from itertools import permutations
import re

qgram = ngram_score('pyciph/break_util/english_quadgrams.txt')
trigram = ngram_score('pyciph/break_util/english_trigrams.txt')
ctext = 'Im wyeb kxfimo fpo imad amtvw mb neiv. Gmzbov ua msyqxk! Im wyeb kxfimo fpo imad amtvw mb neiv. Gmzbov ua msyqxk!'
ctext = re.sub('[^A-Z]', '', ctext.upper())

# an array that holds N best things. 
# It sorts elements and trims it to N elements whenever new elements are added
class nbest(object):
    def __init__(self,N=1000):
        self.store = []
        self.N = N
        
    def add(self,item):
        self.store.append(item)
        self.store.sort(reverse=True)    # sorts by the first tuple item (score) in each tuple in store
        self.store = self.store[:self.N] # trim array back to size N
    
    def __getitem__(self,k):             # allows indexing into classitself
        return self.store[k]

    def __len__(self):
        return len(self.store)

#init
N=100
for KLEN in xrange(3, 20): # for all keys 3-19
    rec = nbest(N)

    ###########################################################################
    # Step 1: Start by finding nbest 3-permutations of the alphabet for PARENT keys
    ###########################################################################
    for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ',3): # 26P3 = 26*25*24 = 15600
        perm3 = ''.join(i)                     # concat the tuple of 3 chars to a string
        key =  perm3 + 'A'*(KLEN-len(perm3))   # A's will ensure we only decrypt snippits of ct 
        pt = Vigenere(key).decrypt(ctext)
        
        # score the resulting plaintext snippets using trigram scoring
        score = 0
        for j in range(0, len(ctext), KLEN):    # 0-len(ctext) in increments of KLEN
            score += trigram.score(pt[j:j+3])   # Sum the scores of the sets of 3 plaintext letters that were decrypted
        rec.add((score, perm3, pt[:30]))        # Make tuple with score for perm3. Add to rec
        
    ###########################################################################
    # Step 2: 1) Find next best single character to add and add it. 2) Repeat for all nbest keys.
    #         3) Repeat steps 1,2 until all nbest key lengths are length KLEN
    # NOTE: Checking ALL keys would have been O(26^N)
    #       Complexity is KLEN*N*26 which is O(N) because we deal with 26 next characters individually (linearly)
    ###########################################################################
    for x in range(0, KLEN-3): # add KLEN-3 many single characters because we already have 3 for each key
        next_rec = nbest(N)    # set next_rec to a new nbest object
        for i in xrange(N):    # for all N best
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                key = rec[i][1] + c   # try adding single character c to key
                paddedKey = key + 'A'*(KLEN-len(key))
                pt = Vigenere(paddedKey).decrypt(ctext)

                # score the resulting plaintext snippets using quadgram scoring
                score = 0
                for j in range(0, len(ctext), KLEN):
                    score += qgram.score(pt[j:j+len(key)])
                next_rec.add((score, key, pt[:30]))
        rec = next_rec 

    ###########################################################################
    # Step 3: 'rec' now contains the nbest keys of length KLEN
    # NOTE: The keys are already ordered by scores of SNIPPETS of the pt.
    #       Now we need to decrypt the FULL ct with each key and see which has the highest score
    ###########################################################################
    bestkey = rec[0][1]           # initialize best key and best score
    pt = Vigenere(bestkey).decrypt(ctext)
    bestscore = qgram.score(pt)
    for i in range(N):
        pt = Vigenere(rec[i][1]).decrypt(ctext)
        score = qgram.score(pt)  
        if score > bestscore:     # update best key and best score if necessary
            bestkey = rec[i][1]
            bestscore = score

    # Print the winning key for this key length
    bestMsg = Vigenere(bestkey).decrypt(ctext)
    print "{0:.2f} klen: {1:2} key: \"{2}\" : {3}".format(bestscore, KLEN, bestkey, bestMsg)

    