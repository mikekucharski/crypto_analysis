#!/usr/bin/env python
import argparse
import re

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def vigenere_cipher(msg, key, decrypt=False):
	if msg == None or len(msg) < 1 or len(key) < 1: return msg

	new_msg = ""
	keyIndex = 0

	# remove non alphabetic chars from key
	regex = re.compile('[^a-zA-Z]')
	key = regex.sub('', key)

	for m in msg:
		if not m.isalpha(): # skip non alphabetic chars
			new_msg += m
			continue
		letterPos = LETTERS.find(m.upper())
		offset = 65 if m.isupper() else 97
		shiftVal = LETTERS.find(key[keyIndex].upper())
		keyIndex += 1
		if keyIndex >= len(key): keyIndex =0 
		if decrypt: shiftVal *= -1   # subtract the value
		new_msg += chr( (((ord(m)-offset) + shiftVal) % 26) + offset)
	return new_msg


def main():	
	parser = argparse.ArgumentParser(description="A program for encrypting and decrypting files securely.")
	parser.add_argument("type", choices=("encrypt", "decrypt"))
	parser.add_argument("-m", "--message", required=True, help="The text to be encrypted/decrypted.")
	parser.add_argument("-k", "--key", required=True, help="The key to determine the alphabet to use")
	args = parser.parse_args()

	decryptFlag = args.type == 'decrypt'
	print vigenere_cipher(args.message, args.key, decrypt=decryptFlag)

if __name__ == "__main__":
	main()