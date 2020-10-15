import sys

from vyperlogix.misc import _utils
from vyperlogix.win.registry import reg_walker

# http://timgolden.me.uk/python-on-windows/programming-areas/registry/walk-the-registry.html

_hit_list = ['HostName','PublicKeyFile','UserName','ProxyUsername','ProxyPassword','Password']

def main(keypath):
    if (_isDelete):
        import _winreg
        try:
            for (key_name, key), subkey_names, values in reg_walker.walk(keypath,writeable=True):
                for name, data, datatype in values:
                    if (datatype == _winreg.REG_SZ) and (name in _hit_list):
                        _winreg.SetValueEx(key, name, None, datatype, '***')
        except AttributeError, _details:
            info_string = _utils.formattedException(details=_details)
            print >>sys.stderr, 'ERROR: --keypath="%s" [Cannot be what it is.]' % (keypath)
            print >>sys.stderr, info_string
    else:
        print 'Windows Registry Editor Version 5.00\n'
        try:
            for (key_name, key), subkey_names, values in reg_walker.walk(keypath):
                print '[%s]' % (key_name)
                for name, data, datatype in values:
                    print '"%s"="%s"' % (name,data)
                print
        except AttributeError, _details:
            info_string = _utils.formattedException(details=_details)
            print >>sys.stderr, 'ERROR: --keypath="%s" [Cannot be what it is.]' % (keypath)
            print >>sys.stderr, info_string

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--delete':'delete the specified keypath.',
            '--keypath=?':'the keypath for the export operation.',
            }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isVerbose = False
    try:
        if _argsObj.booleans.has_key('isVerbose'):
            _isVerbose = _argsObj.booleans['isVerbose']
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print info_string
        _isVerbose = False

    if (_isVerbose):
        print '_argsObj=(%s)' % str(_argsObj)

    _isHelp = False
    try:
        if _argsObj.booleans.has_key('isHelp'):
            _isHelp = _argsObj.booleans['isHelp']
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print info_string
        _isHelp = False

    _isDelete = False
    try:
        if _argsObj.booleans.has_key('isDelete'):
            _isDelete = _argsObj.booleans['isDelete']
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print info_string
        _isDelete = False

    _keypath = ''
    try:
        if _argsObj.arguments.has_key('keypath'):
            _keypath = _argsObj.arguments['keypath']
    except Exception, _details:
        info_string = _utils.formattedException(details=_details)
        print info_string
        _keypath = ''

    if (_isHelp):
        ppArgs()
    else:
        main(_keypath)
