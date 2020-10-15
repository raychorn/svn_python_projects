__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import sys

def __test_using_pylibmc__(__host__,verbose=False):
    results = False
    try:
        import pylibmc
        if (verbose):
            print 'Testing <pylibmc> ... %s' % (__host__)
        mc = pylibmc.Client([__host__], binary=True, behaviors={"tcp_nodelay": True,"ketama": True})
        if (verbose):
            print mc
    
        if (verbose):
            mc["some_key"] = "Some value"
            print mc["some_key"]
    
        assert(mc["some_key"] == "Some value")
        if (verbose):
            print 'DONE !!!'
    except ImportError, ex:
        if (verbose):
            print 'WARNING: %s' % (ex.message)
    return results

def __test_using_umemcache__(__host__,verbose=False,timeout=None):
    from vyperlogix import misc
    from vyperlogix.classes.MagicObject import Wrapper
    results = False
    try:
        import umemcache
    
        if (misc.isString(__host__)):
            __host__ = [__host__]
            
        for host in __host__:
            if (verbose):
                __activity__ = 'Testing <umemcache> ... %s' % (host)
                print __activity__
        
            #mc = umemcache.Client(host)
            __mc__ = umemcache.Client(host)
            mc = Wrapper(__mc__,callback=lambda value:value[0] if (misc.isTuple(value) and (value[-1] == 0)) else value)
            mc.connect()
            print mc

            if (verbose):
                mc.set('key', 'Some value')
                print mc.get('key')[0]
            
            mc['a'] = '1'
            if (verbose):
                print mc['a']
            mc.incr('a',1)
            if (verbose):
                print mc['a']
            mc.incr('a',10)
            if (verbose):
                print mc['a']
        
            assert(mc.get('key')[0] == "Some value")
            if (verbose):
                print 'DONE %s !!!' % (__activity__)
            results = True
    except Exception, ex:
        if (verbose):
            print 'WARNING: %s' % (ex.message)
    return results

if (__name__ == '__main__'):
    try:
        __test_using_pylibmc__('127.0.0.1:11211')
        #__test1__('memcached1.fs7l9z.cfg.use1.cache.amazonaws.com:11211')
    except:
        print 'ERROR #1'
    
    try:
        __test_using_umemcache__('127.0.0.1:11211')
        #__test2__('memcached1.fs7l9z.cfg.use1.cache.amazonaws.com:11211')
    except:
        print 'ERROR #2'

    print "Test complete."
    