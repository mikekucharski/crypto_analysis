from pyciph.vigenere_cipher.vigenere import Vigenere
import unittest
import numpy
import random

class TestVigenereCipher(unittest.TestCase):

	def setUp(self):
		self.m = "This is a REALLY cool string to test!!"

	def test_encryption(self):
		key = "SECRET"
		vig = Vigenere(key)
		encrypted = vig.encrypt(self.m)
		decrypted = vig.decrypt(encrypted)
		self.assertEqual(self.m, decrypted)

	def test_identity_key(self):
		key = "A"
		encrypted = Vigenere(key).encrypt(self.m)
		self.assertEqual(self.m, encrypted)

	def test_long_key(self):
		key = 'G'*50
		vig = Vigenere(key)
		encrypted = vig.encrypt(self.m)
		decrypted = vig.decrypt(encrypted)
		self.assertEqual(self.m, decrypted)

	def test_invalid_key(self):
		key = "123"   # key must be a string
		with self.assertRaises(Exception):
			encrypted = Vigenere(key).encrypt(self.m, key)

	def test_invalid_msg(self):
		with self.assertRaises(Exception):
			encrypted = Vigenere(key).encrypt(None, key)
		with self.assertRaises(Exception):
			encrypted = Vigenere(key).encrypt("", key)