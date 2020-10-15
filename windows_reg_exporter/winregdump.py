import os, sys

from vyperlogix.win.registry import winreg2
from vyperlogix.win.registry.winreg2 import RegistryError

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.classes import SmartObject

from encodings import hex_codec
import simplejson

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

#__hives__ = ['HKEY_LOCAL_MACHINE', 'HKEY_CLASSES_ROOT', 'HKEY_CURRENT_USER', 'HKEY_USERS', 'HKEY_CURRENT_CONFIG']
__hives__ = ['HKEY_LOCAL_MACHINE']

__search__ = __replace__ = None

__keyname__ = 'SOFTWARE\Microsoft\Windows\CurrentVersion'

def enum_keys_from(corekey):
    i = 1
    keys = []
    while (True):
        try:
            aKey = corekey.openkey(i)
            value = aKey.getvalue()
            keys.append([i,SmartObject.SmartObject({'keyname':aKey.getkeyname(),'value':value})])
        except:
            aKey = None
            value = None
            break
        finally:
            if (aKey):
                aKey.close()
        i += 1
    return dict(keys)

def _traverse_key(hivename,root,prefix):
    _is_ = misc.isString(hivename)
    if (_is_):
	_h_ = hivename
    else:
	try:
	    _h_ = hivename['hivename']
	except:
	    _h_ = None
    if (misc.isString(_h_)):
	keyname = str(root.getkeyname())
	_keyname = keyname if (prefix != keyname) else ''
	_k_ = prefix+('\\' if (len(_keyname) > 0) else '')+_keyname
	if (_isDebug):
	    print '%s::%s' % (hivename,_k_)
    
	for value in root.values():
	    _v_ = value[-1].value
	    if (_utils.is_any_non_ascii(_v_ if (misc.isString(_v_)) else str(_v_))):
		_v_ = _utils._hex_ascii(_v_, size=20, ascii_only=False)
	    hivename[value[0]] = (ObjectTypeName.typeClassName(value[-1]),_v_)
	    if (_isDebug):
		print '\t%s=%s' % value
	    
	keys = enum_keys_from(root)
	
	for idx,so in keys.iteritems():
	    corekey = root.openkey(idx)
	    try:
		if (not _is_):
		    __k__ = _k_+'\\'+corekey.getkeyname()
		    hivename[__k__] = {'hivename':_h_}
		_traverse_key(hivename[__k__] if (not _is_) else hivename, corekey, _k_)
		if (not _is_):
		    del hivename[__k__]['hivename']
	    finally:
		corekey.close()

def traverse_key(hivename,keyname):
    _is_ = misc.isString(hivename)
    if (_is_):
	_h_ = hivename
    else:
	try:
	    _h_ = hivename['hivename']
	except:
	    _h_ = None
    if (misc.isString(_h_)):
	root = winreg2.Registry.open(_h_,keyname)
	try:
	    if (not _is_):
		hivename[keyname] = {'hivename':_h_}
	    _traverse_key(hivename[keyname] if (not _is_) else hivename, root, keyname)
	    if (not _is_):
		del hivename[keyname]['hivename']
	finally:
	    root.close()

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--json':'emit json.',
	    '--search=?':'something for which to search.',
	    '--replace=?':'something to replace the search with once found.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',bool,False)
	_isDebug = __args__.get_var('isDebug',bool,False)
	_isHelp = __args__.get_var('isHelp',bool,False)
	_isJson = __args__.get_var('isJson',bool,False)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__search__ = __args__.get_var('search',misc.isString,__search__)
	__replace__ = __args__.get_var('replace',misc.isString,__replace__)
	__keyname__ = __args__.get_var('keyname',misc.isString,__keyname__)
	
	__is_beginning__ = False
	__is_searching__ = misc.isString(__search__)
	__is_replacing__ = misc.isString(__replace__)
	if (_isVerbose):
	    print '1.0 :: INFO: __search__=%s' % (__search__)
	    print '1.1 :: INFO: __is_searching__=%s' % (__is_searching__)
	    print '1.2 :: INFO: __is_replacing__=%s' % (__is_replacing__)
	    print '1.3 :: INFO: _isJson=%s' % (_isJson)
	for aHiveName in __hives__:
	    _hivename_ = aHiveName
	    if (_isJson):
		_hivename_ = {'hivename':aHiveName}
	    traverse_key(_hivename_, __keyname__)
	if (_isJson):
	    _j_ = simplejson.dumps(_hivename_)
	    print _j_
