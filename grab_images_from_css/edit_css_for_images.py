import os, sys

from vyperlogix.daemon.daemon import EchoLog
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

if (__name__ == '__main__'):
    url_prefix = 'http://media.vyperlogix.com/jquery/validator/images/'
    images = os.listdir(os.path.abspath('images'))
    css_fname = r'Z:\python projects\grab_images_from_css\core-2008-10-09-02-30.css'
    if (os.path.exists(css_fname)):
        dataPath = logPath = os.path.dirname(sys.argv[0])
        logFile = os.path.join(logPath,'logs%s%s_%s.log' % (os.sep,os.path.basename(sys.argv[0]),_utils.timeStampLocalTimeForFileName()))
        _utils.makeDirs(logFile)
        logger = EchoLog(open(logFile,'w'))
        sys.stderr = logger
        css_content = _utils.readFileFrom(css_fname,noCRs=False)
        toks = css_content.split('url(')
        num = 0
        d = lists.HashedLists2()
        for image in images:
            d[image] = image
        for image in images:
            for i in xrange(0,len(toks)):
                t = toks[i]
                x = t.find(')')
                if (x > -1):
                    ipath = t[0:x]
                    if (ipath.find(image) > -1):
                        toks[i] = toks[i][x:]
                        image_url = '%s%s' % (url_prefix,image)
                        toks[i] = '%s%s' % (image_url,toks[i])
                        del d[image]
                        num += 1
                        break
        css_content = 'url('.join(toks)
        new_css_fname = os.path.join(dataPath,'styles.css')
        _utils.writeFileFrom(new_css_fname,css_content)
        print >>sys.stderr, 'Done. Replace URLs for %d images.' % (num)
        print >>sys.stderr, 'BEGIN: Did not do anything with these images:'
        for k,v in d.iteritems():
            print >>sys.stderr, '%s' % (v)
        print >>sys.stderr, 'END!   Did not do anything with these images:'
    else:
        print >>sys.stderr, '1. Nothing to do!'
    pass