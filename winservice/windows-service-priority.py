import win32api,win32process,win32con

from vyperlogix.classes.SmartObject import SmartObject, SmartFuzzyObject

from vyperlogix.enum.Enum import Enum

from vyperlogix.misc import ObjectTypeName

class Win32ProcessPriorities(Enum):
    IDLE_PRIORITY_CLASS = win32process.IDLE_PRIORITY_CLASS
    BELOW_NORMAL_PRIORITY_CLASS = win32process.BELOW_NORMAL_PRIORITY_CLASS
    NORMAL_PRIORITY_CLASS = win32process.NORMAL_PRIORITY_CLASS
    ABOVE_NORMAL_PRIORITY_CLASS = win32process.ABOVE_NORMAL_PRIORITY_CLASS
    HIGH_PRIORITY_CLASS = win32process.HIGH_PRIORITY_CLASS
    HIGH_PRIORITY_CLASS = win32process.REALTIME_PRIORITY_CLASS

def setpriority(pid=None,priority=Win32ProcessPriorities.BELOW_NORMAL_PRIORITY_CLASS):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """
        
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    #handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    handle = win32api.OpenProcess(0x0410, False, pid)
    win32process.SetPriorityClass(handle, priority.value if (ObjectTypeName.typeClassName(priority).find('.enum.Enum.EnumInstance') > -1) else Win32ProcessPriorities.BELOW_NORMAL_PRIORITY_CLASS.value)
    
if (__name__ == '__main__'):
    from win32com.client import GetObject
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    process_list_by_id = SmartObject(dict([(p.Properties_("ProcessID").Value, p.Properties_("Name").Value) for p in processes]))
    process_list_by_name = SmartFuzzyObject(dict([(p.Properties_("Name").Value,p.Properties_("ProcessID").Value) for p in processes]))
    pid = process_list_by_name['tntdrive-svc.exe']
    setpriority(pid=pid,priority=Win32ProcessPriorities.HIGH_PRIORITY_CLASS)
    pass
