if (__name__ == '__main__'):
    import os, sys
    import urllib
    from vyperlogix.misc import _utils
    from vyperlogix.hash import lists
    from vyperlogix.lists.ListWrapper import ListWrapper

    fname = r'globalnav.properties.txt'
    print 'Reading "%s".' % (fname)
    props = dict([tuple(toks) for toks in [t.strip().split('=') for t in _utils.readFileFrom(fname).split('\n') if (len(t.strip()) > 0)] if (len(toks) == 2)])
    
    d_props = lists.HashedLists()
    
    for k,v in props.iteritems():
        domain = ''
        toks = ListWrapper(v.split('/'))
        i = toks.findFirstMatching('')
        if (i > -1) and (i+1 < len(toks)):
            domain = toks[i+1]
            d_props[domain] = v
            
    s_props = _utils.stringIO()
    for k,v in d_props.iteritems():
        print >> s_props, '%s' % (k)

    toks = list(os.path.splitext(fname))
    toks[-1] = '.props'
    fname2 = ''.join(toks)
    print 'Writing "%s".' % (fname2)
    _utils.writeFileFrom(fname2,s_props.getvalue())
    print 'DONE !'
    pass
