import socket

try:
    from socket import ssl
    isSSLclient = 1
except:
    isSSLclient = 0

import sys
print 'path=[%s]' % '\n'.join(sys.path)
#print 'isSSLclient=[%s]' % isSSLclient

print '\nversion=[%s]' % sys.version
if (not isSSLclient):
    print '\nThis version of Python (%s) is NOT able to do any SSL.\n' % sys.version

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.verisign.com', 443))

try:
    ssl_sock = socket.ssl(s)
except:
    print 'This confirms the fact that this version (%s) of Python CANNOT do SSL socket operations at-all.' % sys.version
    print '\nThis concludes this test... however since this test FAILED the rest of the SSL test code cannot be run at this time.'
    print '\nThis SSL socket test FAILS for Python version %s' % sys.version
    print '\nFor validation you may run this test with Python 2.5.2 or later.'
    sys.exit(-1)

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

print 'This confirms the fact that this version (%s) of Python CAN do SSL socket operations.' % sys.version
print '\nThis concludes this test... and this test was a SUCCESS.'
print '\nThis SSL socket test PASSED for Python version %s' % sys.version