# ZIP test
import os, sys
import zipfile
import zlib

sys.path += ['Z:\python projects\@lib']

from vyperlogix.oodb import *

test_string = lambda x:''.join([chr(ch) for ch in xrange(128,128+min(x,127))])

hide_string = lambda x:''.join([chr(ord(ch)+128) for ch in x])

def writeZip(_fname):
    z = zipfile.ZipFile(_fname,'w')
    try:
        s = test_string(127)

        data = zlib.compress(s,zlib.Z_BEST_COMPRESSION)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_BEST_COMPRESSION)
        hh_data = hide_string(h_data)

        z.writestr('test_%s' % (zlib.Z_BEST_COMPRESSION),data)
        z.writestr('test_h_%s' % (zlib.Z_BEST_COMPRESSION),h_data)
        z.writestr('test_z_%s' % (zlib.Z_BEST_COMPRESSION),z_data)
        z.writestr('test_hh_%s' % (zlib.Z_BEST_COMPRESSION),hh_data)

        data = zlib.compress(s,zlib.Z_BEST_SPEED)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_BEST_SPEED)
        hh_data = hide_string(h_data)

        z.writestr('test_%s' % (zlib.Z_BEST_SPEED),data)
        z.writestr('test_h_%s' % (zlib.Z_BEST_SPEED),h_data)
        z.writestr('test_z_%s' % (zlib.Z_BEST_SPEED),z_data)
        z.writestr('test_hh_%s' % (zlib.Z_BEST_SPEED),hh_data)

        data = zlib.compress(s,zlib.Z_DEFAULT_COMPRESSION)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_DEFAULT_COMPRESSION)
        hh_data = hide_string(h_data)

        z.writestr('test_%s' % (zlib.Z_DEFAULT_COMPRESSION),data)
        z.writestr('test_h_%s' % (zlib.Z_DEFAULT_COMPRESSION),h_data)
        z.writestr('test_z_%s' % (zlib.Z_DEFAULT_COMPRESSION),z_data)
        z.writestr('test_hh_%s' % (zlib.Z_DEFAULT_COMPRESSION),hh_data)
    finally:
        z.close()

def readZip(_fname):
    z = zipfile.ZipFile(_fname,'r')
    try:
        for zm in [zlib.Z_BEST_COMPRESSION,zlib.Z_BEST_SPEED,zlib.Z_DEFAULT_COMPRESSION]:
            for zs in ['test_%s','test_h_%s','test_z_%s','test_hh_%s']:
                z_str = z.read(zs % (zm))
                if (zs.find('_h_') > -1):
                    pass
                elif (zs.find('_z_') > -1):
                    pass
                elif (zs.find('_hh_') > -1):
                    pass

        data = zlib.compress(s,zlib.Z_BEST_COMPRESSION)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_BEST_COMPRESSION)
        hh_data = hide_string(h_data)

        z.writestr('test_%s' % (zlib.Z_BEST_COMPRESSION),data)
        z.writestr('test_h_%s' % (zlib.Z_BEST_COMPRESSION),h_data)
        z.writestr('test_z_%s' % (zlib.Z_BEST_COMPRESSION),z_data)
        z.writestr('test_hh_%s' % (zlib.Z_BEST_COMPRESSION),hh_data)

        data = zlib.compress(s,zlib.Z_BEST_SPEED)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_BEST_SPEED)
        hh_data = hide_string(h_data)

        z.writestr('test_%s' % (zlib.Z_BEST_SPEED),data)
        z.writestr('test_h_%s' % (zlib.Z_BEST_SPEED),h_data)
        z.writestr('test_z_%s' % (zlib.Z_BEST_SPEED),z_data)
        z.writestr('test_hh_%s' % (zlib.Z_BEST_SPEED),hh_data)

        data = zlib.compress(s,zlib.Z_DEFAULT_COMPRESSION)
        h_data = strToHex(data)
        z_data = zlib.compress(h_data,zlib.Z_DEFAULT_COMPRESSION)
        hh_data = hide_string(h_data)

        z.writestr('test_%s' % (zlib.Z_DEFAULT_COMPRESSION),data)
        z.writestr('test_h_%s' % (zlib.Z_DEFAULT_COMPRESSION),h_data)
        z.writestr('test_z_%s' % (zlib.Z_DEFAULT_COMPRESSION),z_data)
        z.writestr('test_hh_%s' % (zlib.Z_DEFAULT_COMPRESSION),hh_data)
    finally:
        z.close()

if (__name__ == '__main__'):
    _cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    _fname = os.sep.join([_cwd,'test.zip'])
    print '_fname is "%s".' % (_fname)
    if (os.path.exists(_fname)):
        os.remove(_fname)
    #writeZip(_fname)
    readZip(_fname)
    print 'DONE.'
