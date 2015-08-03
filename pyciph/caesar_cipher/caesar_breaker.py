import re
from pyciph.break_util.ngram_score import ngram_score
from pyciph.caesar_cipher.caesar import Caesar

fitness = ngram_score('pyciph/break_util/english_quadgrams.txt') # load our quadgram statistics

def break_caesar(ctext):
	''' Take ciphertext as input and return the most probable shift key and it's ngram score in a tuple'''
	# remove spacing/punc and uppercase the ciphertext
	ctext = re.sub('[^A-Z]','',ctext.upper())
	# try all possible keys, return the one with the highest fitness
	scores = []
	for i in range(26):
		score = fitness.score(Caesar(i).decrypt(ctext))
		scores.append( (score, i) )
		print "Shift: {0:2} Score: {1:.2f}".format(i, score)
	return max(scores)

ctext = "Zh pxvw dwwdfn wkh hdvw zdoov dw gdzq. Zlqwhu lv frplqj!"
score, key = break_caesar(ctext)

print "Best candidate was key \'{0}\':".format(key)
print Caesar(key).decrypt(ctext)