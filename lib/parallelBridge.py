from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_ERROR
import time

_const_issue_callback = '@@@IssueCallback@@@'

def dummy():
    pass

class parallelBridge():
    def __init__(self, ipAddr, port, sShutdown, iBufSize, _callBack):
        self.ipAddr = ipAddr
        if (len(self.ipAddr) == 0):
            self.ipAddr = 'localhost'
        self.port = port
        if (str(self.port).isdigit() == False):
            self.port = 7800
        self.sShutdown = sShutdown
        if (len(self.sShutdown) == 0):
            self.sShutdown = '@@@Shutdown@@@'
        self.iBufSize = iBufSize
        if (str(self.iBufSize).isdigit() == False):
            self.iBufSize = 1024
        self.callBack = _callBack
        if (str(self.callBack.__class__).find("'function'") == -1):
            self.callBack = dummy
        
    def __repr__( self):
        return '%s.parallelBridge :: ipAddr=(%s), sShutdown=(%s), port=(%s), iBufSize=(%s)' % (__name__, str(self.ipAddr),str(self.sShutdown),str(self.port),str(self.iBufSize))
        
    def reportChars(self, chars):
        return ','.join([str(ord(ch)) for ch in chars])
    
    def parse(self, stream):
        d = {}
        toks = stream.split(chr(127))
        for t in toks:
            try:
                k, v = t.split('=')
            except:
                k, v = ('stream',stream)
            if (d.has_key(k)):
                c = [d[k]]
                d[k] = c
                c = d[k]
            else:
                c = []
            if (str(c.__class__).find("'list'") > -1):
                c.append(v)
                d[k] = c
            else:
                d[k] = v
        return d
    
    def startup(self):
        mySocket = socket ( AF_INET, SOCK_STREAM, 0)
        mySocket.bind ( ( self.ipAddr, self.port) )
        mySocket.listen ( 10 )
        channel, details = mySocket.accept()
        print 'Opened a connection with', details
        isRunning = True
        while isRunning:
            hasValue = True
            try:
                cmd = channel.recv(self.iBufSize)
            except:
                isRunning = False
                continue
            _cmd = str(cmd).strip()
            if (_cmd.endswith(chr(0))):
                _cmd = _cmd[0:-1]
            d = self.parse(_cmd)
            print 'Received... (%s) [%s]' % (_cmd,self.reportChars(_cmd))
            print '\td=(%s)' % (str(d))
            if (_cmd == self.sShutdown):
                print 'Shutdown Received...'
                channel.close()
                break
            elif (_cmd == _const_issue_callback):
                print 'Callback Request Received...'
                try:
                    val = self.callBack(d)
                except:
                    pass
                hasValue = False
                continue
            if (hasValue):
                try:
                    val = str(_cmd)
                except Exception, details:
                    val = str(details)
            #val = 'OK'
            val = '<root>' + val + '</root>'
            try:
                print 'Sending... (%s)' % (val)
                while (val):
                    if (not val.endswith('\x00')):
                        val += '\x00'
                    num = channel.send(val)
                    val = val[num:]
            except:
                isRunning = False
                continue
    
