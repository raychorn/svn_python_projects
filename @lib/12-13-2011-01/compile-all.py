import re
import os,sys
import platform
import compileall

import zipfile

from vyperlogix.misc import _utils

_use_zipfile = True

if (0):
    __bucket_name__ = 'cdn-python'
    try:
        from boto.s3 import connection
        from boto.s3 import key
        from vyperlogix.boto import s3, get_aws_credentials
        soCredentials = get_aws_credentials()
        aConnection = connection.S3Connection(aws_access_key_id=soCredentials.AWSAccessKeyId, aws_secret_access_key=soCredentials.AWSSecretKey)
        __bucket__ = aConnection.get_bucket(__bucket_name__)
    except Exception, details:
        __bucket__ = None
        #print >> sys.stderr, _utils.formattedException(details=details)

__version_dots__ = '.'.join(['%d'%(n) for n in sys.version_info[0:2]])
__version_underscore__ = '_'.join(['%d'%(n) for n in sys.version_info[0:2]])

_name = os.path.basename(os.path.basename(sys.argv[0]))
print _name

def __collect_files_using__(top,pattern_or_list_of_patterns,rejecting_re,callback=None):
    _files = []
    pattern_or_list_of_patterns = pattern_or_list_of_patterns if (misc.isList(pattern_or_list_of_patterns)) else [pattern_or_list_of_patterns]
    for top,dirs,files in _utils.walk(os.path.abspath(top),rejecting_re=rejecting_re):
        #for fn in [os.path.join(top,f) for f in files if (any([p for p in pattern_or_list_of_patterns if f.endswith(p)]))]:
        for fn in [os.path.join(top,f) for f in files if (any([p for p in pattern_or_list_of_patterns if os.path.splitext(f)[-1] == p]))]:
            __is__ = True
            if (callable(callback)):
                try:
                    b = callback(fn)
                    if (isinstance(b,bool)):
                        __is__ = b
                except:
                    pass
            if (__is__):
                _files.append(fn)
    return _files

__ignoring__ = re.compile('/[.]svn')
collect_py_files_using = lambda top:__collect_files_using__(top,['.py'],__ignoring__)
collect_pyc_files_using = lambda top:__collect_files_using__(top,['.pyc'],__ignoring__)
collect_pyo_files_using = lambda top:__collect_files_using__(top,['.pyo'],__ignoring__)
collect_files_using = lambda top:__collect_files_using__(top,['.pyc','.pyd','.dll','.pyo'],__ignoring__)

collect_zip_files_using = lambda top,cb:__collect_files_using__(top,['.zip'],__ignoring__,callback=cb)

def write_to_S3_bucket(bucket,source,name):
    from vyperlogix.oodb import strToHex
    try:
        if (bucket):
            aKey = key.Key(bucket=bucket,name=name.replace(os.sep,'/'))
            contents = _utils.readBinaryFileFrom(source)
            data = strToHex(contents)
            aKey.set_contents_from_string(data)
            print '\tWriting to S3 bucket "%s" --> %s --> "%s" ...' % (bucket.name,f,f_new)
    except Exception, details:
        print >> sys.stderr, _utils.formattedException(details=details)

