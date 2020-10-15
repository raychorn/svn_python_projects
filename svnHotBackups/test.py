import os, sys

from vyperlogix.misc import _utils

from vyperlogix.win import diskSpace

if (__name__ == '__main__'):
    #rw_mode = _mask = 0777 if (sys.platform != 'win32') else _utils.windows_mask
    #backup_subdir = 'c:\\docume~1\\rhorn\\locals~1\\temp\\www.vyperlogix.com\\svnHotBackups\\svn-4928\\svn-4928.zip'
    #os.chmod(backup_subdir,rw_mode)
    #_f = backup_subdir
    #print '1). stat of %s\n\t%s' % (_f,_utils.explain_stat(os.stat(_f),delim='\n\t'))
    #_utils.chmod_tree(backup_subdir, rw_mode, _mask) # counteract previous safe_rmtree() actions.
    #print '2). stat of %s\n\t%s' % (_f,_utils.explain_stat(os.stat(_f),delim='\n\t'))

    drive = r'J:'
    print 'TotalSize of %s = %d' % (drive, diskSpace.TotalSize(drive))
    print 'FreeSapce on %s = %d' % (drive, diskSpace.FreeSpace(drive))

    import os

    # pick a folder you have ...
    folder = 'J:\#ubuntu.dyn-o-saur.com'
    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)

    print "Folder = %0.1f MB" % (folder_size/(1024*1024.0))
    