import unittest
import numpy
import hill_cipher as hill
import random

class TestHillCipher(unittest.TestCase):

	def test_keySizes(self):
		min_key_size = 2; max_key_size = 8
		ran_string = ''.join([random.choice(hill.ALPHABET) for x in range(10)])

		for i in range(min_key_size, max_key_size):
			key_matrix = hill.getRandomKeyMatrix(i)
			msg_matrix = hill.getMsgMatrix(ran_string, i)

			encrypted_text = hill.hill_cipher(msg_matrix, key_matrix)
			msg_matrix = hill.getMsgMatrix(encrypted_text, i)

			decrypted_text = hill.hill_cipher(msg_matrix, key_matrix, decrypt=True)
			self.assertEqual(ran_string, decrypted_text[:len(ran_string)])
