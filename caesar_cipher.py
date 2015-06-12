#!/usr/bin/env python
import argparse

def caesar_cipher(msg, key=3, decrypt=False):
	if msg == None or len(msg) < 1: return msg
	if decrypt: key *= -1   # shift left
	new_msg = ""
	for m in msg:
		if not m.isalpha(): 
			new_msg += m
			continue
		offset = 65 if m.isupper() else 97
		new_msg += chr( (((ord(m)-offset) + key) % 26) + offset)
	return new_msg


def main():	
	parser = argparse.ArgumentParser(description="A program for encrypting and decrypting files securely.")
	parser.add_argument("type", choices=("encrypt", "decrypt"))
	parser.add_argument("-m", "--message", help="The text to be encrypted/decrypted.")
	parser.add_argument("-k", "--key", type=int, default=3, choices=range(1, 26), help="The length of the key (Number of shifts).")
	args = parser.parse_args()

	decryptFlag = args.type == 'decrypt'
	print caesar_cipher(args.message, key=args.key, decrypt=decryptFlag)

if __name__ == "__main__":
	main()