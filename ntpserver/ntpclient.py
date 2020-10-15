#!/usr/bin/python

# File: Ntpclient.py
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time

# # Set the socket parameters 

host = "127.0.0.1" # "16.83.121.123" # "pool.ntp.org"
port = 123
buf = 1024
address = (host,port)
msg = 'time'


# reference time (in seconds since 1900-01-01 00:00:00)
TIME1970 = 2208988800L # 1970-01-01 00:00:00

# connect to server
client = socket.socket( AF_INET, SOCK_DGRAM)
client.sendto(msg, address)
msg, address = client.recvfrom( buf )

t = struct.unpack( "!12I", data )[10]
t -= TIME1970
print "\tTime=%s" % time.ctime(t)