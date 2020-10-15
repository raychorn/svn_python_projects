from vyperlogix.misc import _utils

import ultramemcache
mc = ultramemcache.Client(['127.0.0.1:11211'], debug=0)

try:
    stats = mc.servers[0].stats()

    some_key = 'key1'
    
    mc.set(some_key, 'Some value')
    value = mc.get(some_key)
    print '%s=%s' % (some_key,value)
    mc.delete(some_key)
    
    another_key = 'key2'
    
    mc.set(another_key, 3)
    value = mc.get(another_key)
    print '%s=%s' % (another_key,value)
    mc.delete(another_key)
    
    key = 'key3'
    
    mc.set(key, 1)   # note that the key used for incrdecr must be a string.
    value = mc.get(key)
    print '%s=%s' % (key,value)
    mc.incr(key)
    value = mc.get(key)
    print '%s=%s' % (key,value)
    mc.decr(key)
    value = mc.get(key)
    print '%s=%s' % (key,value)
    mc.delete(key)
except Exception, ex:
    info_string = _utils.formattedException(details=ex)
    print info_string

