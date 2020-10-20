from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_ERROR
import time
import os
import sys
import math
from threading import Timer
import win32api
from vyperlogix import misc
from vyperlogix.misc import threadpool
from vyperlogix.sockets import ConnectionHandle
from vyperlogix.win import WinProcesses
from vyperlogix.misc import PrettyPrint
from vyperlogix.misc import hex as __hex__

from vyperlogix.sockets.ConnectionHandle import DataFormat

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def dummy():
    pass

class SocketServer():
    __Q__ = threadpool.ThreadQueue(10)
    __connectionTimeoutTimer__ = None

    def __init__(self):
        self.ipAddr = 'localhost'
        self.port = 55555
        self.sShutdown = '@@@Shutdown@@@'
        self.iBufSize = 1024
        self.callBack = dummy
        self.timeLastRecvd = time.time()
        self.timeoutSecs = 120
        self.__acceptConnectionsFrom = ['localhost','127.0.0.1']
        self.__isSwappingBits = False
        self.__isDebugging = False
        
    def __repr__( self):
        return '%s.SocketServer :: ipAddr=(%s), sShutdown=(%s), port=(%s), iBufSize=(%s), isSwappingBits=(%s), acceptConnectionsFrom=(%s), isDebugging=(%s)' % (__name__, str(self.ipAddr),str(self.sShutdown),str(self.port),str(self.iBufSize),self.isSwappingBits,str(self.acceptConnectionsFrom),self.isDebugging)
        
    def __reportChars__(self, chars):
        return ','.join([str(ord(ch)) for ch in chars])
    
    def termProc(self):
        pid = os.getpid()
        print >>sys.stderr, '(termProc).1 pid=(%s)' % pid
        SocketServer.__Q__.isRunning = False
        os._exit(1)

    def shutdown(self,connHandle):
        print >>sys.stderr, '(shutdown).1 connHandle.isRunning=(%s)' % connHandle.isRunning
        connHandle.isRunning = False
        if (connHandle.channel):
            print >>sys.stderr, '(shutdown).2 connHandle.isRunning=(%s)' % connHandle.isRunning
            connHandle.channel.close()
        if (connHandle.socket):
            print >>sys.stderr, '(shutdown).3 connHandle.channel.close()'
            connHandle.socket.close()
        print >>sys.stderr, '(shutdown).4 connHandle.socket.close()'
        self.termProc()

    def isCallbackValid(self):
        return str(type(self.callBack)).find("'function'") != -1
    
    def __callback__(self,connHandle,_data):
        val = ''
        if (self.isCallbackValid()):
            try:
                val = self.callBack(self,connHandle,_data)
            except Exception, details:
                print >>sys.stderr, '(__callback__) :: ERROR.2 in %s due to "%s"\n._data=(%s)\nsconnHandle.isRunning=(%s)' % (str(self.__class__),str(details),_data,connHandle.isRunning)
                val = str(details)
        return val
    
    def __sendData__(self,connHandle,_data):
        connHandle.isError = False
        try:
            while (_data):
                if (not _data.endswith('\x00')):
                    _data += '\x00'
                num = connHandle.channel.send(_data)
                _data = _data[num:]
        except Exception, details:
            if (details[-1].find('connection abort') > -1):
                if (connHandle.dropConnectionOnErrors):
                    connHandle.server.shutdown(connHandle)
            print >>sys.stderr, 'ERROR.3 in %s due to "%s".' % (str(self.__class__),str(details))
            connHandle.isError = True
        return connHandle.isError

    def __send__(self,connHandle,_data):
        try:
            if (connHandle.server.isDebugging):
                print 'Sending... [%s], len(_data)=(%s)' % (str(_data.__class__),len(_data))
                print '\t[%s]' % (_data)
        except:
            pass
        self.__sendData__(connHandle,connHandle.server.swapBitsForBytesOnSend(_data))
    
    def processData(self, connHandle, data):
        try:
            _data = data
            if (not misc.isString(data)):
                _data = str(data)
            if (_data.endswith(chr(0))):
                _data = _data[0:-1]
            _data = _data.strip()
            connHandle.server.timeLastRecvd = time.time()
            if (connHandle.server.isCallbackValid()):
                _data = connHandle.server.swapBitsForBytesOnReceive([_data[n*2:(n*2)+2] for n in xrange(len(_data)/2)])
                print '(processData).1 :: Received... (%s)' % (_data)
                val = connHandle.server.__callback__(connHandle,_data)
                if (val):
                    connHandle.server.__send__(connHandle,val)
                elif (not connHandle.restart):
                    print >>sys.stderr, '(processData).4 Connection Termination !'
                    connHandle.server.shutdown(connHandle)
                else:
                    print >>sys.stderr, '(processData).5 Connection Termination Inhibited due to connHandle.restart (%s)!' % (connHandle.restart)
        except Exception, details:
            print >>sys.stderr, '(processData).Error "%s".' % (str(details))

    @threadpool.threadify(__Q__)
    def __handleConnection__(self,connHandle):
        try:
            if (connHandle.channel):
                val = connHandle.server.__callback__(connHandle,None)
                if ( (val) and (misc.isString(val)) and (len(val) > 0) ):
                    if (connHandle.server.__send__(connHandle,val)):
                        #connHandle.server.shutdown(connHandle)
                        print >>sys.stderr, '(handleConnection).1 __Q__.isRunning=(%s).' % (SocketServer.__Q__.isRunning)
        
                while SocketServer.__Q__.isRunning:
                    print >>sys.stderr, '(handleConnection).2 __Q__.isRunning=(%s)' % (SocketServer.__Q__.isRunning)
                    data = connHandle.channel.recv(connHandle.server.iBufSize)
                    print '%s --> (%s) "%s"' % (misc.callersName(),'NOT' if (not data) else 'DATA',data)
                    if not data:
                        if (connHandle.dropConnectionOnErrors):
                            connHandle.server.shutdown(connHandle)
                            break
                    connHandle.server.processData(connHandle,data)
                print >>sys.stderr, '(handleConnection).3 __Q__.isRunning=(%s)' % (SocketServer.__Q__.isRunning)
                connHandle.channel.close()
        except Exception, details:
            print >>sys.stderr, '(handleConnection).Error "%s".' % (str(details))
            ex = str(details)
            if (ex.find('Connection reset by peer') > -1) or (ex.find('forcibly closed by the remote host') > -1):
                connHandle.server.shutdown(connHandle)

    def handleConnection(self, connHandle):
        self.__handleConnection__(connHandle)
    
    def set_acceptConnectionsFrom(self, _listOfAddresses):
        if (misc.isList(_listOfAddresses)):
            self.__acceptConnectionsFrom = _listOfAddresses
        else:
            raise ValueError
    
    def get_acceptConnectionsFrom(self):
        return self.__acceptConnectionsFrom
    
    def set_isDebugging(self,bool):
        self.__isDebugging = bool
    
    def get_isDebugging(self):
        return self.__isDebugging
    
    def set_isSwappingBits(self,bool):
        self.__isSwappingBits = bool
    
    def get_isSwappingBits(self):
        return self.__isSwappingBits
    
    def swapBits(self,byte):
        return ((byte & 0x0f) << 4) | ((byte & 0xf0) >> 4)
    
    def swapBitsForBytesOnReceive(self,bytes):
        if ( (self.isSwappingBits) or (__hex__.isHexDigits(''.join(bytes))) ):
            self.isSwappingBits = True
            return ''.join([chr(self.swapBits(__hex__.hex2dec(byte)) & 0x7f) for byte in bytes])
        return bytes
    
    def swapBitsForBytesOnSend(self,bytes):
        if (self.isSwappingBits):
            return ''.join([__hex__.dec2hex(self.swapBits(ord(byte))) for byte in bytes])
        return bytes
    
    def checkConnectionStatus(self, *args, **kwargs):
        connHandle = args[0]
        print >>sys.stderr, '(checkConnectionStatus).1 connHandle.__class__=(%s)' % (str(connHandle.__class__))
        print >>sys.stderr, '(checkConnectionStatus).2 connHandle=(%s)' % (str(connHandle))
        print >>sys.stderr, '(checkConnectionStatus).3 args=(%s), kwargs=(%s)' % (str(args),str(kwargs))
        if (not connHandle.isConnected):
            if (connHandle.dropConnectionOnErrors):
                print >>sys.stderr, '(checkConnectionStatus).4 Force shutdown due to lack of connection.'
                SocketServer.__connectionTimeoutTimer__.cancel()
                connHandle.server.shutdown(connHandle)

    def startup(self,connectionTimeout=60,restart=False,dropConnectionOnErrors=False,isDebugging=False,dataFormat=DataFormat.JSON):
        connHandle = ConnectionHandle.ConnectionHandle(timeout=connectionTimeout,restart=restart,dropConnectionOnErrors=dropConnectionOnErrors,dataFormat=dataFormat)
        connHandle.server = self
        self.isDebugging = isDebugging
        connHandle.socket = socket(AF_INET, SOCK_STREAM)
        print >>sys.stderr, '(startup).0 :: self.ipAddr=(%s), self.acceptConnectionsFrom=(%s)' % (self.ipAddr,str(self.acceptConnectionsFrom))
        print >>sys.stderr, '(startup).1 :: %s' % (self)
        if (self.ipAddr in self.acceptConnectionsFrom):
            try:
                connHandle.socket.bind( ( self.ipAddr, self.port) )
            except Exception, details:
                print >>sys.stderr, 'ERROR in startup() due to "%s".  Reason is probably due to the port "%s" being taken by another process.' % (str(details),self.port)
                return
            if (connectionTimeout > 0):
                SocketServer.__connectionTimeoutTimer__ = Timer(connectionTimeout, self.checkConnectionStatus,[connHandle])
                SocketServer.__connectionTimeoutTimer__.start()
            connHandle.socket.listen(SocketServer.__Q__.maxsize)
            connHandle.isRunning = True
            while connHandle.isRunning:
                print >>sys.stderr, '(startup).2 :: waiting for connection...'
                connHandle.channel, connHandle.details = connHandle.socket.accept()
                print >>sys.stderr, '(startup).3 :: Opened a connection with', connHandle.details
                if (SocketServer.__connectionTimeoutTimer__):
                    SocketServer.__connectionTimeoutTimer__.cancel() # cencel the timeout because we have a connection...
                self.handleConnection(connHandle)
                print >>sys.stderr, '(startup).4 :: connHandle.isRunning=(%s)' % connHandle.isRunning
            if (connHandle.isRunning):
                print >>sys.stderr, '(startup).5 connHandle.socket.close'
                connHandle.server.shutdown(connHandle)
            else:
                print >>sys.stderr, '(startup).6 shutdown !'
        else:
            print >>sys.stderr, '(startup).7 Cannot accept connections when the address is "%s" however connections can be accpeted from any of these: "%s" !' % (self.ipAddr,str(self.acceptConnectionsFrom))

    acceptConnectionsFrom = property(get_acceptConnectionsFrom, set_acceptConnectionsFrom)
    isSwappingBits = property(get_isSwappingBits, set_isSwappingBits)
    isDebugging = property(get_isDebugging, set_isDebugging)
