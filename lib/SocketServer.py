from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_ERROR
import time
import os
import sys
import math
from threading import Timer
import win32api
from lib import threadpool
from lib import ConnectionHandle
from lib import WinProcesses
from lib import PrettyPrint
from lib import hexConversions

_pool = threadpool.Pool(10)

_connectionTimeoutTimer = -1

def termProc():
    pid = os.getpid()
    print >>sys.stderr, '(termProc).1 pid=(%s)' % pid
    _pool.isRunning = False
    os._exit(1)

def processData(connHandle, data):
    try:
        _data = data
        if (not isinstance(data,str)):
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
            else:
                print >>sys.stderr, '(processData).4 Connection Termination !'
                connHandle.server.shutdown(connHandle)
    except Exception, details:
        print >>sys.stderr, '(processData).Error "%s".' % (str(details))

@threadpool.threadpool(_pool)
def handleConnection(connHandle):
    try:
        if (connHandle.channel):
            val = connHandle.server.__callback__(connHandle,None)
            if ( (val) and (isinstance(val,str)) and (len(val) > 0) ):
                if (connHandle.server.__send__(connHandle,val)):
                    connHandle.server.shutdown(connHandle)
                    print >>sys.stderr, '(handleConnection).1 _pool.isRunning=(%s).' % (_pool.isRunning)
    
            while _pool.isRunning:
                print >>sys.stderr, '(handleConnection).2 _pool.isRunning=(%s)' % (_pool.isRunning)
                data = connHandle.channel.recv(connHandle.server.iBufSize)
                if not data:
                    connHandle.server.shutdown(connHandle)
                    break
                connHandle.server.processData(connHandle,data)
            print >>sys.stderr, '(handleConnection).3 _pool.isRunning=(%s)' % (_pool.isRunning)
            connHandle.channel.close()
    except Exception, details:
        print >>sys.stderr, '(handleConnection).Error "%s".' % (str(details))
        if (str(details).find('Connection reset by peer') > -1):
            connHandle.server.shutdown(connHandle)

def sendData(connHandle,_data):
    connHandle.isError = False
    try:
        while (_data):
            if (not _data.endswith('\x00')):
                _data += '\x00'
            num = connHandle.channel.send(_data)
            _data = _data[num:]
    except Exception, details:
        if (details[-1].find('connection abort') > -1):
            connHandle.server.shutdown(connHandle)
        print >>sys.stderr, 'ERROR.3 in %s due to "%s".' % (str(self.__class__),str(details))
        connHandle.isError = True
    return connHandle.isError

def dummy():
    pass

def checkConnectionStatus(*args, **kwargs):
    connHandle = args[0]
    print >>sys.stderr, '(checkConnectionStatus).1 connHandle.__class__=(%s)' % (str(connHandle.__class__))
    print >>sys.stderr, '(checkConnectionStatus).2 connHandle=(%s)' % (str(connHandle))
    print >>sys.stderr, '(checkConnectionStatus).3 args=(%s), kwargs=(%s)' % (str(args),str(kwargs))
    if (not connHandle.isConnected):
        print >>sys.stderr, '(checkConnectionStatus).4 Force shutdown due to lack of connection.'
        _connectionTimeoutTimer.cancel()
        connHandle.server.shutdown(connHandle)

class SocketServer():
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
        
    def __repr__( self):
        return '%s.SocketServer :: ipAddr=(%s), sShutdown=(%s), port=(%s), iBufSize=(%s), isSwappingBits=(%s), acceptConnectionsFrom=(%s)' % (__name__, str(self.ipAddr),str(self.sShutdown),str(self.port),str(self.iBufSize),self.isSwappingBits,str(self.acceptConnectionsFrom))
        
    def __reportChars__(self, chars):
        return ','.join([str(ord(ch)) for ch in chars])
    
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
        termProc()

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
    
    def __send__(self,connHandle,_data):
        try:
            print 'Sending... [%s], len(_data)=(%s)' % (str(_data.__class__),len(_data))
            print '\t[%s]' % (_data)
        except:
            pass
        sendData(connHandle,connHandle.server.swapBitsForBytesOnSend(_data))
    
    def processData(self, connHandle, data):
        processData(connHandle, data)

    def handleConnection(self, connHandle):
        handleConnection(connHandle)
    
    def set_acceptConnectionsFrom(self, _listOfAddresses):
        if (isinstance(_listOfAddresses,list)):
            self.__acceptConnectionsFrom = _listOfAddresses
        else:
            raise ValueError
    
    def get_acceptConnectionsFrom(self):
        return self.__acceptConnectionsFrom
    
    def set_isSwappingBits(self,bool):
        self.__isSwappingBits = bool
    
    def get_isSwappingBits(self):
        return self.__isSwappingBits
    
    def swapBits(self,byte):
        return ((byte & 0x0f) << 4) | ((byte & 0xf0) >> 4)
    
    def swapBitsForBytesOnReceive(self,bytes):
        if ( (self.isSwappingBits) or (hexConversions.isHexDigits(''.join(bytes))) ):
            self.isSwappingBits = True
            return ''.join([chr(self.swapBits(hexConversions.hex2dec(byte)) & 0x7f) for byte in bytes])
        return bytes
    
    def swapBitsForBytesOnSend(self,bytes):
        if (self.isSwappingBits):
            return ''.join([hexConversions.dec2hex(self.swapBits(ord(byte))) for byte in bytes])
        return bytes
    
    def startup(self,dropConnectionOnErrors=False):
        global _connectionTimeoutTimer
        connHandle = ConnectionHandle.ConnectionHandle()
        connHandle.server = self
        connHandle.socket = socket(AF_INET, SOCK_STREAM)
        print >>sys.stderr, '(startup).0 :: self.ipAddr=(%s), self.acceptConnectionsFrom=(%s)' % (self.ipAddr,str(self.acceptConnectionsFrom))
        if (self.ipAddr in self.acceptConnectionsFrom):
            try:
                connHandle.socket.bind( ( self.ipAddr, self.port) )
            except Exception, details:
                print >>sys.stderr, 'ERROR in startup() due to "%s".  Reason is probably due to the port "%s" being taken by another process.' % (str(details),self.port)
                return
            _connectionTimeoutTimer = Timer(60.0, checkConnectionStatus,[connHandle])
            _connectionTimeoutTimer.start()
            connHandle.socket.listen(_pool.maxsize)
            connHandle.isRunning = True
            while connHandle.isRunning:
                print >>sys.stderr, '(startup).1 :: waiting for connection...'
                connHandle.channel, connHandle.details = connHandle.socket.accept()
                print >>sys.stderr, '(startup).2 :: Opened a connection with', connHandle.details
                _connectionTimeoutTimer.cancel()
                self.handleConnection(connHandle)
                print >>sys.stderr, '(startup).3 :: connHandle.isRunning=(%s)' % connHandle.isRunning
            if (connHandle.isRunning):
                print >>sys.stderr, '(startup).4 connHandle.socket.close'
                connHandle.server.shutdown(connHandle)
            else:
                print >>sys.stderr, '(startup).5 shutdown !'
        else:
            print >>sys.stderr, '(startup).6 Cannot accept connections when the address is "%s" however connections can be accpeted from any of these: "%s" !' % (self.ipAddr,str(self.acceptConnectionsFrom))

    acceptConnectionsFrom = property(get_acceptConnectionsFrom, set_acceptConnectionsFrom)
    isSwappingBits = property(get_isSwappingBits, set_isSwappingBits)
