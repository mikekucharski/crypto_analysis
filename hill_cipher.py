#!/usr/bin/env python
import argparse
import numpy
import math
import sys

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
						"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
						"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
						"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", ".", 
						"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "=", "?", 
						"[", "]", "{", "}", ";", ":", ",", "<", ">", "'", " "]
MOD_SIZE = len(ALPHABET)				

def hill_cipher(msg, key, decrypt=False):
	print "MSG: "; print msg
	print "KEY: "; print key

	if decrypt:
		old_key = key
		key = getInverse(key)
		print "INV KEY: "; print key
		print "KEY DIFF: "; print numpy.matrix.round(old_key*key) % MOD_SIZE

	result = numpy.matrix.round(key * msg) % MOD_SIZE
	print "RESULT: "; print result
	return ''.join(ALPHABET[int(round(i) % MOD_SIZE)] for i in result.transpose().getA1())

def getInverse(matrix):
	det = round(numpy.linalg.det(matrix)) # already checked nonzero
	adjoint = det*(matrix.getI())
	print "ADJOINT: "; print adjoint
	print "DET: "; print det

	# xgcd algorithm only accepts positive inputs
	# swap input order if det < 0
	if det < 0:
		(k, invDet, v) = xgcd(det, MOD_SIZE)
	else:
		(k, v, invDet) = xgcd(MOD_SIZE, det)

	print "MUL: "; print invDet
	print invDet*adjoint
	print (invDet*adjoint) % MOD_SIZE

	return (invDet*adjoint) % MOD_SIZE

# Extended Euclidean GCD Algorithm
# INPUTS: a,b positive ints
# OUTPUTS: a - the GCD
#					a1, b1 s.t. gcd(a,b) = a*a1 + b*b1
# Credit: http://userpages.umbc.edu/~rcampbel/Computers/Python/numbthy.html
def xgcd(a,b):
	(a1, a2) = (1,0); (b1, b2) = (0,1) # Two vectors a = (1,0), b = (0,1)
	while True:
		q = a // b # // is floor division, q is the multiple of b to subtract from a
		a1 -= q*b1 # subtract off 'q' multiples of b vector from a vector
		a2 -= q*b2 
		a = a % b
		if a == 0:
			return [b, b1, b2]

		q = b // a # q is the multiple of a to subtract from b
		b1 -= q*a1 # subtract off 'q' multiples of b vector from a vector
		b2 -= q*a2
		b = b % a;
		if b == 0:
			return [a, a1, a2]

def getKeyMatrix(key_string):
	matVals = key_string.split('.')
	if not isPerfSquare(len(matVals)):
		safeExit("Key must be a perfect square!")

	matVals = map(int, matVals)
	for i in matVals:
		if i < 0 or i > MOD_SIZE:
			safeExit("Key values must be between (0-88) Got: ", i)

	rowSize = math.sqrt(len(matVals))
	mat = numpy.reshape(matVals, (rowSize,rowSize))

	if numpy.linalg.det(mat).round() == 0:
		safeExit("Zero determinant. Invalid key.")

	return numpy.matrix(mat)

def getMsgMatrix(msg_string, numRows):
	msgArray = list(msg_string)
	lastChar = msgArray[-1]
	while not len(msgArray) % numRows == 0:
		msgArray += lastChar

	msgArray = map(getAlphIndex, msgArray)

	numCols = len(msgArray) / numRows
	mat = numpy.reshape(msgArray, (numCols, numRows)).transpose()
	return numpy.matrix(mat)

def getAlphIndex(char):
	if not char in ALPHABET:
		safeExit("Message values must appear in alphabet (0-88) Invalid Char: %c" % char)
	return ALPHABET.index(char)

def isPerfSquare(val):
	sqrt = math.sqrt(val)
	return int(sqrt) == sqrt

def safeExit(msg):
	print msg
	sys.exit(1)

def main():	
	parser = argparse.ArgumentParser(description="A program for encrypting and decrypting files securely.")
	parser.add_argument("type", choices=("encrypt", "decrypt"))
	parser.add_argument("-m", "--message", help="The text to be encrypted/decrypted.")
	parser.add_argument("-k", "--key", help="The length of the key (Number of shifts).")
	args = parser.parse_args()
	decryptFlag = args.type == 'decrypt'
	
	# Parse key and message
	key = getKeyMatrix(args.key)
	message = getMsgMatrix(args.message.replace("\\", ""), len(key))

	print hill_cipher(message, key, decryptFlag)

if __name__ == "__main__":
	main()