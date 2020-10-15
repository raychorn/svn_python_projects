from encodings.hex_codec import *

def UnObscurePhrase(t):
	str = ""
	toks = t.split('\\x')
	if (len(toks) > 1):
		for ch in toks:
			_ch = hex_decode(ch)
			str += _ch[0]
		return UnObscurePhrase(str)
	else:
		for ch in t:
			_ch = chr(ord(ch) - 128)
			str += _ch
	return str
