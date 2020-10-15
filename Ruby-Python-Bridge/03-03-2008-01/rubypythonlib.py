#!/usr/bin/env python

import socket
import myeval
from threading import Thread

class rubyPythonParallelBridge():
    def __init__(self, ipAddr, port, sShutdown):
        self.context1 = {}
        self.context2 = {}
        self.sShutdown = sShutdown
        self.ipAddr = ipAddr
        self.port = port
        
    def __repr__( self):
        return '%s.rubyPythonParallelBridge :: ipAddr=(%s), sShutdown=(%s), port=(%s)' % (__name__, str(self.ipAddr),str(self.sShutdown),str(self.port))
        
    def startup(self):
        mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        mySocket.bind ( ( self.ipAddr, self.port) )
        mySocket.listen ( 1 )
        channel, details = mySocket.accept()
        print 'Opened a connection with', details
        while True:
            cmd = channel.recv(1024)
            _cmd = str(cmd)
            print 'Received... (%s)' % (_cmd)
            if (_cmd == self.sShutdown):
                print 'Shutdown Received...'
                channel.close()
                break
            try:
                val = myeval.myeval(_cmd, self.context1, self.context2)
            except Exception, details:
                val = str(details)
            print 'Sending... (%s)' % (str(val))
            channel.send(str(val))
    
class rubyPythonBridge():
    def __init__(self, ipAddr, port, sShutdown):
        self.context1 = {}
        self.context2 = {}
        self.sShutdown = sShutdown
        self.ipAddr = ipAddr
        self.port = port
        
    def __repr__( self):
        return '%s.rubyPythonBridge :: ipAddr=(%s), sShutdown=(%s), port=(%s)' % (__name__, str(self.ipAddr),str(self.sShutdown),str(self.port))
        
    def startup(self):
        mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        mySocket.bind ( ( self.ipAddr, self.port) )
        mySocket.listen ( 1 )
        channel, details = mySocket.accept()
        print 'Opened a connection with', details
        while True:
            cmd = channel.recv(1024)
            _cmd = str(cmd)
            print 'Received... (%s)' % (_cmd)
            if (_cmd == self.sShutdown):
                print 'Shutdown Received...'
                channel.close()
                break
            try:
                val = myeval.myeval(_cmd, self.context1, self.context2)
            except Exception, details:
                val = str(details)
            print 'Sending... (%s)' % (str(val))
            channel.send(str(val))
    