import win32process
import win32con
import win32api
import win32pdh
import time 
import sys
from win32com.client import GetObject
import wmi
import Enum

class Priorities(Enum.Enum):
	HIGH = win32process.HIGH_PRIORITY_CLASS
	ABOVE = win32process.ABOVE_NORMAL_PRIORITY_CLASS
	BELOW = win32process.BELOW_NORMAL_PRIORITY_CLASS
	IDLE = win32process.IDLE_PRIORITY_CLASS
	NORMAL = win32process.NORMAL_PRIORITY_CLASS
	REALTIME = win32process.REALTIME_PRIORITY_CLASS

class WinProcesses:
	def __init__(self):
		try:
			self.wmi = GetObject('winmgmts:')
		except:
			print >>sys.stderr, 'WARNING: Unable to access the WMI Object due to the need to be "Run as Administrator".  Rerun using the "Run as Administrator" option.'

	def listProcNames(self):
		processes = self.wmi.InstancesOf('Win32_Process')
		return [process.Properties_('Name').Value for process in processes]
	
	def pidForProcByName(self,procName=''):
		p = self.wmi.ExecQuery('select ProcessId from Win32_Process where Name="%s"' % procName)
		try:
			return p[0].Properties_('ProcessId').Value 
		except:
			return -1
	
	def procNamesAndPIDs(self):
		c = wmi.WMI()
		return [(process.Name,process.ProcessId) for process in c.Win32_Process()]

	def listprocesses(self,isSilent=False):
		procsList = []
		item = (None,None,None)
		for process in self.proclist():
			try:
				procHandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, 0, process)
			except:
				procHandle = ""
			if procHandle != "":
				procmeminfo = self.meminfo(procHandle)
				procmemusage = (procmeminfo["WorkingSetSize"]/1024)
				try:
					modules = self.modulelist(procHandle)
				except Exception, details:
					modules = 'Error details "%s".' % str(details)
				item = (process,procmemusage,str(modules))
				if (not isSilent):
					print "PID: %s Mem: %sK [%s]" % item
				procsList.append(item)
				win32api.CloseHandle(procHandle)
		return procsList

	def setProcessPriorityByPID(self,pid,pClass):
		if (isinstance(pClass,int)):
			pHand = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, pid)
			if (pHand):
				win32process.SetPriorityClass(pHand,pClass)
			else:
				print >>sys.stderr, '(setProcessPriorityByPID).WARNING :: Unable to get the process handler for PID of "%s".' % pid
			win32api.CloseHandle(pHand)
		else:
			print >>sys.stderr, '(setProcessPriorityByPID).ERROR :: Unable to determine how to handle the pClass of "%s" which is of type "%s".' % (pClass,type(pClass))
	
	def openProcessForPID(self,pid):
		try:
			procHandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, 0, pid)
		except Exception, details:
			print '(openProcessForPID) :: ERROR due to "%s".' % str(details)
			procHandle = None
		return procHandle
	
	def closeProcessHandle(self,procHandle):
		if (procHandle != None):
			try:
				win32api.CloseHandle(procHandle)
			except:
				pass
	
	def getProcessMemoryUsageForHandle(self,procHandle):
		if procHandle != "":
			procmeminfo = self.meminfo(procHandle)
			procmemusage = (procmeminfo["WorkingSetSize"]/1024)
			return procmemusage
		return -1
	
	def getProcessMemoryUsageByPID(self,pid):
		procHandle = self.openProcessForPID(pid)
		procmemusage = self.getProcessMemoryUsageForHandle(procHandle)
		self.closeProcessHandle(procHandle)
		return procmemusage
	
	def getProcessMemoryUsageByName(self, procName):
		return self.getProcessMemoryUsageByPID(self.getProcessIdByName(procName))
	
	def getProcessIdByName(self, procName):
		object = "Process" 
		instances = self.objlist()
		val = None 
		if procName in instances : 
			hq = win32pdh.OpenQuery() 
			hcs = [] 
			item = "ID Process" 
			path = win32pdh.MakeCounterPath( (None,object,procName, None, 0, item) ) 
			hcs.append(win32pdh.AddCounter(hq, path)) 
			win32pdh.CollectQueryData(hq) 
			time.sleep(0.01) 
			win32pdh.CollectQueryData(hq) 
			for hc in hcs: 
				type, val = win32pdh.GetFormattedCounterValue(hc,win32pdh.PDH_FMT_LONG) 
				win32pdh.RemoveCounter(hc) 
			win32pdh.CloseQuery(hq) 
		return val 

	def modulelist(self, handle):
		return win32process.EnumProcessModules(handle)

	def proclist(self):
		return win32process.EnumProcesses()

	def meminfo(self, handle):
		return win32process.GetProcessMemoryInfo(handle)

	def objlist(self):
		object = "Process" 
		items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD) 
		return instances 

if __name__=="__main__":
	win_proc = WinProcesses()

	#test = win_proc.listprocesses()
	#print test

	print 'pid=(%s)' % win_proc.getProcessIdByName('python')
	print 'memory=(%s)' % win_proc.getProcessMemoryUsageByName('python')
