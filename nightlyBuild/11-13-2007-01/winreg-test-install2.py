import Tkinter
from vyperlogix import tkMessageBox, winreg, putStr, decodeUnicode
import traceback
import encodings
import os
import sys
import psyco

_isVerbose = False
_isAllKeys = False
_isInstall = False
_isRemove = False

_programName = ''

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

################################################################################

def updateAddOrRemoveProgramStrings(root, op='ADD'):
    op = str(op).upper()
    if (op == 'ADD'):
	subKey = get_key(root, 'DSS', winreg.KEY.ALL_ACCESS)
	subKey.values['DisplayName'] = solve('DSS - Decision Support System')
	subKey.values['DisplayVersion'] = solve('1.0.0.0')
	subKey.values['HelpLink'] = solve('mailto:ray_horn@bigfix.com')
	subKey.values['URLUpdateInfo'] = solve('http://www.bigfix.com')
	subKey.values['NoModify'] = solve(1)
	subKey.values['NoRepair'] = solve(1)
	subKey.values['Publisher'] = solve('BigFix, Inc.')
	subKey.values['UninstallString'] = solve('c:\\dss\\uninstall.exe')
    elif (op == 'REMOVE'):
	print 'root.__class__=(%s)' % str(root.__class__)
	root.remove('DSS')

def main(key):
    Tkinter.Tk().withdraw()
    try:
        print 'key=(%s)' % key
        root = get_key(winreg.HKEY.LOCAL_MACHINE, key, winreg.KEY.ALL_ACCESS)
        print 'root=(%s)' % str(root)
        print 'root.__class__=(%s)' % str(root.__class__)
        print 'len(root.values)=(%s)' % len(root.values)
	if (_isInstall):
	    updateAddOrRemoveProgramStrings(root,'ADD')
	elif (_isRemove):
	    updateAddOrRemoveProgramStrings(root,'REMOVE')
        print 'root.values=(%s)' % str(root.values)
        print 'root.values.__class__=(%s)' % str(root.values.__class__)
	if (_isAllKeys):
	    for v in root.values:
		print 'v=(%s) [%s]' % (str(v),str(v.__class__))
	    for k in root.keys:
		print 'k=(%s)' % str(k)
		subKey = get_key(root, k, winreg.KEY.ALL_ACCESS)
		print 'subKey.__class__=(%s)' % str(subKey.__class__)
		print 'subKey.values.__class__=(%s)' % str(subKey.values.__class__)
		for v in subKey.values:
		    _v = subKey.values.__getitem__(v)
		    try:
			print '\t(%s)=(%s)' % (str(v),_v.value)
		    except UnicodeEncodeError:
			print '\t(%s)=(%s)' % (decodeUnicode(v),decodeUnicode(_v.value))
		print '\n'
        tkMessageBox.showinfo('Info', 'root=(%s)' % (str(root)))
    except:
        tkMessageBox.showerror('Error', traceback.format_exc())

def get_key(key, subkey, mode=None):
    'Return the specified subkey.'
    key = winreg.Key(key)
    for subkey in subkey.split('\\'):
        if subkey not in key.keys:
            key.keys = subkey
        key = key.keys[subkey]
    return winreg.Key(key, mode=mode)

def solve(value):
    'Correctly package the value.'
    if isinstance(value, str):
        return winreg.REG_SZ(value)
    elif isinstance(value, int):
        return winreg.REG_DWORD(value)
    elif isinstance(value, list):
        return winreg.REG_MULTI_SZ(value)
    raise NotImplementedError, 'Cannot solve for %s' % type(value)

################################################################################

if __name__ == '__main__':
    if ( (len(sys.argv) > 1) and (sys.argv[1] == '--help') ):
	print '--help                      ... displays this help text.'
	print '--verbose                   ... output more stuff.'
	print '--allKeys                   ... display all the keys.'
	print '--install                   ... install the mock product in the Add or Reove Program Strings.'
	print '--remove                    ... remove the mock product from the Add or Reove Program Strings.'
	print '--key=keyname               ... sets the beginning keyname.'
    else:
	toks = sys.argv[0].split(os.sep)
	_programName = toks[-1]
	for i in xrange(len(sys.argv)):
	    bool = (sys.argv[i].find('--key=') > -1)
	    if (bool): 
		toks = sys.argv[i].split('=')
		if (sys.argv[i].find('--key=') > -1):
		    _rootKeyName = toks[1]
	    elif (sys.argv[i].find('--verbose') > -1):
		_isVerbose = True
	    elif (sys.argv[i].find('--allKeys') > -1):
		_isAllKeys = True
	    elif (sys.argv[i].find('--install') > -1):
		_isInstall = True
	    elif (sys.argv[i].find('--remove') > -1):
		_isRemove = True
    psyco.bind(main)
    main(_rootKeyName)

