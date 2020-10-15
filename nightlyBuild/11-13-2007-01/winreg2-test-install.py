import Tkinter
from vyperlogix import tkMessageBox, winreg, winreg2, putStr
import traceback
import os
import sys
import psyco

_isVerbose = False
_isAllKeys = False

_programName = ''

_rootKeyName = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'

################################################################################

def printKeysAndValues(root):
    try:
        keys = root.keys()
        print 'root.__class__=(%s)' % str(root.__class__)
        print 'len(keys)=(%s)' % len(keys)
        for i in xrange(len(keys)):
            subKey = root.openkey(i+1)
            print '(%s)' % (subKey.getkeyname())
            _keys = subKey.keys()
            for k in _keys:
                print '\t(%s)' % (str(k))
            _vals = subKey.values()
            for v in _vals:
                print '\t(%s)' % (str(v))
            subKey.close()
    except:
        tkMessageBox.showerror('Error', traceback.format_exc())

def main(key):
    Tkinter.Tk().withdraw()
    try:
        key = winreg2.Registry.open('HKEY_LOCAL_MACHINE', key)
        print 'key=(%s)' % str(key)
        print 'key.getkeyname()=(%s)' % str(key.getkeyname())
        print 'key.getkey()=(%s)' % str(key.getkey())
	if (_isAllKeys):
	    printKeysAndValues(key)
	_keyTarget = 'DSS'
	_keys = key.keys()
	dKeys = {}
	i = 0
	for k in _keys:
	    dKeys[k] = i
	    i += 1
	i = -1
	#print '_keys=(%s)' % str(_keys)
	if (dKeys.has_key(_keyTarget)):
	    i = dKeys[_keyTarget]
	print 'i=(%s)' % i
	subKey = None
	if (i > -1):
	    subKey = key.enumkey(i)
	print 'subKey=(%s)' % subKey
        #dssKey = key.create(key.getkey(), _keyTarget)
	dssKey = key.openkey(i+1)
	if (isinstance(dssKey, None.__class__)):
	    pass
	else:
	    print '(2) dssKey.__class__=(%s)' % str(dssKey.__class__)
	    print '(2) dssKey.getkeyname()=(%s)' % dssKey.getkeyname()
	dssKey.setvalue('DisplayName', solve('DSS - Decision Support System'))
	dssKey.setvalue('NoModify', solve(1))
	dssKey.setvalue('NoRepair', solve(1))
	if (os.path.exists('c:/dss/uninstall.exe')):
	    dssKey.setvalue('UninstallString', solve('c:\\dss\\uninstall.exe'))
	dssKey.close()
        print 'END! Created Key called "DSS".'
        key.close()
    except:
        tkMessageBox.showerror('Error', traceback.format_exc())

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
    psyco.bind(main)
    main(_rootKeyName)

