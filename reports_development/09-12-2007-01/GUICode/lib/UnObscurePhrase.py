def UnObscurePhrase(t):
	str = ""
	j = len(t)
	for i in range(j):
		_ch = t[i]
		_ch = chr(ord(_ch) - 128)
		str += _ch
	return str
