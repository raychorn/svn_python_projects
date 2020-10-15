import win32com.client as com


def TotalSize(drive):
    """ Return the TotalSize of a shared drive [GB]"""
    try:
        fso = com.Dispatch("Scripting.FileSystemObject")
        drv = fso.GetDrive(drive)
        return drv.TotalSize/2**30
    except:
        return 0

def FreeSpace(drive):
    """ Return the FreeSape of a shared drive [GB]"""
    try:
        fso = com.Dispatch("Scripting.FileSystemObject")
        drv = fso.GetDrive(drive)
        return drv.FreeSpace/2**30
    except:
        return 0

drive = r'\\servername\c$'
print 'TotalSize of %s = %d' % (drive, TotalSize(drive))
print 'FreeSapce on %s = %d' % (drive, FreeSapce(drive))
