from vyperlogix import mongodb

if (__name__ == '__main__'):
    import os,sys
    
    sm = mongodb.SleepyMongoose('127.0.0.1:27080').db('gps_1M').collection('num_connections')
    results = sm.connect()
    print 'sm.connect() #1 --> ',results

    results = sm.server('mongodb://127.0.0.1:65535').connect()
    print 'sm.connect() #2 --> ',results

    results = sm.server('mongodb://127.0.0.1:65535').name('backup').connect()
    print 'sm.connect() #3 --> ',results

    results = sm.docs({"x":2}).insert()
    print 'sm.insert() #1 --> ',results

    results = sm.find({"x":2})
    print 'sm.find() #1 --> ',results

    results = sm.criteria({"x":2}).remove()
    print 'sm.remove() #1 --> ',results

    results = sm.docs().insert({"x":3})
    print 'sm.insert() #1 --> ',results

    results = sm.find({"x":3})
    print 'sm.find() #2 --> ',results

    results = sm.remove({"x":3})
    print 'sm.remove() #2 --> ',results

    results = sm.docs([{"x":2},{"x":3}]).insert()
    print 'sm.insert() #3 --> ',results

    results = sm.criteria({"x":2}).remove()
    print 'sm.remove() #3 --> ',results

    results = sm.criteria([{"x":3}]).remove()
    print 'sm.remove() #4 --> ',results

    results = sm.insert([{"x":2},{"x":3}])
    print 'sm.insert() #4 --> ',results

    results = sm.remove({"x":2})
    print 'sm.remove() #5 --> ',results

    results = sm.remove([{"x":3}])
    print 'sm.remove() #6 --> ',results
    pass
