import socket,asyncore

class ReverseProxy(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, backlog=5, buffered=False):
        asyncore.dispatcher.__init__(self)
        self.remoteip=remoteip
        self.remoteport=remoteport
        self.buffered=buffered
        self.__cache__ = None
        if (self.buffered):
            from vyperlogix.cache.lru import LRUCache
            self.__cache__ = LRUCache(size=1000)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        print '--- Connect --- %s ' % ('(%s)'%(self.__cache__) if (self.__cache__) else '')
        sender(receiver(conn,cache=self.__cache__),self.remoteip,self.remoteport)

class receiver(asyncore.dispatcher):
    def __init__(self,conn,cache=None):
        asyncore.dispatcher.__init__(self,conn)
        self.to_remote_buffer=''
        self.sender=None
        self.cache=cache

    def handle_connect(self):
        print '(%s.handle_connect)' % (self.__class__)

    def handle_read(self):
        read = self.recv(4096)
        print '(%s.handle_read) (cache=%s) %04i -->' % (self.__class__,self.cache,len(read))

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        print '(%s.handle_write) (cache=%s) %04i <--' % (self.__class__,self.cache,sent)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        print '(%s.handle_close)' % (self.__class__)
        self.close()
        if self.sender:
            self.sender.close()

class sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr,remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver=receiver
        receiver.sender=self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        print '(%s.handle_connect)' % (self.__class__)

    def handle_read(self):
        read = self.recv(4096)
        print '(%s.handle_read) %04i -->' % (self.__class__,len(read))
        self.receiver.to_remote_buffer += read

    def writable(self):
        return (len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        print '(%s.handle_write) %04i <--' % (self.__class__,sent)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        print '(%s.handle_close)' % (self.__class__)
        self.close()
        self.receiver.close()

if __name__=='__main__':
    import optparse
    parser = optparse.OptionParser()

    def optional_arg(arg_default):
        def func(option,opt_str,value,parser):
            if parser.rargs and not parser.rargs[0].startswith('-'):
                val=parser.rargs[0]
                parser.rargs.pop(0)
            elif (opt_str == '-b'):
                val=True
            else:
                val=arg_default
            setattr(parser.values,option.dest,val)
        return func
    
    parser.add_option(
        '-l','--local-ip',
        dest='local_ip',default='127.0.0.1',
        help='Local IP address to bind to')
    parser.add_option(
        '-p','--local-port',
        type='int',dest='local_port',default=80,
        help='Local port to bind to')
    parser.add_option(
        '-r','--remote-ip',dest='remote_ip',
        help='Local IP address to bind to')
    parser.add_option(
        '-P','--remote-port',
        type='int',dest='remote_port',default=80,
        help='Remote port to bind to')
    parser.add_option(
        '-b','--buffer',
        dest='buffered',action='callback',callback=optional_arg(False),
        help='Buffered - stores requests.')
    options, args = parser.parse_args()

    print 'ReverseProxy(local_ip=%s,local_port=%s%s)' % (options.local_ip,options.local_port,(',buffered=%s'%(options.buffered)) if (options.buffered) else (',remote_ip=%s,remote_port=%s'%(options.remote_ip,options.remote_port)))
    ReverseProxy(options.local_ip,options.local_port,options.remote_ip,options.remote_port,buffered=options.buffered)
    asyncore.loop()

