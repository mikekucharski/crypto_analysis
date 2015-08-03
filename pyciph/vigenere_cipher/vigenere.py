import re

class Vigenere(object):
	
	LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	def __init__(self, key="A"):
		if type(key) is not str:
			raise TypeError("key must be a string")	
		if len(key) < 1: 
			raise Exception("key length must be > 0 alphabetic letters")

		regex = re.compile('[^a-zA-Z]')   # remove non alphabetic chars from key
		key = regex.sub('', key)
		self.key = key

	def encrypt(self, msg, decrypt=False):
		if type(msg) is not str : 
			raise TypeError("msg must be a string")
		if len(msg) < 1: 
			raise Exception("msg length must be > 0 alphabetic letters")

		new_msg = ""
		keyIndex = 0
		for m in msg:
			if not m.isalpha(): # skip non alphabetic chars
				new_msg += m
				continue
			letterPos = self.LETTERS.find(m.upper())
			offset = 65 if m.isupper() else 97
			shiftVal = self.LETTERS.find(self.key[keyIndex].upper())
			keyIndex += 1
			if keyIndex >= len(self.key): keyIndex =0 
			if decrypt: shiftVal *= -1   # subtract the value
			new_msg += chr( (((ord(m)-offset) + shiftVal) % 26) + offset)
		return new_msg

	def decrypt(self, msg):
		return self.encrypt(msg, decrypt=True)