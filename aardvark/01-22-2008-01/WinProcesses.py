import win32process
import win32con
import win32api
import win32pdh
import time 

class WinProcesses:
	def __init__(self):
		pass

	def listprocesses(self):
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
				print "PID: %s Mem: %sK [%s]" % (process,procmemusage,str(modules))
				win32api.CloseHandle(procHandle)

	def openProcessForPID(self,pid):
		try:
			procHandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, 0, pid)
		except:
			procHandle = ""
		return procHandle
	
	def closeProcessHandle(self,procHandle):
		if procHandle != "":
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
