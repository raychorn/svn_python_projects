def dummy():
    pass

def phaseIII(d,dbx_callback=dummy,close_callback=dummy):
    import os, sys, types
    from vyperlogix import oodb
    
    print >>sys.stderr, 'Begin: Phase III'
    _cwd = os.path.abspath('.')
    fname = os.sep.join([_cwd,'db.dbx'])
    print >>sys.stderr, 'fname is "%s".' % (fname)
    _root = os.path.dirname(fname)
    _tail = os.path.splitext(fname)[-1]
    _files = [f for f in os.listdir(_root) if (f.endswith(_tail))]
    for f in _files:
        _f = os.sep.join([_root,f])
        if (os.path.exists(_f)):
            print 'Removed "%s".' % (_f)
            os.remove(_f)
    # oodb.PickleMethods.useBsdDbShelf = 1.023 secs
    # oodb.PickleMethods.useStrings = 2.151 secs
    # oodb.PickleMethods.useSafeSerializer = 16.438 secs
    # oodb.PickleMethods.useMarshal = 55.609 secs
    dbx = {}
    if (type(dbx_callback) == types.FunctionType):
        try:
            dbx = dbx_callback(fname)
        except Exception, details:
            print >>sys.stderr, 'Phase III Error :: Cannot call the dbx_callback because %s.' % (details)
    else:
        print >>sys.stderr, 'Phase III Error :: Cannot call the dbx_callback.'
    for k,v in d.iteritems():
        dbx[str(k)] = v
    if (type(close_callback) == types.FunctionType):
        try:
            close_callback(dbx)
        except Exception, details:
            print >>sys.stderr, 'Phase III Error :: Cannot call the dbx_callback because %s.' % (details)
    else:
        print >>sys.stderr, 'Phase III Error :: Cannot call the close_callback.'
    return dbx.fileName
    