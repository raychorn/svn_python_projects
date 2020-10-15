import os,sys

from pyax.connection import Connection
from pyax.exceptions import ApiFault

from vyperlogix.handlers.ExceptionHandler import *

import traceback

def dummy():
    pass

def runWithAnalysis(func=dummy,args=[]):
    import lib.ioTimeAnalysis
    import sfUtil
    caller = sfUtil.callersName()
    lib.ioTimeAnalysis.initIOTime('%s' % caller) 
    lib.ioTimeAnalysis.ioBeginTime('%s' % caller)
    val = None
    try:
        if (len(args) == 0):
            val = func()
        else:
            val = func(args)
    except Exception, details:
        print 'ERROR due to "%s".' % details
        traceback.print_exc()
    lib.ioTimeAnalysis.ioEndTime('%s' % caller)
    lib.ioTimeAnalysis.ioTimeAnalysisReport()
    return val
    
def processSalesForce(args):
    _username, _password, soql = args
    try:
        sfdc = Connection.connect(_username, _password)
        ret = sfdc.query(soql)
    except ApiFault, details:
        print 'ERROR due to "%s".' % (details)
        traceback.print_exc()
        ret = []
    return ret

def main():
    excp = ExceptionHandler()
    #print 'sys.version=[%s]' % sys.version
    #print 'sys.path=[%s]' % '\n'.join(sys.path)
    
    print 'sys.argv=[%s]' % sys.argv
    
    username = ''
    password = ''
    for arg in sys.argv[1:]:
        toks = arg.split('=')
        verb, noun = toks
        if (verb == '--username'):
            username = noun
        elif (verb == '--password'):
            password = noun
            
    if (len(username) > 0) and (len(password) > 0):
        #soql = "Select c.Case_Watcher__c, c.Id, c.LastModifiedDate, c.Name, c.Alias_Email__c, c.Email__c from Case_Watcher_List__c c"
        #ret = runWithAnalysis(processSalesForce,[username,password,soql])
        #print 'ret=[%s]' % ret
        pass
    else:
        print 'ERROR - Missing arguments...'

    print 'Done !'

if (__name__ == '__main__'):
    main()
