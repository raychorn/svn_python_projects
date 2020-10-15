from vyperlogix.zlib import zlibCompressor
from vyperlogix.misc import _utils

import zipfile

import gzip, zlib, base64

from vyperlogix.products import keys

dname = r'C:\Documents and Settings\c0horra\My Documents\@myFiles\@Flex Projects\AS3ZLib\myfzip\src'

if (__name__ == '__main__'):
    import os, sys
    import zipfile
    
    files = [os.path.join(dname,f) for f in os.listdir(dname) if (os.path.splitext(f)[-1] in ['.zip','.gz'])]
    for f in files:
        if (zipfile.is_zipfile(f)):
            print 'ZIP FILE named "%s".' % (f)
            zip = zipfile.ZipFile(f)
            for f in zip.filelist:
                print f.filename
            pass
        else:
            print 'NOT ZIP FILE named "%s".' % (f)
            data = zlib.compress('Now is the time for all good men to come...')
            #data = _utils.readBinaryFileFrom(f)
            try:
                s = zlib.decompress(data)
            except Exception, e:
                print 'ERROR: %s' % (_utils.formattedException(e))
            else:
                x = keys._encode(data)
                _utils.writeFileFrom('_x_.zlib.hex',x,mode='w')
            print s
            print '='*40
            print
    pass