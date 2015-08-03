from pyciph.caesar_cipher.caesar import Caesar
import unittest
import numpy
import random

class TestCaesarCipher(unittest.TestCase):

	def setUp(self):
		self.m = "This is a REALLY cool string to test!!"

	def test_encryption(self):
		key = 5
		caesar = Caesar(key)
		encrypted = caesar.encrypt(self.m)
		decrypted = caesar.decrypt(encrypted)
		self.assertEqual(self.m, decrypted)

	def test_default_key(self):
		key = 3 # default key is 3
		encrypted1 = Caesar(key).encrypt(self.m)
		encrypted2 = Caesar().encrypt(self.m)
		self.assertEqual(encrypted1, encrypted2)

	def test_identity_key(self):
		key = 0
		encrypted = Caesar(key).encrypt(self.m)
		self.assertEqual(self.m, encrypted)

	def test_key_rotation(self):
		key = 7
		rotatedKey = key + 26
		encrypted1 = Caesar(key).encrypt(self.m)
		encrypted2 = Caesar(rotatedKey).encrypt(self.m)
		self.assertEqual(encrypted1, encrypted2)

	def test_invalid_key(self):
		key = "A"   # key must be an integer
		with self.assertRaises(TypeError):
			encrypted = Caesar(key).encrypt(self.m)

	def test_invalid_msg(self):
		with self.assertRaises(Exception):
			encrypted = Caesar(key).encrypt(None)
		with self.assertRaises(Exception):
			encrypted = Caesar(key).encrypt("")