import os
import warnings
import sys
from vyperlogix.sockets import SocketServer
import SocketProcessor

from vyperlogix.sockets.ConnectionHandle import DataFormat

__shutdown__ = '___Shutdown___'
__ipAddr__ = '127.0.0.1'
__port__ = 55555
__bufSize__ = 4096
__timeout__ = -1
__restart__ = True  # required for the Adobe Air Connection Method.

processor = SocketProcessor.Processor()
processor.isLicensed = SocketProcessor.LicenseLevels.TRIAL

def __callBack__(server,connHandle,data):
    print >>sys.stderr, '(callBack) :: server=(%s), connHandle=(%s), data=%s' % (str(server),str(connHandle),data)
    if (isinstance(data,str)):
        response = processor.process(connHandle,data)
    else:
        #response = ''.join(['<%s>%s</%s>' % (c[0],c[-1],c[0]) for c in XMLProcessor.LicenseLevels])
        #response = '<LicenseLevels>' + response + '</LicenseLevels>'
        #server.__send__(connHandle,response)
        #response = '<license>' + str(XMLProcessor.LicenseLevels(processor.isLicensed)).split('.')[-1] + '</license>'
        #server.__send__(connHandle,response)
        if (connHandle.isXML):
            response = ''.join(['<%s>%s</%s>' % (c[0],c[-1],c[0]) for c in SocketProcessor.Commands])
            response = '<commands>' + response + '</commands>'
        elif (connHandle.isJSON):
            d = SocketProcessor.Commands.asDict()
            response = SocketProcessor.Commands.asJSON()
    if ( (isinstance(response,tuple)) or (isinstance(response,list)) ):
        response = response[0]
    return response

def server_startup(ipAddr=__ipAddr__,port=__port__,shutdown=__shutdown__,bufSize=__bufSize__,callBack=__callBack__,acceptConnectionsFrom=[],isSwappingBits=True,timeout=__timeout__,restart=__restart__,isDebugging=False,isVerbose=False,dropConnectionOnErrors=False):
    from vyperlogix.misc import _utils
    
    theServer = SocketServer.SocketServer()
    theServer.ipAddr = ipAddr
    theServer.port = port
    theServer.sShutdown = shutdown
    theServer.iBufSize = bufSize
    theServer.acceptConnectionsFrom = acceptConnectionsFrom
    theServer.callBack = callBack
    theServer.isSwappingBits = isSwappingBits
    isDebugging = _utils.isBeingDebugged if (isDebugging is None) else isDebugging
    
    if (isVerbose):
        print '(server_startup) --> theServer.ipAddr=%s' % (theServer.ipAddr)
        print '(server_startup) --> theServer.port=%s' % (theServer.port)
        print '(server_startup) --> theServer.sShutdown=%s' % (theServer.sShutdown)
        print '(server_startup) --> theServer.iBufSize=%s' % (theServer.iBufSize)
        print '(server_startup) --> theServer.acceptConnectionsFrom=%s' % (theServer.acceptConnectionsFrom)
        print '(server_startup) --> theServer.callBack=%s' % (theServer.callBack)
        print '(server_startup) --> theServer.isSwappingBits=%s' % (theServer.isSwappingBits)
        print '(server_startup) --> isDebugging=%s' % (isDebugging)
    
    theServer.startup(connectionTimeout=timeout,restart=restart,dropConnectionOnErrors=dropConnectionOnErrors,isDebugging=isDebugging,dataFormat=DataFormat.JSON)

if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    args = {
        '--help':'displays this help text.',
        '--verbose':'output more stuff.',
        '--development':'development mode.',
        '--debugging':'debugging mode.',
        '--production':'production mode (lowers the logging level).',
        '--restart':'restart mode',
        '--ip=ip_address':'ip address like 127.0.0.1 or 0.0.0.0 or another.',
        '--port=port_number':'port number in the range of 49152-65535.',
        '--timeout=timeout':'timeout can be -1 for no timeout or some number of seconds to keep the server from being alive all the time.',
    }
    _argsObj = Args.Args(args)
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

    if (len(sys.argv) == 1):
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
        _isDebugging = _argsObj.booleans['isDebugging']
    except:
        _isDebugging = False
            
    if (_isVerbose):
        print 'INFO: _isDebugging=%s' % (_isDebugging)

    try:
        _isRestart = _argsObj.booleans['isRestart']
        if (_isRestart):
            __restart__ = _isRestart
    except:
        __restart__ = False
        
    if (_isVerbose):
        print 'INFO: _isProduction=%s' % (_isProduction)

    try:
        _isDevelopment = _argsObj.booleans['isDevelopment']
    except:
        _isDevelopment = False

    if (_isVerbose):
        print 'INFO: _isDevelopment=%s' % (_isDevelopment)

    try:
        __port__ = int(_argsObj.arguments['port'])
        if ( (__port__ < 49152) or (__port__ > 65535) ):
            __port__ = 55555
    except:
        pass
    
    if (_isVerbose):
        print 'INFO: __port__=%s' % (__port__)

    try:
        ip = _argsObj.arguments['ip']
        if (ip):
            __ipAddr__ = ip
    except:
        pass

    if (_isVerbose):
        print 'INFO: __ipAddr__=%s' % (__ipAddr__)

    try:
        timeout = int(_argsObj.arguments['timeout'])
        if (timeout):
            __timeout__ = timeout
    except:
        pass
    
    if (_isVerbose):
        print 'INFO: __timeout__=%s' % (__timeout__)

    if (_isVerbose):
        print 'INFO: __restart__=%s' % (__restart__)

    #warnings.filterwarnings('ignore','tempnam')
    server_startup(ipAddr=__ipAddr__,port=__port__,shutdown=__shutdown__,bufSize=__bufSize__,acceptConnectionsFrom=[__ipAddr__],restart=__restart__,isDebugging=_isDebugging,isVerbose=_isVerbose)
    print '(%s) :: End of Main !' % __name__
    sys.exit(1)
