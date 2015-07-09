#!/usr/bin/env python
def encrypt(msg, key=3, decrypt=False):
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