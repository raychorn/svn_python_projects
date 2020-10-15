import os, sys

import common

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.enum.Enum import Enum

__bin_debug__ = 'bin-debug'

__fpath_for_xml_file = None
__fpath_for_cert_file = None
__fpath_for_bin_adt = None

__apk_builder_template = lambda adt,cert,name:'call "%s" -package -target apk -storetype pkcs12 -keystore "%s" %s.apk %s-app.xml %s.swf' % (adt,cert,name,name,name)

__cert_builder_template = lambda adt,target,commonName,password:'call "%s" -certificate -cn %s 1024-RSA "%sSigningCert_AIR2.5.p12" %s' % (adt,commonName,target,password)

class FolderLocation(Enum):
    desktop = 1
    mydocuments = 2

def _pickler(item):
    import pickle
    from cStringIO import StringIO

    src = StringIO()
    p = pickle.Pickler(src)
    p.dump(item)
    return src.getvalue()

def _unpickler(stuff):
    import pickle
    from cStringIO import StringIO

    dst = StringIO(stuff)
    up = pickle.Unpickler(dst)
    return up.load()

target_file = lambda foo:os.sep.join([os.path.dirname(foo),'%s.dat'%(os.path.splitext(os.path.basename(foo))[0])])

def save_fpaths_for_later(pidl_project,pidl_cert,pidl_adt,pwd):
    target = target_file(__file__)
    fOut = open(target,mode='w')
    try:
        print >> fOut, _pickler(tuple([pidl_project,pidl_cert,pidl_adt,pwd]))
    except:
        pass
    finally:
        fOut.flush()
        fOut.close()

def get_fpaths_from_earlier():
    blob = (None,None,None)
    target = target_file(__file__)
    if (os.path.exists(target)):
        fIn = open(target,mode='r')
        try:
            blob = _unpickler(fIn.read())
        except:
            pass
        finally:
            fIn.close()
    return blob

def get_shellicon(top):
    from win32com.shell import shellcon
    _get_shellicon = lambda top:shellcon.CSIDL_DESKTOP if (top == FolderLocation.desktop) else shellcon.CSIDL_PERSONAL
    return _get_shellicon(top)

def browse_for_target_folder(pidl,title,top=FolderLocation.desktop):
    import win32gui
    from win32com.shell import shell, shellcon

    pidl, display_name, image_list = shell.SHBrowseForFolder (
        win32gui.GetDesktopWindow (),
        shell.SHGetFolderLocation (0, get_shellicon(top), 0, 0) if ( (pidl == None) or (os.path.exists(shell.SHGetPathFromIDList(pidl)) == False) ) else pidl,
        title if (title) else "Select a folder",
        0,
        None,
        None
    )
    if (pidl != None) and (display_name != None) and (image_list != None):
        pass
    else:
        print 'WARNING: You failed to choose a folder... Cannot continue.'
    return pidl

def browse_for_target_file(pidl,title,target=None,top=FolderLocation.desktop):
    import os
    import win32gui
    from win32com.shell import shell, shellcon

    i = 1
    x = 0
    n = 0
    if (title.find('%s') > -1) and (target):
        title = title % (target)
    while (1):
        pidl, display_name, image_list = shell.SHBrowseForFolder (
            win32gui.GetDesktopWindow(),
            shell.SHGetFolderLocation(0, get_shellicon(top), 0, 0) if ( (pidl == None) or (os.path.exists(shell.SHGetPathFromIDList(pidl)) == False) ) else pidl,
            title if (title) else "Select a file or folder",
            shellcon.BIF_BROWSEINCLUDEFILES,
            None,
            None
        )
    
        if (pidl, display_name, image_list) == (None, None, None):
            x += 1
            if (n == 0) or (x > 1):
                print 'WARNING: You failed to choose a file or folder...'
                break
        else:
            path = shell.SHGetPathFromIDList(pidl)
            if (os.path.isfile(path)):
                if (target == None) or ((target) and (path.find('%s%s' % (os.sep,os.path.basename(path))) > -1)):
                    break
                else:
                    n += 1
                    title = title.lower().replace('do not','do not').replace('wrong','WRONG')
                    pidl = None
            else:
                i += 1
                n += 1
                if (i > 1):
                    title = title.lower().replace('do not','do NOT').replace('wrong','wrong')
                else:
                    title = title.lower().replace('do NOT','DO NOT').replace('wrong','wrong')
                if (i > 5):
                    break
                title = title.replace('Cancel','Cancel again')
                pidl = None
    return pidl

def make_cert_in(adt,fpath,cn,pwd):
    from vyperlogix import misc
    fOut = _utils.stringIO()
    cn = _utils.alpha_numeric_only(''.join([str(c).capitalize() for c in cn.split()]))
    normalize = lambda target:os.sep.join(misc.append([f for f in target.split(os.sep) if (len(f) > 0)],''))
    _cmd = __cert_builder_template(adt,normalize(fpath),cn,pwd)
    print _cmd
    Popen.Shell(_cmd, shell=None, env=None, isExit=True, isWait=True, isVerbose=True, fOut=fOut)
    print >> sys.stderr, fOut.getvalue()

