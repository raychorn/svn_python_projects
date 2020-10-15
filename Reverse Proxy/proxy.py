import sys
import socket,asyncore

# Design Notes:
#
#  List of Nodes to choose from.
#
# Incoming connects choose a Node then make the connection.

from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName

class ReverseProxy(asyncore.dispatcher):
    def __init__(self, ip, port, remotes=[],backlog=100):
        asyncore.dispatcher.__init__(self)
        self.__remote_addresses__ = []
        for remote in remotes:
            self.__remote_addresses__.append(remote)
        self.__remote_address_num__ = 0 if (len(self.__remote_addresses__) > 0) else -1
        self.__ip__ = ip
        self.__port__ = port
        print >>sys.stdout, '%s is active.' % (str(self.__repr__()))
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)
        
    def __repr__(self):
        return '<%s> <%s:%s>' % (ObjectTypeName__typeName(self),self.ip,self.port)

    def handle_accept(self):
        conn_addr = self.accept()
        if (conn_addr):
            conn, addr = conn_addr
            remote_ip = self.next_remote_address()
            if (remote_ip is not None):
                remote_addr = remote_ip.split(':')
                print '--- Connect <%s> to <%s> --- ' % (addr,remote_addr)
                remoteip = remote_addr[0]
                remoteport = int(remote_addr[-1]) if (len(remote_addr) == 2) else -1
                is_remote_addr_valid = _utils.is_ip_address_valid(remoteip)
                if (is_remote_addr_valid):
                    sender(receiver(conn),remoteip,remoteport)
                else:
                    print >>sys.stderr, 'Cannot form a connection to %s.' % (remote_addr)
            else:
                print >>sys.stderr, 'Cannot form a connection for %s.' % (remote_ip)

    def ip():
        doc = "ip"
        def fget(self):
            return self.__ip__
        return locals()
    ip = property(**ip())

    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        return locals()
    port = property(**port())

    def remote_addresses():
        doc = "remote_addresses"
        def fget(self):
            return self.__remote_addresses__
        return locals()
    remote_addresses = property(**remote_addresses())

    def remote_address_num():
        doc = "remote_address_num"
        def fget(self):
            return self.__remote_address_num__
        return locals()
    remote_address_num = property(**remote_address_num())

    def next_remote_address(self):
        print '1. self.__remote_address_num__=%s' % (self.__remote_address_num__)
        if (self.__remote_address_num__ > -1):
            self.__remote_address_num__ += 1
            print '2. self.__remote_address_num__=%s' % (self.__remote_address_num__)
            if (self.__remote_address_num__ > len(self.__remote_addresses__)):
                self.__remote_address_num__ = 0
            print '3. self.__remote_addresses__=%s' % (self.__remote_addresses__)
            return self.__remote_addresses__[self.__remote_address_num__] if (self.__remote_address_num__ < len(self.__remote_addresses__)) else None
        return None
    
class receiver(asyncore.dispatcher):
    def __init__(self,conn):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer=''
        self.to_remote_buffer=''
        self.sender=None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        print '(%s.handle_read) %04i -->' % (self.__class__,len(read))
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        print '(%s.handle_write) %04i <--' % (self.__class__,sent)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
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
        pass

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
        self.close()
        self.receiver.close()

if __name__=='__main__':
    ReverseProxy('127.0.0.1',7777,remotes=['127.0.0.1:8080'])
    asyncore.loop()

