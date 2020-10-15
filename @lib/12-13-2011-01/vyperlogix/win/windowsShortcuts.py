import os, sys
import pythoncom
from win32com.shell import shell, shellcon

from vyperlogix import misc

def getDesktopPath():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0)

def getDocumentsPath():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, 0, 0)

def getPathFromShortcut(lnkPath):
    try:
        shortcut = pythoncom.CoCreateInstance (
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
        persist_file.Load(lnkPath)

        return shortcut.GetPath(shell.SLGP_UNCPRIORITY)

    except Exception, details:
        print >>sys.stderr, '(getPathFromShortcut).1 :: ERROR due to "%s".' % str(details)

def __makeWindowsShortcut(shortcut,targetPath,workingPath,description,iconLocation):
    if (misc.isString(targetPath)):
        if (os.path.exists(targetPath)):
            shortcut.SetPath(targetPath)
    if (misc.isString(description)):
        if (len(description) > 0):
            shortcut.SetDescription(description)
    if (misc.isString(iconLocation)):
        if (os.path.exists(iconLocation)):
            shortcut.SetIconLocation(iconLocation, 0)
    if (misc.isString(workingPath)):
        if (os.path.exists(workingPath)):
            shortcut.SetWorkingDirectory(workingPath)

def makeWindowsShortcut(lnkPath,targetPath,workingPath,description,iconLocation):
    try:
        if (os.path.exists(targetPath)):
            shortcut = pythoncom.CoCreateInstance (
                shell.CLSID_ShellLink,
                None,
                pythoncom.CLSCTX_INPROC_SERVER,
                shell.IID_IShellLink
            )
            __makeWindowsShortcut(shortcut,targetPath,workingPath,description,iconLocation)

            persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
            persist_file.Save(lnkPath, 0)
        else:
            print >>sys.stderr, '(makeWindowsShortcut).2 :: ERROR - Cannot make a shortcut to a non-extant path which is "%s".' % targetPath
    except Exception, details:
        print >>sys.stderr, '(makeWindowsShortcut).1 :: ERROR due to "%s".' % str(details)

def updateWindowsShotcut(lnkPath,targetPath,workingPath,description,iconLocation):
    try:
        shortcut = pythoncom.CoCreateInstance (
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
        persist_file.Load(lnkPath)

        __makeWindowsShortcut(shortcut,targetPath,workingPath,description,iconLocation)

        persist_file.Save(lnkPath, 0)
    except Exception, details:
        print >>sys.stderr, '(updateWindowsShotcut).1 :: ERROR due to "%s".' % str(details)

def updateWindowsShortcut(lnkPath,targetPath,workingPath,description,iconLocation):
    return updateWindowsShotcut(lnkPath, targetPath, workingPath, description, iconLocation)