def main():
    __programName = os.path.splitext(_argsObj.programName)[0]
    
    print 'STARTING: %s v%s' % (__programName,common.__version__)
    pidl_project,pidl_cert,pidl_adt,password = [None,None,None,None]
    try:
        pidl_project,pidl_cert,pidl_adt,password = get_fpaths_from_earlier()
    except:
        try:
            pidl_project,pidl_cert,pidl_adt = get_fpaths_from_earlier()
            password = None
        except:
            pass
    pidl_adt = browse_for_target_file(pidl_adt,"Choose your %s file, do not choose the folder or the wrong file.",target='adt.bat')
    if (pidl_adt != None):
        __fpath_for_bin_adt = shell.SHGetPathFromIDList(pidl_adt)
        print '--> ',__fpath_for_bin_adt
    pidl_cert = browse_for_target_file(pidl_cert,"Choose the folder that contains your cert file (Cancel to make a cert).")
    if (pidl_cert != None):
        __fpath_for_cert_file = shell.SHGetPathFromIDList(pidl_cert)
        print '--> ',__fpath_for_cert_file
    else:
        pidl_cert_folder = browse_for_target_folder(None,"Choose the folder that will contain your cert file.")
        if (pidl_cert_folder != None):
            __fpath_for_cert_folder = shell.SHGetPathFromIDList(pidl_cert_folder)
            print '--> ',__fpath_for_cert_folder
            cn = raw_input("What is the Common Name for your cert ? (Company Name or the like...) ")
            password = getpass.getpass()
            if (cn) and (len(cn) > 1) and (password) and (len(password) > 1):
                make_cert_in(__fpath_for_bin_adt,__fpath_for_cert_folder,cn,password)
            else:
                print 'WARNING: Cannot continue to create your cert file without the required information, please start again.'
                sys.exit(1)
        else:
            print 'WARNING: Cannot continue without a cert file, please start again.'
            sys.exit(1)
    pidl_project = browse_for_target_folder(pidl_project,"Choose the folder that contains your .xml file.")
    if (pidl_project != None):
        __fpath_for_xml_file = shell.SHGetPathFromIDList(pidl_project)
        print '--> ',__fpath_for_xml_file
    if (password == None):
        password = getpass.getpass()
    save_fpaths_for_later(pidl_project,pidl_cert,pidl_adt,password)
    if (__fpath_for_xml_file):
        if (os.path.isdir(__fpath_for_xml_file)):
            bin_debug_fname = os.sep.join([__fpath_for_xml_file,__bin_debug__]) if (__fpath_for_xml_file.split(os.sep).__contains__(__bin_debug__) == False) else __fpath_for_xml_file
            if (os.path.exists(bin_debug_fname)) and (os.path.isdir(bin_debug_fname)):
                app_name = os.path.dirname(bin_debug_fname).split(os.sep)[-1]
                swf_name = '%s.swf' % (app_name)
                swf_fname = os.sep.join([bin_debug_fname,swf_name])
                xml_name = '%s-app.xml' % (app_name)
                xml_fname = os.sep.join([bin_debug_fname,xml_name])
                if (os.path.exists(swf_fname)):
                    if (os.path.exists(xml_fname)):
                        _cwd = os.getcwd()
                        print 'cwd (1) -->', _cwd
                        os.chdir(bin_debug_fname)
                        fOut = _utils.stringIO()
                        _cmd = __apk_builder_template(__fpath_for_bin_adt,__fpath_for_cert_file,app_name)
                        print _cmd
                        p = Popen.Shell(_cmd, shell=None, env=None, isExit=False, isWait=False, isVerbose=True, fOut=fOut)
                        p.doSendWithTail(password)
                        p.doExit()
                        print >> sys.stderr, fOut.getvalue()
                        os.chdir(_cwd)
                        print 'cwd (2) -->', os.getcwd()
                    else:
                        print 'WARNING: Cannot proceed without the file named "%s".' % (xml_fname)
                else:
                    print 'WARNING: Cannot proceed without the file named "%s".' % (swf_fname)
            else:
                print 'WARNING: You must compile your Flex Builder 4 Project before you can make your .APK file.'
        else:
            print 'WARNING: You must choose a folder, rather than a file...'
    print 'ENDING!   %s v%s' % (__programName,common.__version__)

if (__name__ == '__main__'):
    import getpass
    
    from vyperlogix.process import Popen
    from win32com.shell import shell

    from vyperlogix.misc import Args
    
    args = {'--help':'show some help.',
            '--copyright':'show copyright.',
	    }
    _argsObj = Args.Args(args)

    print >>sys.stderr, common.__copyright__
    
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except:
	pass
    
    if (_isHelp):
	print >>sys.stderr, common.__copyright
	sys.exit()
	    
    main()