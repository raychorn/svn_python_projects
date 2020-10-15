from distutils.core import setup
import glob
import py2exe

packages_list = ['Z:\\python projects\\@lib\\lib']

import os, sys
wx_dir = [p for p in sys.path if (p.find('wx') > -1)]
wx_pdir = os.path.dirname(wx_dir[0])
pith = os.sep.join([wx_pdir,'wx.pth'])
if (os.path.exists(pith)):
    fIn = open(pith,'r')
    c_pith = [s.strip() for s in fIn.readlines()]
    fIn.close()
    fpith = os.sep.join([wx_pdir,c_pith[0]])
    print '\n'.join(wx_dir)
    print 'wx_pdir=%s' % (wx_pdir)
    print 'pith=%s' % (pith)
    print 'c_pith=%s' % (c_pith[0])
    print 'fpith=%s' % (fpith)
    #packages_list.append(fpith.replace('.','\.'))

if (1):
    print 'Packages: %s' % ('\n'.join(packages_list))
    setup(windows=['PDFexporter.py'],
    packages=packages_list,
    #data_files=[('bitmaps', glob.glob('bitmaps/*.*')),('data', glob.glob('data/*.*')),('bmp_source', glob.glob('bmp_source/*.*')),('', glob.glob('*.py'))],
    )