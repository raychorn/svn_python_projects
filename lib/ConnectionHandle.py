class ConnectionHandle(object):
    def __init__(self, server=None, socket=None, channel=None, details=None):
        self.__server = server
        self.__socket = socket
        self.__channel = channel
        self.__details = details
        self.__isError = False
        self.__isRunning = False

    def __repr__( self):
        return '%s :: isConnected=(%s), channel=(%s), details=(%s), isError=(%s), isRunning=(%s)' % (__name__,self.isConnected,str(self.channel),str(self.details),self.isError,self.isRunning)
        
    def getIsRunning(self):
        return self.__isRunning
    
    def setIsRunning(self,isRunning):
        self.__isRunning = isRunning
        
    def getIsError(self):
        return self.__isError
    
    def setIsError(self,isError):
        self.__isError = isError
        
    def getServer(self):
        return self.__server
    
    def setServer(self,server):
        self.__server = server
        
    def getSocket(self):
        return self.__socket
    
    def setSocket(self,socket):
        self.__socket = socket
        
    def getChannel(self):
        return self.__channel
    
    def setChannel(self,channel):
        self.__channel = channel
        
    def getDetails(self):
        return self.__details
    
    def setDetails(self,details):
        self.__details = details
        
    def getIsConnected(self):
        return self.channel and self.details
    
    server = property(getServer, setServer)
    socket = property(getSocket, setSocket)
    channel = property(getChannel, setChannel)
    details = property(getDetails, setDetails)
    isError = property(getIsError, setIsError)
    isRunning = property(getIsRunning, setIsRunning)
    isConnected = property(getIsConnected)

