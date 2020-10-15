import socket
import struct

class NoMatch(Exception):
    pass

class MessageQueue(object):
    def __init__(self, socketname, queuename, recvsize):
        self.socketname = socketname
        self.queuename = queuename
        self.recvsize = recvsize
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.socket.bind(self.socketname)
        self.queue = open(self.queuename, 'w+')

    def receive(self, pattern):
        for place, payload in self.iter_queue():
            try:
                interpreted = pattern(payload)
                self.markused(place)
                return interpreted
            except NoMatch:
                continue

        for payload in self.iter_socket(True):
            try:
                return pattern(payload)
            except NoMatch:
                self.enqueue(payload)

        for payload in self.iter_socket(False):
            self.enqueue(payload)

    def iter_queue(self):
        self.queue.seek(0)
        while True:
            place = self.queue.tell()
            sizebuffer = self.queue.read(8)
            if len(sizebuffer) != 8:
                break
            used, size = struct.unpack('ii', sizebuffer)
            if used:
                self.queue.seek(size, 1)
                continue
            payloadbuffer = self.queue.read(size)
            if len(payloadbuffer) != size:
                break
            yield place, payloadbuffer

    def iter_socket(self, blocking):
        self.socket.setblocking(blocking)
        while True:
            try:
                payloadbuffer = self.socket.recv(self.recvsize)
            except socket.error, e:
                if e.args[0] == 1:
                    break
                else:
                    raise
            yield payloadbuffer

    def markused(self, place):
        previous = self.queue.tell()
        self.queue.seek(place)
        self.queue.write(struct.pack('i', 1))
        self.queue.seek(previous)

    def enqueue(self, payload):
        self.queue.seek(0, 2)
        self.queue.write(struct.pack('ii', 0, len(payload)))
        self.queue.write(payload)

def main():
    q = MessageQueue('tests', 'testq', 4096)

    def patterna(buf):
        if buf[0] == 'a':
            return buf
        else:
            raise NoMatch, buf

    def patternb(buf):
        if buf[0] == 'b':
            return buf
        else:
            raise NoMatch, buf

    while 1:
        print 'match!', q.receive(patterna)
        print 'match!', q.receive(patternb)

def test():
    import socket
    
    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    for p in ('a', 'b'):
        for i in xrange(0, 3):
            s.sendto('%s%d' % (p, i), 'tests')
        
if __name__ == '__main__':
    main()
