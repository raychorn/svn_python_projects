from lib import socks
from lib import threadpool
import psyco

_pool = lib.threadpool.Pool(100)

@lib.threadpool.threadpool(_pool)
def createAnotherServer():
    print '(createAnotherServer) :: '

__shutdown__ = '@@@Shutdown@@@'
__ipAddr__ = 'localhost'
__port__ = 8000
__bufSize__ = 1024

def handle_callback(args):
    print '(handle_callback) :: args=(%s)' % (str(args))
    return str(args)

def main():
    theServer = lib.socks.parallelBridge(__ipAddr__, __port__,__shutdown__, __bufSize__, handle_callback)
    print 'theServer=(%s)' % (str(theServer))
    theServer.startup()

if (__name__ == '__main__'):
    psyco.bind(main)
    main()

