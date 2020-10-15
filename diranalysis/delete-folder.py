import os, sys
import time

verbose = False
import imp
if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    import zipfile
    import pkg_resources

    import re
    __regex_libname__ = re.compile(r"(?P<libname>.*)_2_7\.zip", re.MULTILINE)

    my_file = pkg_resources.resource_stream('__main__',sys.executable)

    import tempfile
    __dirname__ = os.path.dirname(tempfile.NamedTemporaryFile().name)

    zip = zipfile.ZipFile(my_file)
    files = [z for z in zip.filelist if (__regex_libname__.match(z.filename))]
    for f in files:
        libname = f.filename
        data = zip.read(libname)
        fpath = os.sep.join([__dirname__,os.path.splitext(libname)[0]])
        __is__ = False
        if (not os.path.exists(fpath)):
            os.mkdir(fpath)
        else:
            fsize = os.path.getsize(fpath)
            if (fsize != f.file_size):
                __is__ = True
        fname = os.sep.join([fpath,libname])
        if (verbose):
            print 'INFO: fname is "%s".' % (fname)
            print 'INFO: __is__ is "%s".' % (__is__)
        if (not os.path.exists(fname)) or (__is__):
            file = open(fname, 'wb')
            file.write(data)
            file.flush()
            file.close()
            if (verbose):
                print 'INFO: fname(2) is "%s".' % (fname)
        __module__ = fname

        import zipextimporter
        zipextimporter.install()
        sys.path.insert(0, __module__)

from vyperlogix.misc import _utils
from vyperlogix.lists import ListWrapper

from vyperlogix.misc import threadpool

__Q1__ = threadpool.ThreadQueue(500)
__Q2__ = threadpool.ThreadQueue(50)

__filecount = 0
__foldercount = 0

@threadpool.threadify(__Q1__)
def remove_file(fname):
    if (os.path.exists(fname)):
        print '(-) %s' % (fname)
        os.remove(fname)
        
@threadpool.threadify(__Q2__)
def remove_folder(fname):
    if (os.path.exists(fname) and os.path.isdir(fname)):
        files = os.listdir(fname)
        while (len(files) > 0):
            time.sleep(1)
            files = os.listdir(fname)
        print '(--) %s' % (fname)
        os.rmdir(fname)

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-f", "--folder",action="store", type="string", dest="fpath")
    
    options, args = parser.parse_args()

    if (os.path.exists(options.fpath) and os.path.isdir(options.fpath)):
        for top, dirs, files in _utils.walk(options.fpath,topdown=False):
            for f in files:
                _fname = os.sep.join([top,f])
                __filecount += 1
                print '%s --> %s' % (__filecount,_fname)
                remove_file(_fname)
            __foldercount += 1
            remove_folder(top)
        print 'There are %d files in %d folders.' % (__filecount,__foldercount)
        __Q1__.join()
        __Q2__.join()
        _utils.terminate('Done !!!')
    else:
        print 'Cannot use "%s".' % (options.fpath)
    