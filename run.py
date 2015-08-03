#!/usr/bin/env python
import argparse
from pyciph.caesar_cipher.caesar import Caesar
from pyciph.vigenere_cipher.vigenere import Vigenere
from pyciph.hill_cipher.hill import Hill

def main():	
	parser = argparse.ArgumentParser(description="A program for encrypting and decrypting files securely.")
	parser.add_argument("-c", "--cipher", choices=("caesar", "vigenere", "hill"), required=True)
	parser.add_argument("type", choices=("encrypt", "decrypt"))
	parser.add_argument("-m", "--message", help="The text to be encrypted/decrypted.")
	parser.add_argument("-k", "--key", help="Key")

	# Extract cmd line arguments
	args = parser.parse_args()
	decryptFlag = args.type == 'decrypt'
	cipher = args.cipher
	msg = args.message
	key = args.key

	if cipher == 'caesar':
		key = int(key)
		caesar = Caesar(key)
		print caesar.decrypt(msg) if decryptFlag else caesar.encrypt(msg)
	elif cipher == 'vigenere':
		vig = Vigenere(key)
		print vig.decrypt(msg) if decryptFlag else vig.encrypt(msg)
	elif cipher == 'hill':
		hill = Hill(key)
		msg = msg.replace("\\", "")
		print hill.decrypt(msg) if decryptFlag else hill.encrypt(msg)

if __name__ == "__main__":
	main()