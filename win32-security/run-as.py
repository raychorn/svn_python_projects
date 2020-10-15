import win32security
import win32process
import win32api
import win32con
import sys
import time
import os
from ntsecuritycon import *

def AdjustPrivilege(priv, enable = 1):
    # Get the process token.
    flags = TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),flags)
    # Get the ID for the privilege.
    id = win32security.LookupPrivilegeValue(None, priv)
    # Now obtain the privilege for this process.
    # Create a list of the privileges to be added.
    if enable:
        newPrivileges = [(id, SE_PRIVILEGE_ENABLED)]
    else:
        newPrivileges = [(id, 0)]
    win32security.AdjustTokenPrivileges(handle, 0, newPrivileges)
    # and make the adjustment.

handle=win32security.LogonUser('administrator','domain','sisko@7660$boo',win32con.LOGON32_LOGON_INTERACTIVE,win32con.LOGON32_PROVIDER_DEFAULT)

win32security.ImpersonateLoggedOnUser(handle)
AdjustPrivilege(SE_TCB_NAME)
AdjustPrivilege(SE_INCREASE_QUOTA_NAME)
AdjustPrivilege(SE_ASSIGNPRIMARYTOKEN_NAME)
#AdjustPrivilege(TOKEN_DUPLICATE)
#AdjustPrivilege(TOKEN_IMPERSONATE)
AdjustPrivilege(SE_CHANGE_NOTIFY_NAME) 

print "Started as: ", win32api.GetUserName()
#this prints target username, impersonation successful 

win32process.CreateProcessAsUser(handle,None,'notepad',None,None,0,0,None,None,win32process.STARTUPINFO())

win32security.RevertToSelf()
handle.Close()
