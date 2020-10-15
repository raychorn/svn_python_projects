from vyperlogix.google import google
from vyperlogix.misc import _psyco
from vyperlogix import oodb
import datetime
import os
import sys

_psyco.importPsycoIfPossible()

_rootFolderName = 'searches'

_keywords = ['Python']

__dbx_domainName = 'domainNames.dbx'
__dbx_date = 'date.dbx'

_numPages = 999

_numPerPage = 10

for keyword in _keywords:
    _rootFolder = _rootFolderName
    if (not os.path.exists(_rootFolderName)):
        os.mkdir(_rootFolderName)
    _rootFolder = os.path.sep.join([_rootFolderName,keyword])
    if (not os.path.exists(_rootFolder)):
        os.mkdir(_rootFolder)
    _dbx_domainName = os.path.sep.join([_rootFolder,__dbx_domainName])
    dbx_domain = oodb.PickledHash(_dbx_domainName,oodb.PickleMethods.useSafeSerializer)
    _dbx_date = os.path.sep.join([_rootFolder,__dbx_date])
    dbx_date = oodb.PickledHash(_dbx_date,oodb.PickleMethods.useSafeSerializer)
    
    _urlBucket = []
    _index = -1
    for i in xrange(0,_numPages+1):
        l = len(_urlBucket)
        try:
            d = google.performGoogleSearch(keyword,_index)
            print str(d)
        
            if (d.has_key('parser')):
                p = d['parser'][0]
                for u in p.tagContents:
                    toks = u.split('//')
                    if (toks[0] in ['http:','https:']):
                        del toks[0]
                    _urlBucket.append(u)
                    dbx_domain[toks[0]] = u
                    dbx_date[datetime.datetime.now().isoformat(' ').split()[0]] = u
                if (len(p.tagContents) < 5):
                    print '\nHad to stop. Seems like there are no more URLs. #1 (%s)\n' % len(p.tagContents)
                    break
            _index += _numPerPage + (1 if _index < 0 else 0)
        except:
            print '\nHad to stop. Seems like there are no more URLs. #2 (%s)\n' % len(p.tagContents)
            break
        
    print 'There are %s raw URLs.' % len(_urlBucket)
    
    _urlBucket = list(set(_urlBucket))
    
    print 'There are %s unique URLs.' % len(_urlBucket)
    
    i = 1
    for u in _urlBucket:
        print '%s :: %s' % (i,u)
        i += 1

    dbx_domain.close()
    dbx_date.close()

# Note: pyOODB by date->search_term,results_list
# Deterine if anything changed from the prior day and make those items 'new'.

# Categorize the links by sorting on the domain name.

# pyOODB indexes:
# domain name & date found

