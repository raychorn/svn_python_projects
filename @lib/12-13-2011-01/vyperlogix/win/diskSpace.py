__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
from vyperlogix.misc import _utils
if (_utils.isUsingWindows):
    import win32com.client as com
else:
    import os
    import statvfs
    
    def free_bytes(path):
        stats = os.statvfs(path)
        return stats[statvfs.F_BSIZE] * stats[statvfs.F_BFREE]
    
    def avail_bytes(path):
        stats = os.statvfs(path)
        return stats[statvfs.F_BSIZE] * stats[statvfs.F_BAVAIL]
    
__one_gb__ = 2**30

def TotalSize(drive):
    """ Return the TotalSize of a shared drive [GB] via any valid UNC or Drive Letter (C:)
    drive = r'\\servername\c$'
    drive = r'J:'
    print 'TotalSize of %s = %d' % (drive, TotalSize(drive))
    print 'FreeSapce on %s = %d' % (drive, FreeSpace(drive))
    """
    if (_utils.isUsingWindows):
        try:
            fso = com.Dispatch("Scripting.FileSystemObject")
            drv = fso.GetDrive(drive)
            return drv.TotalSize/__one_gb__
        except:
            return 0
    else:
        try:
            return (free_bytes('.')+avail_bytes('.'))/__one_gb__
        except:
            pass
    return 0

def FreeSpace(drive):
    """ Return the FreeSape of a shared drive [GB] via any valid UNC or Drive Letter (C:)
    drive = r'\\servername\c$'
    drive = r'J:'
    print 'TotalSize of %s = %d' % (drive, TotalSize(drive))
    print 'FreeSapce on %s = %d' % (drive, FreeSpace(drive))
    """
    if (_utils.isUsingWindows):
        try:
            fso = com.Dispatch("Scripting.FileSystemObject")
            drv = fso.GetDrive(drive)
            return drv.FreeSpace/__one_gb__
        except:
            return 0
    else:
        try:
            return free_bytes('.')/__one_gb__
        except:
            pass
    return 0
    
