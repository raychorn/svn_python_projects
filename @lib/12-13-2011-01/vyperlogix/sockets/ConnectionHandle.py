from vyperlogix.enum import Enum

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class DataFormat(Enum.Enum):
    XML = 1
    JSON = 2

class ConnectionHandle(object):
    def __init__(self, server=None, socket=None, channel=None, details=None, timeout=60, restart=False, dropConnectionOnErrors=False, dataFormat=DataFormat.XML):
        self.__server = server
        self.__socket = socket
        self.__channel = channel
        self.__details = details
        self.__timeout = timeout
        self.__restart = restart
        self.__dataFormat = dataFormat
        self.__isError = False
        self.__isRunning = False
        self.__dropConnectionOnErrors = dropConnectionOnErrors

    def __repr__( self):
        return '%s :: isConnected=(%s), channel=(%s), details=(%s), isError=(%s), isRunning=(%s), timeout=(%s), restart=(%s), dropConnectionOnErrors=(%s), dataFormat=(%s)' % (__name__,self.isConnected,str(self.channel),str(self.details),self.isError,self.isRunning,self.timeout,self.restart,self.dropConnectionOnErrors,self.dataFormat)
        
    def server():
        doc = "server"
        def fget(self):
            return self.__server
        def fset(self, server):
            self.__server = server
        return locals()
    server = property(**server())

    def socket():
        doc = "socket"
        def fget(self):
            return self.__socket
        def fset(self, socket):
            self.__socket = socket
        return locals()
    socket = property(**socket())

    def channel():
        doc = "channel"
        def fget(self):
            return self.__channel
        def fset(self, channel):
            self.__channel = channel
        return locals()
    channel = property(**channel())

    def timeout():
        doc = "timeout"
        def fget(self):
            return self.__timeout
        def fset(self, timeout):
            self.__timeout = timeout
        return locals()
    timeout = property(**timeout())

    def restart():
        doc = "restart"
        def fget(self):
            return self.__restart
        def fset(self, restart):
            self.__restart = restart
        return locals()
    restart = property(**restart())
    
    def dropConnectionOnErrors():
        doc = "dropConnectionOnErrors"
        def fget(self):
            return self.__dropConnectionOnErrors
        def fset(self, dropConnectionOnErrors):
            self.__dropConnectionOnErrors = dropConnectionOnErrors
        return locals()
    dropConnectionOnErrors = property(**dropConnectionOnErrors())
    
    def details():
        doc = "details"
        def fget(self):
            return self.__details
        def fset(self, details):
            self.__details = details
        return locals()
    details = property(**details())

    def dataFormat():
        doc = "dataFormat"
        def fget(self):
            return self.__dataFormat
        def fset(self, dataFormat):
            self.__dataFormat = dataFormat
        return locals()
    dataFormat = property(**dataFormat())

    def isXML():
        doc = "is dataFormat XML"
        def fget(self):
            return self.__dataFormat == DataFormat.XML
        return locals()
    isXML = property(**isXML())

    def isJSON():
        doc = "is dataFormat JSON"
        def fget(self):
            return self.__dataFormat == DataFormat.JSON
        return locals()
    isJSON = property(**isJSON())

    def isError():
        doc = "isError"
        def fget(self):
            return self.__isError
        def fset(self, isError):
            self.__isError = isError
        return locals()
    isError = property(**isError())

    def isRunning():
        doc = "isRunning"
        def fget(self):
            return self.__isRunning
        def fset(self, isRunning):
            self.__isRunning = isRunning
        return locals()
    isRunning = property(**isRunning())

    def isConnected():
        doc = "isConnected"
        def fget(self):
            return self.channel and self.details
        return locals()
    isConnected = property(**isConnected())
