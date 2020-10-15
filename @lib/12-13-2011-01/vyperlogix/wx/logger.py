import sys, logging

import wx

from vyperlogix.misc import _utils

from vyperlogix.classes.CooperativeClass import Cooperative

class wxLog(Cooperative):
    """
    Works like print >>wxLog, '%s' % (foo)
    """
    def __init__(self, f):
        self.f = f
        
    def fileno(self):
        return -1
    
    def _appendText(self,log,x):
	try:
	    x = x.strip()
	    log.AppendText(x+'\n')
	    print >>sys.stdout, x
	except Exception, details:
	    _details = _utils.formattedException(details)
	    print >>sys.stderr, _details

    def write(self, s):
        if (self.f):
            try:
		wx.CallAfter(self._appendText,self.f,s)
            except Exception, details:
                info_string = _utils.formattedException(details=details)
		print >>sys.stderr, info_string
            
    def close(self):
	pass

    def flush(self):
	pass

class wxSimpleLog(wxLog):
    """
    Works like print >>wxLog, '%s' % (foo)
    """
    def _appendText(self,log,x):
	try:
	    x = x.strip()
	    print >>sys.stdout, x
	except Exception, details:
	    _details = _utils.formattedException(details)
	    print >>sys.stderr, _details

