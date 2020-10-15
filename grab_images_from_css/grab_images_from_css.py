import os, sys
import urllib
import re

import cssutils

from vyperlogix.daemon.daemon import EchoLog
from vyperlogix.misc import _utils

def retrieveImage( url, fname):
    urllib.urlretrieve( url, fname)

if (__name__ == '__main__'):
    fname = r'Z:\python projects\grab_images_from_css\core-2008-10-09-02-30.css'
    if (os.path.exists(fname)):
        dataPath = logPath = os.path.dirname(sys.argv[0])
        logFile = os.path.join(logPath,'logs%s%s_%s.log' % (os.sep,os.path.basename(sys.argv[0]),_utils.timeStampLocalTimeForFileName()))
        _utils.makeDirs(logFile)
        logger = EchoLog(open(logFile,'w'))
        sys.stderr = logger
        cssparser = cssutils.CSSParser()
        sheet = cssparser.parseFile(fname,href='http://www.pokerroom.com')
        num = 0
        for rule in sheet.cssRules:
            s = rule.style.cssText
            if (s.find('url(') > -1):
                url = rule.style.cssText.split('url(')[-1].split(')')[0]
                if (len(url) > 0):
                    fname = os.path.basename(url.replace('/',os.sep))
                    fpath = os.path.join(dataPath,'images%s%s' % (os.sep,fname))
                    _utils.makeDirs(fpath)
                    url = '%s%s%s' % (sheet.href,'/' if (not url.startswith('/')) else '',url)
                    print >>sys.stderr, '%s --> %s' % (url,fpath)
                    retrieveImage(url,fpath)
                    num += 1
            pass
        print >>sys.stderr, 'Done. Retrieved %d images.' % (num)
    else:
        print >>sys.stderr, '1. Nothing to do!'
    pass