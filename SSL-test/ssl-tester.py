import socket

try:
    from socket import ssl
    isSSLclient = 1
except:
    isSSLclient = 0

import sys
print 'version=[%s]' % sys.version
print 'path=[%s]' % '\n'.join(sys.path)
print 'isSSLclient=[%s]' % isSSLclient

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.verisign.com', 443))

ssl_sock = socket.ssl(s)

print repr(ssl_sock.server())
print repr(ssl_sock.issuer())

# Set a simple HTTP request -- use httplib in actual code.
ssl_sock.write("""GET / HTTP/1.0\r
Host: www.verisign.com\r\n\r\n""")

# Read a chunk of data.  Will not necessarily
# read all the data returned by the server.
data = ssl_sock.read()

# Note that you need to close the underlying socket, not the SSL object.
del ssl_sock
s.close()

