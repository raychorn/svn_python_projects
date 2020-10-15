from vyperlogix.sockets import traceroute

from vyperlogix.misc import _utils

if (_utils.isUsingLinux):
    __ip__ = 'google.com'
else:
    __ip__ = 'rackspace.vyperlogix.com'

if (__name__ == "__main__"):
    hops = traceroute.TraceRoute(__ip__,isDebugging=True).hops
    print 'There %s %d hop%s.' % ('are' if (hops > 1) else 'is',hops,'s' if (hops > 1) else '')