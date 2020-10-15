# http://thenerdcan.wordpress.com/2007/07/25/windows-live-messenger-has-new-protocol-underway/

import socket
HOST = 'messenger.hotmail.com' # The remote host
PORT = 1863 # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('VER 0 MSNP16 CVR0\r\n')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
