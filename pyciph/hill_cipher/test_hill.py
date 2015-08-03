from pyciph.hill_cipher.hill import Hill
import unittest
import numpy
import random

class TestHillCipher(unittest.TestCase):

	def getRandKeyHill(self, size):
		totalSize = size*size
		while True:
			arr = [random.randint(0, Hill.MOD_SIZE-1) for x in range(totalSize)]
			key_string = '.'.join(map(str, arr))
			try:
				hill = Hill(key_string)
				return hill
			except:
				pass

	def test_keySizes(self):
		min_key_len = 2
		max_key_len = 8
		rand_string = ''.join([random.choice(Hill.ALPHABET) for x in range(10)])

		for key_size in range(min_key_len, max_key_len):
			hill = self.getRandKeyHill(key_size)
			encrypted = hill.encrypt(rand_string)
			decrypted = hill.decrypt(encrypted)
			self.assertEqual(rand_string, decrypted[:len(rand_string)])
