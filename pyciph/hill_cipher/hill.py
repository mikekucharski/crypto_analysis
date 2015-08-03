import argparse
import numpy
import math
import sys
import random

class Hill(object):
	ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
							"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
							"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
							"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
							"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", ".", 
							"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "=", "?", 
							"[", "]", "{", "}", ";", ":", ",", "<", ">", "'", " "]
	MOD_SIZE = len(ALPHABET)

	def __init__(self, key_string="1.0.1.0"):
		self.key = self.getKeyMatrix(key_string)

	def encrypt(self, msg, decrypt=False):
		key = self.key
		if decrypt: key = self.getModInvMatrix(key)
		msg_mat = self.getMsgMatrix(msg.replace("\\", ""), len(key))

		result = numpy.matrix.round(key * msg_mat) % self.MOD_SIZE
		return ''.join(self.ALPHABET[int(round(i) % self.MOD_SIZE)] for i in result.transpose().getA1())

	def decrypt(self, msg):
		return self.encrypt(msg, decrypt=True)

	def getKeyMatrix(self, key_string):
		matVals = key_string.split('.')
		if not self.isPerfSquare(len(matVals)):
			raise Exception("Key must be a perfect square!")

		matVals = map(int, matVals)
		for i in matVals:
			if i < 0 or i > self.MOD_SIZE:
				raise Exception("Key values must be between (0-88) Got: ", i)

		rowSize = math.sqrt(len(matVals))
		mat = numpy.reshape(matVals, (rowSize,rowSize))

		if self.invalidKeyDet(mat):
			raise Exception("Key is invalid because of Zero determinant.")

		return numpy.matrix(mat)

	def getMsgMatrix(self, msg_string, numRows):
		msgArray = list(msg_string)
		lastChar = msgArray[-1]
		while not len(msgArray) % numRows == 0:
			msgArray += lastChar

		msgArray = map(self.getAlphIndex, msgArray)

		numCols = len(msgArray) / numRows
		mat = numpy.reshape(msgArray, (numCols, numRows)).transpose()
		return numpy.matrix(mat)

	def getModInvMatrix(self, matrix):
		det = round(numpy.linalg.det(matrix)) # already checked nonzero
		adjoint = det*(matrix.getI())

		# xgcd algorithm only accepts positive inputs
		# swap input order if det < 0
		if det < 0:
			(k, invDet, v) = self.xgcd(det, self.MOD_SIZE)
		else:
			(k, v, invDet) = self.xgcd(self.MOD_SIZE, det)

		return numpy.matrix.round(invDet*adjoint) % self.MOD_SIZE

	# Extended Euclidean GCD Algorithm
	# INPUTS: a,b positive ints
	# OUTPUTS: a - the GCD
	#					a1, b1 s.t. gcd(a,b) = a*a1 + b*b1
	# Credit: http://userpages.umbc.edu/~rcampbel/Computers/Python/numbthy.html
	def xgcd(self, a,b):
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

	def invalidKeyDet(self, key):
		return numpy.linalg.det(key).round() % self.MOD_SIZE == 0

	def getAlphIndex(self, char):
		if not char in self.ALPHABET:
			raise Exception("Message values must appear in alphabet (0-88) Invalid Char: %c" % char)
		return self.ALPHABET.index(char)

	def isPerfSquare(self, val):
		sqrt = math.sqrt(val)
		return int(sqrt) == sqrt
