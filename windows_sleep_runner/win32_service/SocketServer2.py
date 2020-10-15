import os
import warnings
import sys
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
from vyperlogix.sockets import SocketServer
import SocketProcessor

from vyperlogix.sockets.ConnectionHandle import DataFormat

__shutdown__ = '___Shutdown___'
__ipAddr__ = '127.0.0.1'
__port__ = 55555
__bufSize__ = 4096
__timeout__ = -1
__restart__ = False

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

def server_startup(ipAddr=__ipAddr__,port=__port__,shutdown=__shutdown__,bufSize=__bufSize__,callBack=__callBack__,acceptConnectionsFrom=[],isSwappingBits=True,timeout=__timeout__,restart=__restart__):
    theServer = SocketServer.SocketServer()
    theServer.ipAddr = ipAddr
    theServer.port = port
    theServer.sShutdown = shutdown
    theServer.iBufSize = bufSize
    theServer.acceptConnectionsFrom = acceptConnectionsFrom
    theServer.callBack = callBack
    theServer.isSwappingBits = isSwappingBits
    theServer.startup(connectionTimeout=timeout,restart=restart,dataFormat=DataFormat.JSON)

if (__name__ == '__main__'):
    args = {
        '--help':'displays this help text.',
        '--verbose':'output more stuff.',
        '--development':'development mode.',
        '--production':'production mode (lowers the logging level).',
        '--ip=ip_address':'ip address like 127.0.0.1 or 0.0.0.0 or another.',
        '--port=port_number':'port number in the range of 49152-65535.',
        '--restart=restart':'true or false, 1 or 0.',
        '--timeout=timeout':'timeout can be -1 for no timeout or some number of seconds to keep the server from being alive all the time.',
    }
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
        ip = _argsObj.arguments['ip']
        if (ip):
            __ipAddr__ = ip
    except:
        pass

    try:
        timeout = int(_argsObj.arguments['timeout'])
        if (timeout):
            __timeout__ = timeout
    except:
        pass
    
    try:
        restart = _argsObj.get_var('restart',Args._bool_,False)
        if (restart):
            __restart__ = restart
    except:
        pass
    
    #warnings.filterwarnings('ignore','tempnam')
    server_startup(ipAddr=__ipAddr__,port=__port__,shutdown=__shutdown__,bufSize=__bufSize__,acceptConnectionsFrom=[__ipAddr__],restart=__restart__)
    print '(%s) :: End of Main !' % __name__
    sys.exit(1)
