__copyright__ = """\
(c). Copyright 1990-2008, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

See also: http://www.VyperLogix.com and http://www.pypi.info for details.

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

__version__ = "0.2.1.2"

import sys

import BaseHTTPServer, select, socket, SocketServer, urlparse

from vyperlogix.classes.CooperativeClass import Cooperative

from vyperlogix.lists.ListWrapper import CircularList

from vyperlogix.sockets.proxies.TinyHTTPProxy import VyperProxy
from vyperlogix.sockets.proxies.TinyHTTPProxy import start_VyperProxy

from vyperlogix.misc import ObjectTypeName

if __name__ == '__main__':
    from sys import argv
    import sys
    allowed = []
    deletes = {}
    for i in xrange(1,len(argv)):
        if (argv[i] in ['-h', '--help']):
            print argv[0], "[port [allowed_client_name ...]]"
            sys.exit(1)
        elif (argv[i] in ['--hosts']):
            try:
                hosts = argv[i+1].split(',')
                print >>sys.stderr, '%s %s %s' % (argv[0],argv[i],hosts)
                VyperProxy.remotes = CircularList(hosts)
                deletes[i] = argv[i]
                deletes[i+1] = argv[i+1]
            except:
                pass
        elif (argv[i] in ('--allowed')):
            try:
                name = argv[i+1]
                client = socket.gethostbyname(name)
                allowed.append(client)
                print "Accept: %s (%s)" % (client, name)
                VyperProxy.allowed_clients = allowed
                deletes[i] = argv[i]
                deletes[i+1] = argv[i+1]
            except:
                pass
    if (len(allowed) == 0):
        print "Any clients will be served..."
    for k,v in deletes.iteritems():
        argv[k] = None
    start_VyperProxy()

if (__name__ == '__main__'):
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
