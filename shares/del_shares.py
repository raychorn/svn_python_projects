import os, sys
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

import win32api
import win32com.client 
import win32net

from vyperlogix.process import Popen

__allowed__ = ['IPC$']

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName

	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print 'DEBUG: _isDebug=%s' % (_isDebug)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print 'DEBUG: _isHelp=%s' % (_isHelp)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	strComputer = "."
	serverName = None
	if serverName is None:
	    serverName = "\\\\" + win32api.GetComputerName()
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
	colItems = objSWbemServices.ExecQuery("Select * from Win32_Share") 
	for objItem in colItems: 
	    if (_isVerbose or _isDebug):
		print "Access Mask: ", objItem.AccessMask 
		print "Allow Maximum: ", objItem.AllowMaximum 
		print "Caption: ", str(objItem.Caption)
		print "Description: ", str(objItem.Description) 
		print "Install Date: ", objItem.InstallDate 
		print "Maximum Allowed: ", objItem.MaximumAllowed 
		print "Name: ", str(objItem.Name) 
		print "Path: ", str(objItem.Path) 
		print "Status: ", str(objItem.Status) 
		print "Type: ", str(objItem.Type) 
		print '='*40
	    if (objItem.Name not in __allowed__):
		if (_isVerbose or _isDebug):
		    print "Removing %s from %s" % (str(objItem.Name),serverName)
		win32net.NetShareDel(serverName, str(objItem.Name))
		
	def handle_command(data):
	    print data
	
	_cmd_ = 'net stop RemoteRegistry'
	print 'INFO: %s' % (_cmd_)
	Popen.Shell(_cmd_, shell=None, env=None, isExit=True, isWait=False, isVerbose=True, fOut=handle_command)
	
	raw_input('Waiting for user interaction...')