def main(libname='vyperlogix'):
    global _is_target_folder_valid
    __libname__ = libname
    print '__libname__ --> "%s" ...' % (__libname__)
    fp = os.path.abspath(__libname__) if (not os.path.exists(__libname__)) else __libname__
    print 'fp --> "%s" ...' % (fp)

    _has_library = False
    for f in sys.path:
        if (os.path.isdir(f)):
            files = os.listdir(f)
            if (__libname__ in files):
                _has_library = True
                break
        if (str(f).find(__libname__) > -1):
            _has_library = True
            break

    _bias = os.path.dirname(fp)
    print '_bias --> "%s" ...' % (_bias)

    if (not _has_library):
        sys.path.insert(0,_bias)

    _normalized_name = lambda name:('%s_%s'%(name.replace(__version_underscore__,''),__version_underscore__)).replace('__','_')
    normalized_name = lambda name:('%s_%s'%(name.replace(__version_dots__,''),__version_dots__)).replace('__','_')

    __cwd__ = os.path.abspath(os.curdir)

    _bias_name = fp.replace(os.sep, '/').split('/')[-1]
    print '_bias_name --> "%s" ...' % (_bias_name)

    _target_folder = os.sep.join([__cwd__,normalized_name('dist')])
    _utils._makeDirs(_target_folder)
    _is_target_folder_valid = (os.path.exists(_target_folder)) and (os.path.isdir(_target_folder))
    print '_is_target_folder_valid --> "%s" ...' % (_is_target_folder_valid)

    compileall.compile_dir(fp, rx=__ignoring__, force=True)

    if (_is_target_folder_valid):
        print 'Collecting .pyc files...',
        pyc_files = collect_pyc_files_using(fp)

        if (len(pyc_files) > 0):
            print 'Removing .pyc files...\n','\n'.join(pyc_files),
            for f in [n for n in pyc_files if (os.path.splitext(n)[-1] == '.pyc')]:
                dot_py = os.path.splitext(f)[0]+'.py'
                dot_pyo = os.path.splitext(f)[0]+'.pyo'
                if (os.path.exists(dot_py) and os.path.exists(dot_pyo)):
                    print 'Removing "%s".' % (f)
                    os.remove(f)
            print 'Done !'
        else:
            print 'There are NO .pyc files.'

        print 'Collecting .pyo files...',
        pyo_files = collect_pyo_files_using(fp)

        if (len(pyo_files) > 0):
            print 'Renaming .pyo --> .pyc ...\n','\n'.join(pyo_files),
            for f in pyo_files:
                f_new = '.'.join([os.path.splitext(f)[0],'pyc'])
                print 'Rrenaming "%s" --> "%s".' % (f,f_new)
                os.rename(f,f_new)
            print 'Done !'
        else:
            print 'There are NO .pyo files.'

    print 'Making dist folder...',

    _dist_folder = _target_folder
    print 'Done !'

    print 'Collecting .py files again...'
    py_files = collect_py_files_using(fp)

    print 'Collecting .pyc files again...'
    pyc_files = collect_files_using(fp)

    print 'INFO: _use_zipfile=%s' % (_use_zipfile)
    if (_use_zipfile == True):
        zf_name = '%s.zip' % (_normalized_name(_bias_name))
        zf_name = '%s%s%s' % (_dist_folder,os.sep,zf_name)
        print 'Moving .pyc --> "%s" ...' % (zf_name)
        zf = zipfile.PyZipFile(zf_name, mode='w')

        zf_name2 = '%s_source.zip' % (_normalized_name(_bias_name))
        zf_name2 = '%s%s%s' % (_dist_folder,os.sep,zf_name2)
        print 'Moving .py --> "%s" ...' % (zf_name2)
        zf2 = zipfile.PyZipFile(zf_name2, mode='w')
    else:
        print 'Moving .pyc --> "%s" ...' % (_dist_folder)

    __bias__ = _bias.replace('/',os.sep)
    __default_bias__ = '%s%s%s'%(os.sep,_bias_name,os.sep)
    for f in pyc_files:
        if (_use_zipfile == False):
            f_new = os.path.join(_dist_folder,os.path.basename(f))
            if (os.path.exists(f_new)):
                os.remove(f_new)
            if (f.find(_name) > -1):
                os.remove(f)
            else:
                try:
                    os.rename(f,f_new)
                except WindowsError, _details:
                    info_string = _utils.formattedException(details=_details)
                    print info_string
        else:
            try:
                if (len(__bias__) == 0):
                    f_new = f.replace('//','/').replace('/',os.sep)
                    toks = f_new.split(__default_bias__)
                    f_new = os.sep.join(['',__default_bias__.replace(os.sep,''),toks[-1]])
                else:
                    f_new = f.replace('//','/').replace('/',os.sep).replace(__bias__,'')
                print '\tAdding %s --> "%s" ...' % (f,f_new)
                zf.write(f,f_new)
            except:
                zf.close()
                break
    ##################################################################
    for f in py_files:
        if (_use_zipfile == True):
            try:
                if (len(__bias__) == 0):
                    f_new = f.replace('//','/').replace('/',os.sep)
                    toks = f_new.split(__default_bias__)
                    f_new = os.sep.join(['',__default_bias__.replace(os.sep,''),toks[-1]])
                else:
                    f_new = f.replace('//','/').replace('/',os.sep).replace(__bias__,'')
                print '\tAdding %s --> "%s" ...' % (f,f_new)
                zf2.write(f,f_new)
            except:
                zf2.close()
                break
    ##################################################################
    print '(+++) _use_zipfile=%s' % (_use_zipfile)
    if (_use_zipfile == True):
        zf.close()
        zf2.close()
        print 'BEGIN: .pyc files'
        for name in zf.namelist():
            print name
        print 'END!!! .pyc files'
        print '\n'
        print 'BEGIN: .py files'
        for name in zf2.namelist():
            print name
        print 'END!!! .py files'
        ftoks = list(os.path.splitext(zf_name))
        ftoks[0] = _normalized_name(ftoks[0])
        _zf_name = ''.join(ftoks)
        #os.rename(zf_name,_zf_name)
        
        __libs__ = {}
        def __callback__(fname):
            __is_build__ = (fname.find(os.sep+'build'+os.sep) > -1)
            __is__ = (fname.find(os.sep+'@lib'+os.sep) > -1) and (not __is_build__)
            bname = os.path.basename(fname)
            __exists__ = bname in __libs__.keys()
            if (not __is__):
                #print 'DEBUG: (@@@.2) fname=%s --> bname=%s [__is__=%s] [__is_build__=%s] [__exists__=%s]' % (fname,bname,__is__,__is_build__,__exists__)
                pass
            if (__is__):
                __libs__[bname] = fname
                #print 'DEBUG: (@@@.2a) __libs__=%s' % (__libs__)
            if ((not __is_build__) and __exists__):
                #print 'DEBUG: (@@@.2b) bname=%s [__is__=%s] [__is_build__=%s] [__exists__=%s]' % (bname,__is__,__is_build__,__exists__)
                pass
            return (not __is_build__) and __exists__
        cwd = os.path.abspath(os.curdir)
        print 'DEBUG: (@@@.3) cwd=%s' % (cwd)
        toks = cwd.split(os.sep)
        while (len(toks)>1):
            print 'DEBUG: (@@@.4) toks[-1]=%s' % (toks[-1])
            if (toks[-1] == '@lib'):
                toks.pop()
                break
            toks.pop()
        __cwd__ = os.sep.join(toks)
        print 'DEBUG: (@@@.1) %s --> %s' % (cwd,__cwd__)
        zips = collect_zip_files_using(__cwd__,__callback__)
        print '\n'
        print 'BEGIN: .zip files'
        for dest in zips:
            bname = os.path.basename(dest)
            src = __libs__.get(bname,None)
            if (src):
                src_stat = os.stat(src)
                dest_stat = os.stat(dest)
                src_stat_data = _utils.explain_stat(src_stat,asDict=True)
                dest_stat_data = _utils.explain_stat(dest_stat,asDict=True)
                __is__ = src_stat[_utils.stat.ST_CTIME] > dest_stat[_utils.stat.ST_CTIME]
                print 'DEBUG: Date check, %s > %s=%s' % (src_stat[_utils.stat.ST_CTIME],dest_stat[_utils.stat.ST_CTIME],__is__)
                if (__is__) or (src_stat[_utils.stat.ST_CTIME] != dest_stat[_utils.stat.ST_CTIME]):
                    print 'DEBUG: %s --> %s' % (src,dest)
                    print 'DEBUG: src_stat_data=%s' % (src_stat_data)
                    print 'DEBUG: dest_stat_data=%s' % (dest_stat_data)
                    print 'DEBUG: Performing copy %s --> %s.' % (src,dest)
                    _utils.copy_binary_files_by_chunks(src,dest)
                    print '\n'
                else:
                    print 'DEBUG: No need to copy, target is newer than source.'
        print 'END!!! .zip files'
        
        if (0):
            from vyperlogix.crypto import Encryptors
            from vyperlogix.ssh import sshUtils
            __dest__ = '/downloads.vyperlogix.com/web/content/vyperlogix'
            sshUtils.sftp_to_host('ftp.ord1-1.websitesettings.com', Encryptors._decode('F2E1F9E3E8EFF2EE'), Encryptors._decode('D0E5E5EBC0E2B0B0'), _zf_name, __dest__, isSilent=False)
        
    #_utils.removeAllFilesUnder(_target_folder) # don't do this, ever !!!
    print '(+++) Done !'

if (__name__ == '__main__'):
    from vyperlogix import misc
    try:
        from vyperlogix.misc import _psyco
        _psyco.importPsycoIfPossible(func=main)
    except Exception, ex:
        print >>sys.stderr, _utils.formattedException(details=ex)
    print 'BEGIN !'
    try:
        libname = sys.argv[1] if (len(sys.argv) > 1) else None
        print 'libname --> "%s" ...' % (libname)
        main(libname='vyperlogix' if (not misc.isStringValid(libname)) else libname)
    except Exception, ex:
        print >>sys.stderr, _utils.formattedException(details=ex)
    print 'END !'