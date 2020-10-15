import win32api
import win32com.client 
strComputer = "."
__allowed__ = ['IPC$']
serverName = None
if serverName is None:
    serverName = "\\\\" + win32api.GetComputerName()
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
colItems = objSWbemServices.ExecQuery("Select * from Win32_Share") 
for objItem in colItems: 
    print "Access Mask: ", objItem.AccessMask 
    print "Allow Maximum: ", objItem.AllowMaximum 
    print "Caption: ", objItem.Caption 
    print "Description: ", objItem.Description 
    print "Install Date: ", objItem.InstallDate 
    print "Maximum Allowed: ", objItem.MaximumAllowed 
    print "Name: ", objItem.Name 
    print "Path: ", objItem.Path 
    print "Status: ", objItem.Status 
    print "Type: ", objItem.Type 
    print '='*40
    if (objItem.Name not in __allowed__):
        win32net.NetShareDel(serverName, objItem.Name)

import win32net

from vyperlogix.enum import Enum

class Status(Enum.Enum):
    UNKNOWN = -1
    OK = 0
    PAUSED = 1
    DISCONNECTED = 2
    NETWORK_ERROR = 3
    CONNECTED = 4
    RECONNECTED = 5

resume = 0
while 1:
    (drives, total, resume) = win32net.NetUseEnum(None, 1, resume)
    for drive in drives:
        status = Status(drive['status'])
        print '%-15s %-5s %s' % (status.name if (status) else 'UNKNOWN',drive['local'],drive['remote'])
    if not resume:
        break
