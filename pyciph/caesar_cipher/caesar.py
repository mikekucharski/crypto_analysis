class Caesar(object):
	
	def __init__(self, key=3):
		if type(key) is not int:
			raise TypeError("key must be an int")
		self.key = key % 26

	def encrypt(self, msg, decrypt=False):
		if type(msg) is not str:
			raise TypeError("msg must be a string")
		
		k = self.key
		if msg == None or len(msg) < 1: return msg
		if decrypt: k *= -1    # shift left
		new_msg = ""
		for m in msg:
			if not m.isalpha(): 
				new_msg += m
				continue
			offset = 65 if m.isupper() else 97
			new_msg += chr( (((ord(m)-offset) + k) % 26) + offset)
		return new_msg

	def decrypt(self, msg):
		return self.encrypt(msg, decrypt=True)