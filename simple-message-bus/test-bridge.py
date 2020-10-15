import time
import simplejson

from vyperlogix import misc
from vyperlogix.misc import _utils

run_tests = [1,2]

if (__name__ == '__main__'):
    import sys
    import tcpipbridge
    if (sys.platform == 'win32'):
       
        if (1 in run_tests):
            # Test #1 :: Create a new object
            data = {'items':['1','2','3','4','5']}
            json = tcpipbridge.tcpipConnector(simplejson.dumps(data))
            print json
            print '='*40

        def __callback__(*args, **kwargs):
            print 'DEBUG.%s: args=%s, kwargs=%s' % (misc.funcName(),args,kwargs)
            return args[0].replace('@vm2','@vm1') if (len(args) > 0) else args
        
        __eof__ = '@@@EOF@@@'
        if (2 in run_tests):
            tcpipbridge.startTCPIPBridge('127.0.0.1', 55555, callback=__callback__,__eof__=__eof__)

            print '+'*40
            writer = tcpipbridge.SocketWriter('127.0.0.1', 55555)
            
            if (0):
                for i in xrange(0,100):
                    writer.send('HELLO-%s' % (i))
                    
            writer.sendFile("C:\@vm2\simple-message-bus\data.json",__eof__=__eof__)

        time.sleep(1)
        _utils.terminate('Program complete.')
else:
    print 'Do you have any idea what you are doing ?  Get a grip and figure this out !  NOW !'
