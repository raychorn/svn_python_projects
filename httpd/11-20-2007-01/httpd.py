import socket
import BaseHTTPServer
#import lib.threadpool

#_pool = lib.threadpool.Pool(1000)

#@lib.threadpool.threadpool(_pool)
def processRequest(r):
    _socket = r[0]
    data = _socket.recv(65535)
    print '(processRequest) :: r.__class__=(%s) [%s]\ndata=[%s]' % (str(r.__class__),str(r),str(data))
    _socket.send('To-Do.txt')

class Server(BaseHTTPServer.HTTPServer):
    """HTTPServer class with timeout."""

    def get_request(self):
        """Get the request and client address from the socket."""
        # 10 second timeout
        self.socket.settimeout(10.0)
        result = None
        while result is None:
            try:
                result = self.socket.accept()
                self.socket.send('<root></root>')
            except socket.timeout:
                pass
        # Reset timeout on the new socket
        result[0].settimeout(None)
        return result

if __name__ == '__main__':
    from SimpleHTTPServer import SimpleHTTPRequestHandler

    server = Server(('localhost', 7800), SimpleHTTPRequestHandler)
    print 'Serving (%s)' % (str(server.server_address))
    server.serve_forever()