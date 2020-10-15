#!/usr/bin/env python
import zipfile
import os
import re
from distutils import util

ignore = list(set(['makeZip.cmd','makeZip.py','makeZip.pyc','makeZip.pyo','pythonProcess.pyc','pythonProcess.pyo','ruby-python-daemon.wpr','_compile.py','_compile.pyc','_compile.pyo','makeZip.py','makeZip.pyc','makeZip.pyo','project.properties','project.xml','private.properties','spawn-process.rb','exec.rb','hello.py','salesForce.py','myeval.py','myeval.pyo','myeval.pyc','makezip.txt','run2.cmd','test.py','test.pyc','test.pyo','proxy.py','proxy.pyc','proxy.pyo','runProxy.cmd','mapi_delete.py','mapi_delete.pyc','mapi_delete.pyo','To-Do.txt','test.txt','runmapi.cmd']))

edit_files = list(set(['run.cmd']))

if (0):
    try:
        execdict = { }
        execfile( '_compile.py', globals(), execdict)
    except Exception, details:
        print 'Error running compilation. (%s)' % (str(details))

rx = re.compile('[.]svn')
rxZip = re.compile('[.]zip')

bridge_token = '%sbridge' % os.sep
nbproject_token = "%snbproject" % os.sep

zipName = 'Ruby-Python-Bridge_0_1_1.zip'

_files = [f for f in os.listdir('.') if f.startswith('Ruby-Python-Bridge_') and f.endswith('.zip')]

print '_files=[%s]' % _files
if (len(_files) > 0):
    fname = _files[0]

    try:
        if os.path.exists(fname):
            print 'Removing "%s".' % fname
            os.remove(fname)
    except Exception, details:
        print 'WARNING in removing the old ZIP due to (%s)' % (str(details))

    toks = fname.split('.')[0].split('_')
    if (len(toks) ==4):
        n = int(toks[-1]) + 1
        toks[-1] = '%s' % n
        zipName = ('_'.join(toks))+'.zip'
    else:
        print 'Not sure how to determine the next number in the ZIP file sequence.'

ignore.append(zipName)

def editFile(zip,fname,base):
    import tempfile
    if (base.endswith('run.cmd')):
        tmp = tempfile.NamedTemporaryFile('w+')
        tmp_name = tmp.name
        tmp.close()
        fOut = open(tmp_name,'w+')
        fIn = open(fname,'r')
        lines = [l.strip() for l in fIn.readlines() if len(l.strip()) > 0]
        for l in lines:
            _l = l
            if (_l.find('PYTHONPATH=') > -1):
                toks = l.strip().split('=')
                _toks = [toks[-1].split(';')[0]]
                _toks.append('bridge.zip')
                toks[-1] = ';'.join(_toks)
                _l = '='.join(toks)
            fOut.write('%s\n' % _l)
        fIn.close()
        os.rename(fname,fname+'_')
        fOut.flush()
        fOut.close()
        os.rename(tmp_name,fname)
        zip.write(fname,base)
        os.remove(fname)
        os.rename(fname+'_',fname)
    pass

try:
    zip = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED)
    _zName = os.sep.join([os.path.abspath('.'),'bridge'])+'.zip'
    zipBridge = zipfile.ZipFile( _zName, 'w', zipfile.ZIP_DEFLATED)
    top = os.path.abspath('.')
    for root, dirs, files in os.walk(top):
        if (rx.search(root) == None) and (root.find(nbproject_token) == -1):
            d = {}
            _files = [os.sep.join([root,f]) for f in files]
            for f in _files:
                d[os.path.basename(f)] = f
            for f in ignore:
                try:
                    if (d.has_key(f)):
                        del d[f]
                except Exception, details:
                    print 'WARNING in ignoring files due to (%s)' % (str(details))
            _files = d.values()
            py_files = [f for f in _files if f.endswith('.py')]
            if (root != top):
                print 'Compiling (%s) %s' % (root,py_files)
                util.byte_compile(py_files,optimize=2,force=1)
            if (root.find(bridge_token) == -1):
                for f in _files:
                    if (rxZip.search(f) == None):
                        print 'ZIP Adding (%s) to (%s)' % (f,zipName)
                        f_base = f.replace('.pyo','.pyc').replace(top,'')
                        _f_base = f_base.split(os.sep)[-1]
                        if (_f_base in edit_files):
                            if (f_base.startswith(os.sep)):
                                f_base = f_base[1:]
                            editFile(zip,f,f_base)
                        else:
                            zip.write(f,f_base)
            elif (root.find(bridge_token) > -1):
                py_files = [f for f in _files if f.endswith('.pyo')]
                if (len(py_files) == 0):
                    py_files = [f for f in _files if f.endswith('.pyc')]
                for f in py_files:
                    f_base = f.replace('.pyo','.pyc').replace(root,'')
                    zipBridge.write(f,f_base)
    _top = 'Z:\@myMagma\python-local-new-trunk'
    top = os.path.abspath(os.sep.join([_top,'pyax']))
    for root, dirs, files in os.walk(top):
        if (rx.search(root) == None):
            py_files = [os.sep.join([root,f]) for f in [f for f in files if f.endswith('.py')]]
            print 'Compiling (%s) %s' % (root,py_files)
            util.byte_compile(py_files,optimize=2,force=1)
            _files = os.listdir(root)
            py_files = [f for f in _files if f.endswith('.pyo')]
            if (len(py_files) == 0):
                py_files = [f for f in _files if f.endswith('.pyc')]
            py_files = [os.sep.join([root,f]) for f in py_files]
            for f in py_files:
                _root = os.sep.join(root.split(os.sep)[0:-1])
                f_base = f.replace('.pyo','.pyc').replace(_top,'')
                zipBridge.write(f,f_base)
            pass
    zipBridge.close()
    zip.write(_zName,os.path.basename(_zName))
    os.remove(_zName)
except Exception, details:
    print 'Error in ZIP processing. (%s)' % (str(details))
finally:
    try:
        zip.close()
    except Exception, details:
        pass