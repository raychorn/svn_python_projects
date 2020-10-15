from encodings.hex_codec import *

def ObscurePhrase(str):
	t = ""
	j = len(str)
	for i in range(j):
		_ch = ord(str[i])
		_ch += 128
		t += chr(_ch)
	return t

def ObscurePhraseAsHex(str):
	t = ""
	j = len(str)
	for i in range(j):
		t += "\\x" + hex_encode(str[i])[0]
	return t

def ObscurePhraseTest(str):
	print 'ObscurePhrase(test)=', """'""" + ObscurePhrase('test') + """'"""