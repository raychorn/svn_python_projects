import msvcrt

def putStr(s):
	for ch in s:
		msvcrt.putch(ch)

if __name__ == "__main__":
	putStr('Testing...')
