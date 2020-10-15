import re
import os,sys
import compileall

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.misc.ReportTheList import reportTheList

StringIO = _utils.stringIO

def _commitTarget(cmds):
    from vyperlogix.process import Popen

    cmds = cmds if (misc.isList(cmds)) else [cmds]
    reportTheList(cmds,'Commands')
    buf = StringIO()
    shell = Popen.Shell(cmds,isExit=True,isWait=True,isVerbose=True,fOut=buf)
    print buf.getvalue()
    print '-'*40
    print

def commitTarget(target):
    cmd1 = 'svn add --quiet --force .'
    cmd2 = 'svn commit --non-interactive -m "Automated Commit on %s" .' % (_utils.timeStampLocalTime())
    cmds = ['cd "%s"' % (target)]
    cmds.append(cmd1)
    cmds.append(cmd2)
    _commitTarget(cmds)

_name = os.path.basename(os.path.basename(sys.argv[0]))

print _name

_rx=re.compile('[.]svn')

fp = os.path.abspath('.')
folders = [f for f in os.listdir(fp) if (os.path.isdir(f)) and (_rx.search(f) is None) and (f != 'dist')]
folders.append(fp)

compileall.compile_dir(fp, rx=re.compile('/[.]svn'), force=True)

x = '%sdist' % (os.sep)
d = {}
for root, dirs, files in _utils.walk(fp,rejecting_re=_rx):
    inRoot = (root == fp)
    inLogs = (root.endswith('%slogs' % (os.sep)))
    if (root.find(x) == -1) and (not inLogs):
        if (inRoot):
            files = [f for f in files if (not f.startswith('compile-all.'))]
        d_ext = lists.HashedLists()
        for f in files:
            toks = os.path.splitext(f)
            d_ext[toks[-1]] = os.path.join(root,f)
        try:
            pyo_files = [os.path.join(root,f) for f in d_ext['.pyo']]
        except:
            pyo_files = []
        for f in pyo_files:
            f_new = '.'.join([os.path.splitext(f)[0],'pyc'])
            if (os.path.exists(f_new)):
                os.remove(f_new)
                f_base = os.path.basename(f)
                d_ext['.pyo'] = [x for x in d_ext['.pyo'] if (x != f_base)]
            os.rename(f,f_new)
            d_ext['.pyc'] = f_new
        if (inRoot):
            d_ext['.pyc'] = [f for f in d_ext['.pyc'] if (f.find('compile-all.') == -1)]
            for k,v in d_ext.iteritems():
                if (k not in ['.pyc','.py']):
                    del d_ext[k]
        not_pyc = []
        for k,v in d_ext.iteritems():
            if (k.find('.py') == -1):
                not_pyc = not_pyc + d_ext[k]
        d[root] = (d_ext['.pyc'] if (d_ext['.pyc'] is not None) else [],not_pyc)

print 'Making dist folder...',

_dist_folder = os.path.join(os.path.join(fp,'dist'),'%s_dist' % (fp.split(os.sep)[-1]))
_utils._makeDirs(_dist_folder)
print 'Done !'

_utils.removeAllFilesUnder(os.path.dirname(_dist_folder))
_utils._makeDirs(_dist_folder)

for fname,tup in d.iteritems():
    for t in tup:
        for f in t:
            _fname = os.sep.join(fname.replace(fp,'').split(os.sep)[1:])
            f_new = os.path.join(_dist_folder,_fname)
            _utils.makeDirs(f_new)
            try:
                _f = os.path.join(f_new,f.replace(os.path.join(fp,fname)+os.sep,''))
                _utils.makeDirs(_f)
                if (os.path.splitext(f)[-1] == '.pyc'):
                    print '(Dist) Removing "%s".' % (f)
                    os.rename(f,_f)
                else:
                    _utils.copyFile(f,_f)
            except Exception, _details:
                info_string = _utils.formattedException(details=_details)
                print '%s %s,%s' % (info_string,f,_f)

_deploy_folder = os.path.dirname(os.path.dirname(os.path.dirname(_dist_folder)))
_project_folder = os.path.join(_deploy_folder,os.sep.join(['django']))
_deploy_name = _deploy_folder.split(os.sep)[-1]
_deploy_folder = os.path.join(_deploy_folder,os.sep.join(['deployments','%s_deployment' % (_deploy_name)]))

for root, dirs, files in _utils.walk(_dist_folder,rejecting_re=_rx):
    for f in files:
        f1 = os.path.join(root,f)
        _f = os.sep.join(f1.replace(_dist_folder,'').split(os.sep)[1:])
        f2 = os.path.join(_deploy_folder,_f)
        isCopied = False
        try:
            _utils.copyFile(f1,f2)
            isCopied = True
        except:
            pass
        if (isCopied):
            print '(Deploy) Removing "%s".' % (f1)
            os.remove(f1)

_root_ = os.path.dirname(_dist_folder)
num_files = 0
for root, dirs, files in _utils.walk(_dist_folder,rejecting_re=_rx):
    num_files += len(files)
if (num_files == 0):
    _utils.removeAllFilesUnder(_root_)

commitTarget(_project_folder)
commitTarget(_deploy_folder)

print 'Done !'
