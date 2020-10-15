def phaseII(d):
    import sys
    from vyperlogix.hash import lists
    from pyax.datatype.apexdatetime import ApexDatetime
    from vyperlogix.misc import _utils
    
    print >>sys.stderr, 'Begin: Phase II'
    for k,v in d.iteritems():
        v = v if (isinstance(v,list)) else [v]
        dd = lists.HashedLists2(d)
        dd['dt'] = ApexDatetime.fromSfIso(_utils.timeStamp())
        d[k] = _utils.insert(v,len(v),dd.asDict())
    return d
