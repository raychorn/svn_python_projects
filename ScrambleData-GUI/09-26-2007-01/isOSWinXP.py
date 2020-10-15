import sys

win_vers = {5:'XP', 6:'Vista', 'XP':5, 'Vista':6}

def isOSWinSpecific(ver=5):
	try:
		winver = sys.getwindowsversion()
		if (len(winver) < 5):
			return False
		return ( (sys.platform.lower() == 'win32') and (winver[0] == ver) )
	except Exception, details:
		return False

def isOSWinXP():
	return isOSWinSpecific(win_vers['XP'])

def isOSWinVista():
	return isOSWinSpecific(win_vers['Vista'])

def isOSWinAny():
	try:
		return (sys.platform.lower() == 'win32')
	except Exception, details:
		return False

