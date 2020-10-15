import os, sys
from vyperlogix.misc import _utils
from vyperlogix.win.registry import reg_walker

import _winreg

from vyperlogix.win.registry import winreg

def reg_scanner(keypath):
    try:
        for (key_name, key), subkey_names, values in reg_walker.walk(keypath,writeable=True):
            for name, data, datatype in values:
                if (datatype == _winreg.REG_SZ) and (name in _hit_list):
                    _winreg.SetValueEx(key, name, None, datatype, '***')
    except AttributeError, ex:
        info_string = _utils.formattedException(details=ex)
        print >>sys.stderr, 'ERROR: --keypath="%s" [Cannot be what it is.]' % (keypath)
        print >>sys.stderr, info_string

__hives__ = [_winreg.HKEY_LOCAL_MACHINE, _winreg.HKEY_CLASSES_ROOT, _winreg.HKEY_CURRENT_USER, _winreg.HKEY_USERS, _winreg.HKEY_CURRENT_CONFIG]

if (__name__ == '__main__'):
    from vyperlogix.win.registry import winreg
    aRegistry = winreg.Registry()
    for aKey in aRegistry:
        pass
    pass
    #_hives = ['HKEY_LOCAL_MACHINE', 'HKEY_CLASSES_ROOT', 'HKEY_CURRENT_USER', 'HKEY_USERS', 'HKEY_CURRENT_CONFIG']
    #for hive in hives:
        #root = winreg.get_key(hive, '\\', winreg.KEY.ALL_ACCESS)
        #reg_scanner(hive)
        