from vyperlogix import misc
from vyperlogix.parsers import CSV

from props_parser import parse_props_file
from props_parser import parse_url

if (__name__ == '__main__'):
    import os, sys
    import urllib
    import urllib2
    from vyperlogix.misc import _utils
    from vyperlogix.hash import lists
    from vyperlogix.lists.ListWrapper import ListWrapper

    text_file_name = r'globalnav.properties.txt'
    csv_file_name = r'GN+AM_Matrix_Defaults_20091113-shortened.csv'
    props_file_name = r"C:\Documents and Settings\c0horra\My Documents\@myFiles\python-projects\verizonwireless\django\static\global-nav\globalnav.properties.props"
    
    fname = props_file_name
    print 'Reading "%s".' % (fname)
    
    if (fname == text_file_name):
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
    elif (fname == props_file_name):
        def report_data(_d_,fOut):
            keys = misc.sortCopy(_d_.keys())
            for k in keys:
                v = _d_[k]
                if (lists.isDict(v)):
                    if (len(k) > 0):
                        print >>fOut, k
                    _fOut = _utils.stringIO()
                    report_data(v,_fOut)
                    print >>fOut, _fOut.getvalue()
                else:
                    print >>fOut, '%s=%s' % (k,v)
        
        d,dd = parse_props_file(fname,mode=2)
                    
        csv = CSV.CSV(filename=csv_file_name)
        _domains = csv.associationsBy("Domain")
        
        domains = lists.HashedLists()
        protocols = lists.HashedLists()
        for k,v in _domains.iteritems():
            so = parse_url(k,value=v)
            domains[so.domain] = so
            protocols[so.protocol] = so

        existing_domains = lists.HashedLists()
        new_domains = lists.HashedLists()
        for k,v in dd.iteritems():
            so = parse_url(k,value=v)
            print so.domain, '==>',
            if (dd.has_key(so.domain)):
                existing_domains[so.domain] = (v,dd[so.domain])
                print '(Found #%d)' % (len(existing_domains))
            else:
                new_domains[so.domain] = v
                print '(New #%d)' % (len(new_domains))
                
        if (len(existing_domains)):
            print 'There are %d existing domains.' % (len(existing_domains))
        if (len(new_domains)):
            print 'There are %d new domains.' % (len(new_domains))
        
        if (len(d) > 0):
            print '='*40
            print '%s file.' % (props_file_name)
            fOut = _utils.stringIO()
            report_data(d,fOut)
            print '-'*40
            print fOut.getvalue()
            print '='*40

        if (len(dd) > 0):
            print '='*40
            print 'Domain Analysis'
            fOut = _utils.stringIO()
            report_data(dd,fOut)
            print '-'*40
            print fOut.getvalue()
            print '='*40

        if (len(new_domains) > 0):
            print '='*40
            print 'New Domains'
            fOut = _utils.stringIO()
            report_data(new_domains,fOut)
            print '-'*40
            print fOut.getvalue()
            print '='*40
    
    print 'DONE !'
    pass
