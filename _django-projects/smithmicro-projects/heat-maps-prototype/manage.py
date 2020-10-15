#!/usr/bin/env python
import os, sys
from vyperlogix.misc import _utils

from django.core.management import execute_manager

try:
    import settings # Assumed to be in the same directory.
except ImportError, details:
    info_string = _utils.formattedException(details=details)
    print >>sys.stderr, "Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__
    print >>sys.stderr, info_string
    sys.exit(1)
except Exception, details:
    info_string = _utils.formattedException(details=details)
    print >>sys.stderr, info_string
    sys.exit(1)
    
#from vyperlogix.misc import ReportTheList
#ReportTheList.reportTheList(sys.path,'sys.path',fOut=sys.stderr)

if __name__ == "__main__":
    try:
        execute_manager(settings, argv=sys.argv)
    except:
        pass
