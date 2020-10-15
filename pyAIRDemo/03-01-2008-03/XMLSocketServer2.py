from lib import SocketServer
from lib import threadpool
import os
import warnings
import sys
import psyco
from lib import PrettyPrint
from lib import Args
import XMLProcessor
from win32api import GetComputerName
from lib import _psyco
from lib import _utils

_pool = threadpool.Pool(100)

__shutdown__ = '___Shutdown___'
__ipAddr__ = 'localhost'
__port__ = 55555
__bufSize__ = 4096

def callBack(server,connHandle,data):
    print >>sys.stderr, '(callBack) :: server=(%s), connHandle=(%s)' % (str(server),str(connHandle))
    if (isinstance(data,str)):
        response = processor.processXML(connHandle,data)
    else:
        response = ''.join(['<%s>%s</%s>' % (c[0],c[-1],c[0]) for c in XMLProcessor.Commands])
        response = '<response><commands>' + response + '</commands>'
        response += '<machineID>' + GetComputerName() + '</machineID></response>'
    if ( (isinstance(response,tuple)) or (isinstance(response,list)) ):
        response = response[0]
    return response

def main():
    theServer = SocketServer.SocketServer()
    theServer.ipAddr = __ipAddr__
    theServer.port = __port__
    theServer.sShutdown = __shutdown__
    theServer.iBufSize = __bufSize__
    #theServer.acceptConnectionsFrom = []
    theServer.callBack = callBack
    theServer.isSwappingBits = True
    print '(main) :: theServer=(%s)' % (str(theServer))
    theServer.startup()
    print '(main) :: End of Main !'

args = {'--help':'displays this help text.','--verbose':'output more stuff.','--development':'development mode.','--production':'production mode (lowers the logging level).','--port=port_number':'port number in the range of 49152-65535.','--launch=exeName':'launch the AIR App using this file.','--uninstall=uninstaller':'uninstall the AIR App and clean-up afterwards using the original uninstaller from Adobe.'}
_argsObj = Args.Args(args)
print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
    pArgs = [(k,args[k]) for k in args.keys()]
    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
    pPretty.pprint()

try:
    _isVerbose = _argsObj.booleans['isVerbose']
except:
    _isVerbose = False

try:
    _isProduction = _argsObj.booleans['isProduction']
except:
    _isProduction = False

try:
    _isDevelopment = _argsObj.booleans['isDevelopment']
except:
    _isDevelopment = False

try:
    __port__ = int(_argsObj.arguments['port'])
    if ( (__port__ < 49152) or (__port__ > 65535) ):
        __port__ = 55555
except:
    pass

try:
    _launch_fileName = _argsObj.arguments['launch']
except:
    _launch_fileName = ''

try:
    _uninstall_fileName = _argsObj.arguments['uninstall']
except:
    _uninstall_fileName = ''

if (_utils.getVersionNumber() >= 251):
    _psyco.importPsycoIfPossible()
    processor = XMLProcessor.XMLProcessor()
    #warnings.filterwarnings('ignore','tempnam')
    main()
print '(%s) :: End of Main !' % __name__
sys.exit(1)
