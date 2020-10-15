import re
import os,sys
import compileall

from vyperlogix.misc import _utils

_name = os.path.basename(os.path.basename(sys.argv[0]))

print _name

fp = os.path.abspath('.')
compileall.compile_dir(fp, rx=re.compile('/[.]svn'), force=True)

if (1):
    print 'Collecting .pyc files...',
    pyc_files = [os.path.join(fp,f) for f in os.listdir(fp) if (f.endswith('.pyc'))]
    
    if (len(pyc_files) > 0):
        print 'Removing .pyc files...\n(+++)','\n'.join(pyc_files),
        for f in pyc_files:
            os.remove(f)
        print 'Done !'
    else:
        print 'There are NO .pyc files.'
    
    print 'Collecting .pyo files...',
    pyo_files = [os.path.join(fp,f) for f in os.listdir(fp) if (f.endswith('.pyo'))]
    
    if (len(pyo_files) > 0):
        print 'Renaming .pyo --> .pyc ...\n(+++)','\n'.join(pyo_files),
        for f in pyo_files:
            f_new = '.'.join([os.path.splitext(f)[0],'pyc'])
            os.rename(f,f_new)
        print 'Done !'
    else:
        print 'There are NO .pyo files.'

print 'Making dist folder...',

_dist_folder = os.path.join(os.path.join(fp,'dist'),'%s_dist' % (fp.split(os.sep)[-1]))
_utils._makeDirs(_dist_folder)
print 'Done !'

print 'Collecting .pyc files again...',
pyc_files = [os.path.join(fp,f) for f in os.listdir(fp) if (f.endswith('.pyc'))]

print 'Moving .pyc --> "%s" ...' % (_dist_folder)
for f in pyc_files:
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
print 'Done !'

print 'Done !'
