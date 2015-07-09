#!/usr/bin/env python
import argparse
from mycrypto.caesar import caesar_cipher as caesar
from mycrypto.hill import hill_cipher as hill
from mycrypto.vigenere import vigenere_cipher as vig

def main():	
	parser = argparse.ArgumentParser(description="A program for encrypting and decrypting files securely.")
	parser.add_argument("-c", "--cipher", choices=("caesar", "vigenere", "hill"), required=True)
	parser.add_argument("type", choices=("encrypt", "decrypt"))
	parser.add_argument("-m", "--message", help="The text to be encrypted/decrypted.")
	parser.add_argument("-k", "--key", help="Key")
	args = parser.parse_args()
	decryptFlag = args.type == 'decrypt'
	cipher = args.cipher

	if cipher == 'caesar':
		print caesar.encrypt(args.message, int(args.key), decryptFlag)
	elif cipher == 'vigenere':
		print vig.vigenere_cipher(args.message, args.key, decryptFlag)
	elif cipher == 'hill':
		key = hill.getKeyMatrix(args.key)
		message = hill.getMsgMatrix(args.message.replace("\\", ""), len(key))
		print hill.hill_cipher(message, key, decryptFlag)

if __name__ == "__main__":
	main()