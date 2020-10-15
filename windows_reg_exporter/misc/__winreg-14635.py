import os, sys

from vyperlogix import misc
from vyperlogix.misc import _utils

import _winreg
from vyperlogix.win.registry import winreg
from vyperlogix.win.registry import reg_walker

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

__hives__ = ['HKEY_LOCAL_MACHINE', 'HKEY_CLASSES_ROOT', 'HKEY_CURRENT_USER', 'HKEY_USERS', 'HKEY_CURRENT_CONFIG']

__search__ = __replace__ = None

def gettype(datatype):
    _datatype = winreg.REG(datatype)
    return _datatype if (_datatype) else datatype

def QueryValueEx(hkey, name=''):
    try:
	value, regtype = _winreg.QueryValueEx(hkey, name)
	return (value, regtype, gettype(datatype))
    except WindowsError:
	pass
    except:
	pass
    return None

def SetValueEx(hkey, value, value_name='', type=winreg.REG.SZ, reserved=None):
    try:
	_winreg.SetValueEx(hkey, value_name, reserved, type, value)
    except WindowsError:
	pass
    except:
	pass

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
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

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	__search__ = __args__.get_var('search',misc.isString,__search__)
	__replace__ = __args__.get_var('replace',misc.isString,__replace__)
	
	#######################################################################
	__is_beginning__ = False
	__is_searching__ = misc.isString(__search__)
	__is_replacing__ = misc.isString(__replace__)
	if (_isVerbose):
	    print '1.0 :: INFO: __search__=%s' % (__search__)
	    print '1.1 :: INFO: __is_searching__=%s' % (__is_searching__)
	    print '1.1.1 :: INFO: __is_replacing__=%s' % (__is_replacing__)
	for aHiveName in __hives__:
	    try:
		for (key_name, key), subkey_names, values in reg_walker.walk(aHiveName):
		    __is_beginning__ = True
		    _key_ = None
		    if (_isVerbose) or (__is_searching__):
			_key_ = QueryValueEx(key)
		    if (_isVerbose):
			print '1.2 :: INFO: key_name=%s, key=%s' % (key_name,_key_)
		    if (__is_searching__):
			if (str(key_name).find(__search__) > -1):
			    print '1.3 :: FOUND-KEYNAME: "%s".' % (key_name)
			_value_ = str(_key_[0] if (misc.isIterable(_key_)) else '')
			_vector_ = _value_.find(__search__)
			if (_isDebug):
			    print '1.4 :: DEBUG: _value_=%s, _vector_=%s' % (_value_,_vector_)
			if (_vector_ > -1):
			    print '1.5 :: FOUND-KEY: "%s".' % (_value_)
			    if (__is_replacing__):
				print '1.5.1 :: REPLACED: "%s" --> "%s".' % (__search__, __replace__)
				_value = _value_.replace(__search__, __replace__)
				SetValueEx(key, _value)
		    if (_isVerbose):
			print '1.6 :: INFO: len(values)=%s' % (len(values))
		    for name, data, datatype in values:
			datatype = gettype(datatype)
			_hex_ascii = _utils.hex_ascii(data,ascii_only=True)
			if (__is_searching__):
			    if (str(name).find(__search__) > -1):
				print '1.7 :: FOUND-NAME: "%s".' % (name)
				if (__is_replacing__):
				    print '1.7.1 :: REPLACED: "%s" --> "%s".' % (__search__, __replace__)
				    _name = name.replace(__search__, __replace__)
				    SetValueEx(key, _hex_ascii, value_name=_name, type=datatype.value)
			    if (_hex_ascii.find(__search__) > -1):
				print '1.8 :: FOUND-DATA: "%s".' % (_hex_ascii)
				if (__is_replacing__):
				    print '1.8.1 :: REPLACED: "%s" --> "%s".' % (__search__, __replace__)
				    _hex_ascii_ = _hex_ascii.replace(__search__, __replace__)
				    SetValueEx(key, _hex_ascii_, value_name=name, type=datatype.value)
			else:
			    if (__is_beginning__):
				print 'BEGIN: {%s} {%s}' % (datatype,key_name)
				__is_beginning__ = False
			    print '\t"%s"="%s"' % (name,_utils.hex_ascii(data))
		    if (not __is_searching__):
			print 'END!'
			print
	    except AttributeError, _details:
		info_string = _utils.formattedException(details=_details)
		print >>sys.stderr, info_string
