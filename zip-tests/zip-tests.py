# Pack a string into a deeply nested ZIP
import os, sys
import zipfile
import zlib

sys.path += ['Z:\python projects\@lib']

from vyperlogix.oodb import *
from vyperlogix.hash import lists
from vyperlogix.misc import _utils
from vyperlogix.misc import ioTimeAnalysis
from vyperlogix.decorators import TailRecursive

test_string = lambda x:''.join([chr(ch) for ch in xrange(128,128+min(x,127))])
hide_string = lambda x:''.join([chr(ord(ch)+128) for ch in x])

csv_string = lambda d:','.join(['%d' % ord(ch) for ch in d])

rosetta_stone = lists.HashedLists2()

def writeZip(_fname):
    z = zipfile.ZipFile(_fname,'w')
    try:
        s = test_string(127)

        data = zlib.compress(s,zlib.Z_BEST_COMPRESSION)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_BEST_COMPRESSION)
        hh_data = hide_string(h_data)

        methods = [('test_%s' % (zlib.Z_BEST_COMPRESSION),data),('test_h_%s' % (zlib.Z_BEST_COMPRESSION),h_data),('test_z_%s' % (zlib.Z_BEST_COMPRESSION),z_data),('test_hh_%s' % (zlib.Z_BEST_COMPRESSION),hh_data)]
        for m,d in methods:
            rosetta_stone[m] = d
            print '%s :: %s = %s' % (_utils.funcName(),m,csv_string(d))
            z.writestr(m,d)

    finally:
        z.close()

def readZip(_fname):
    z = zipfile.ZipFile(_fname,'r')
    try:
        for zm in [zlib.Z_BEST_COMPRESSION,zlib.Z_BEST_SPEED,zlib.Z_DEFAULT_COMPRESSION]:
            for zs in ['test_%s','test_h_%s','test_z_%s','test_hh_%s']:
                try:
                    z_method = zs % (zm)
                    z_str = z.read(z_method)
                    assert z_str == rosetta_stone[z_method], 'Oops, something went wrong with the retrieval of the data; "%s" was expected but "%s" was read.' % (csv_string(rosetta_stone[z_method],csv_string(z_str)))
                    print '%s = %s' % (z_method,csv_string(z_str))
                except:
                    pass
    finally:
        z.close()

def rreadZip(root,fname,sname):
    z = zipfile.ZipFile(fname,'r')
    try:
        zfiles = [zn.filename for zn in z.filelist]
        nzfiles = [zn for zn in zfiles if (not zn.endswith('.zip'))]
        zzfiles = [zn for zn in zfiles if (zn.endswith('.zip'))]
        if (sname in nzfiles):
            print '%s :: FOUND "%s" in "%s".' % (_utils.funcName(),sname,fname)
        else:
            for f in zzfiles:
                data = z.read(f)
                fq = os.sep.join([root,f])
                _utils.writeFileFrom(fq,data,'wb')
                rreadZip(root,fq,sname)
                _utils.safely_remove(fq)
    finally:
        z.close()

def dropIntoZip(fname,level=1):
    toks = fname.split('.')
    toks[0] += '_%s' % (level)
    _fname = '.'.join(toks)
    z = zipfile.ZipFile(_fname,'w')
    try:
        z_name = os.path.basename(fname)
        data = _utils.readFileFrom(fname,'rb')
        z.writestr(z_name,data)
        print '%s :: %s = %s' % (_utils.funcName(),z_name,_fname)
    finally:
        z.close()
        _utils.safely_remove(fname)
    return _fname

def dropIntoNestedZips(_fname,levels=10):
    ioTimeAnalysis.ioBeginTime('ZIP')
    ff = dropIntoZip(_fname)
    for i in xrange(2,levels+1):
        ff = dropIntoZip(ff,level=i)
    ioTimeAnalysis.ioEndTime('ZIP')
    return ff

def main():
    ioTimeAnalysis.initIOTime(__name__)
    ioTimeAnalysis.initIOTime('ZIP')
    ioTimeAnalysis.initIOTime('ZIP_READ')
    ioTimeAnalysis.ioBeginTime(__name__)
    _cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    _fname = os.sep.join([_cwd,'test.zip'])
    print '_fname is "%s".' % (_fname)
    files = [f for f in os.listdir(_cwd) if (f.startswith('test')) and (f.find('.zip') > -1)]
    print 'files is "%s".' % (files)
    for f in files:
        _fqname = os.sep.join([_cwd,f])
        _utils.safely_remove(_fqname)
        print 'remove "%s".' % (_fqname)
    writeZip(_fname)
    readZip(_fname)
    ff = dropIntoNestedZips(_fname,25)
    ioTimeAnalysis.ioBeginTime('ZIP_READ')
    rreadZip(_cwd,ff,'test_9')
    ioTimeAnalysis.ioEndTime('ZIP_READ')
    ioTimeAnalysis.ioEndTime(__name__)
    print 'DONE.'
    ioTimeAnalysis.ioTimeAnalysisReport()

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(main)
    main()
