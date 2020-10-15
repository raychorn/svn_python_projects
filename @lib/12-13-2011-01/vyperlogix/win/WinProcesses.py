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

import win32process
import win32con
import win32api
import win32pdh
import time 
import sys
from win32com.client import GetObject
from vyperlogix.enum import Enum

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.hash import lists

from vyperlogix.misc import ObjectTypeName

from vyperlogix.classes.CooperativeClass import Cooperative

from vyperlogix.trees.tinytree import tinytree

class Priorities(Enum.Enum):
    HIGH = win32process.HIGH_PRIORITY_CLASS
    ABOVE = win32process.ABOVE_NORMAL_PRIORITY_CLASS
    BELOW = win32process.BELOW_NORMAL_PRIORITY_CLASS
    IDLE = win32process.IDLE_PRIORITY_CLASS
    NORMAL = win32process.NORMAL_PRIORITY_CLASS
    REALTIME = win32process.REALTIME_PRIORITY_CLASS

class Win32Processes(Cooperative):
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
                    modules = None
                item = (process,procmemusage,str(modules))
                if (not isSilent):
                    print "PID: %s Mem: %sK [%s]" % item
                procsList.append(item)
                win32api.CloseHandle(procHandle)
        return procsList

    def setProcessPriorityByPID(self,pid,pClass):
        if (isinstance(pClass,int)):
            pHand = win32api.OpenProcess(win32con.PROCESS_SET_INFORMATION, 0, pid)
            if (pHand):
                win32process.SetPriorityClass(pHand,pClass)
            else:
                print >>sys.stderr, '(%s).WARNING :: Unable to get the process handler for PID of "%s".' % (ObjectTypeName.objectSignature(self),pid)
            win32api.CloseHandle(pHand)
        else:
            print >>sys.stderr, '(%s).ERROR :: Unable to determine how to handle the pClass of "%s" which is of type "%s".' % (ObjectTypeName.objectSignature(self),pClass,type(pClass))

    def getProcessPriorityByPID(self,pid):
        pClass = -1
        if (isinstance(pClass,int)):
            pHand = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, 0, pid)
            if (pHand):
                pClass = win32process.GetPriorityClass(pHand)
            else:
                print >>sys.stderr, '(%s).WARNING :: Unable to get the process handler for PID of "%s".' % (ObjectTypeName.objectSignature(self),pid)
            win32api.CloseHandle(pHand)
        else:
            print >>sys.stderr, '(%s).ERROR :: Unable to determine how to handle the pClass of "%s" which is of type "%s".' % (ObjectTypeName.objectSignature(self),pClass,type(pClass))
        return pClass

    def openProcessForPID(self,pid):
        try:
            procHandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, 0, pid)
        except Exception, details:
            print '(%s) :: ERROR due to "%s".' % (ObjectTypeName.objectSignature(self),str(details))
            procHandle = None
        return procHandle

    def openProcessTerminateForPID(self,pid):
        try:
            procHandle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
        except Exception, details:
            print '(%s) :: ERROR due to "%s".' % (ObjectTypeName.objectSignature(self),str(details))
            procHandle = None
        return procHandle

    def closeProcessHandle(self,procHandle):
        if (procHandle != None):
            try:
                win32api.CloseHandle(procHandle)
            except:
                pass

    def getProcessMemoryUsageForHandle(self,procHandle):
        if procHandle:
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
        _object = "Process" 
        instances = self.objlist()
        val = None 
        vals = []
        if procName in instances : 
            hq = win32pdh.OpenQuery() 
            hcs = [] 
            item = "ID Process" 
            path = win32pdh.MakeCounterPath( (None,_object,procName, None, 0, item) ) 
            hcs.append(win32pdh.AddCounter(hq, path)) 
            win32pdh.CollectQueryData(hq) 
            time.sleep(0.01) 
            win32pdh.CollectQueryData(hq)
            for hc in hcs: 
                t, val = win32pdh.GetFormattedCounterValue(hc,win32pdh.PDH_FMT_LONG)
                vals.append(val)
                win32pdh.RemoveCounter(hc) 
            win32pdh.CloseQuery(hq) 
        return vals

    def modulelist(self, handle):
        return win32process.EnumProcessModules(handle)

    def proclist(self):
        return win32process.EnumProcesses()

    def meminfo(self, handle):
        return win32process.GetProcessMemoryInfo(handle)

    def objlist(self):
        _object = "Process" 
        items, instances = win32pdh.EnumObjectItems(None,None,_object, win32pdh.PERF_DETAIL_WIZARD) 
        return instances 

class WinProcesses(Win32Processes):
    def __init__(self):
        try:
            import wmi
            self.wmi = GetObject('winmgmts:')
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, 'WARNING: Unable to access the WMI Object due to the need to be "Run as Administrator".  Rerun using the "Run as Administrator" option.'

    def listProcNames(self):
        try:
            import wmi
            processes = self.wmi.InstancesOf('Win32_Process')
            return [process.Properties_('Name').Value for process in processes]
        except:
            return ['wmi might be missing.']

    def pidForProcByName(self,procName=''):
        try:
            import wmi
            p = self.wmi.ExecQuery('select ProcessId from Win32_Process where Name="%s"' % procName)
            try:
                return p[0].Properties_('ProcessId').Value 
            except:
                return -1
        except:
            return -1

    def procNamesAndPIDs(self):
        try:
            import wmi
            c = wmi.WMI()
            return [(process.Name,process.ProcessId) for process in c.Win32_Process()]
        except:
            return ['wmi misng be missing.']

from ctypes import *

#PSAPI.DLL
psapi = windll.psapi
#Kernel32.DLL
kernel = windll.kernel32

def EnumProcesses():
    arr = c_ulong * 256
    lpidProcess= arr()
    cb = sizeof(lpidProcess)
    cbNeeded = c_ulong()
    hModule = c_ulong()
    count = c_ulong()
    modname = c_buffer(30)
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

    #Call Enumprocesses to get hold of process id's
    psapi.EnumProcesses(byref(lpidProcess), cb, byref(cbNeeded))

    #Number of processes returned
    nReturned = cbNeeded.value/sizeof(c_ulong())

    pidProcess = [i for i in lpidProcess][:nReturned]

    proc_names = []
    for pid in pidProcess:
        #Get handle to the process based on PID
        hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if hProcess:
            psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
            proc_names.append("".join([ i for i in modname if i != '\x00']))

            #-- Clean up
            for i in range(modname._length_):
                modname[i]='\x00'

            kernel.CloseHandle(hProcess)
    return proc_names

class ProcessNode(tinytree.Tree):
    def __init__(self, _tuple, children=None):
        procName, procId, parentId = _tuple if (isinstance(_tuple,tuple)) else tuple(_tuple)
        tinytree.Tree.__init__(self, children)
        self.__procName__ = procName
        self.__procId__ = procId
        self.__parentId__ = parentId
        self.parent = None

    def __repr__(self):
        return "<%s> <%s> <%s>" % (self.procName,self.procId,self.parentId)

    def _addChild(self, node):
        try:
            n = self.findForwards(procId=node.parentId)
            if (n is None):
                root = self.getRoot()
                root.addChild(node)
            else:
                n.addChild(node)
        except Exception, details:
            info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string

    def procName():
        doc = "procName"
        def fget(self):
            return self.__procName__
        def fset(self, procName):
            self.__procName__ = procName
        return locals()
    procName = property(**procName())

    def procId():
        doc = "procId"
        def fget(self):
            return self.__procId__
        def fset(self, procId):
            self.__procId__ = procId
        return locals()
    procId = property(**procId())

    def parentId():
        doc = "parentId"
        def fget(self):
            return self.__parentId__
        def fset(self, parentId):
            self.__parentId__ = parentId
        return locals()
    parentId = property(**parentId())

from vyperlogix.classes.MagicObject import MagicObject2

class ProcessTree(MagicObject2):
    def __init__(self):
        from vyperlogix.iterators import iterutils
        self.root = ProcessNode(["root",-1,-1])
        for procs in self.processTree:
            for aProc in iterutils.itergroup(procs,3):
                self.root._addChild(ProcessNode([aProc[0],aProc[1],aProc[2]]))
        self.reorder()

    def dump(self):
        self.root.dump()

    def reorder(self):
        _root = ProcessNode(["root",-1,-1])
        d = lists.HashedLists2()
        for node in self.root.preOrder():
            d[node.parentId] = node
        l = misc.sort(d.keys())
        for i in l:
            if (i > -1):
                _root._addChild(ProcessNode([d[i].procName,d[i].procId,d[i].parentId]))
        for node in self.root.preOrder():
            if (node.procId not in l):
                _root._addChild(node)
        self.root = _root
        return self.root

    def __call__(self,*args,**kwargs):
        '''Automatically redirect all unknown methods to the underlying Tree object.'''
        m = super(MagicObject2, self).__call__(*args,**kwargs)[1:]
        d = m[1][0]
        s = 'self.root.%s(%s=%s)' % (m[0][0],d.keys()[0],d.values()[0])
        try:
            n = eval(s)
        except Exception, _details:
            info_string = _utils.formattedException(details=_details)
            print >>sys.stderr, info_string
        self.__reset_magic__()
        return n

    def parents_without_nodes(self):
        d_nodes = {}
        for node in self.root.preOrder():
            n = self.root.findForwards(parentId=node.procId)
            if (n is None) and (node.procId > -1) and (node.parentId > -1):
                d_nodes[node.parentId] = node
        return misc.sort(d_nodes.keys())
    
    def procs_by_parentId(self):
        d = lists.HashedLists()
        for node in self.root.preOrder():
            d[str(node.parentId)] = node
        return d

    def processTree():
        doc = "processTree"
        def fget(self):
            import win32pdh
            object = 'Process'
            items, instances = win32pdh.EnumObjectItems(None, None, object, win32pdh.PERF_DETAIL_WIZARD)
            instance_dict = {}
            for instance in instances:
                try:
                    instance_dict[instance] = instance_dict[instance] + 1
                except KeyError:
                    instance_dict[instance] = 0
            procs = []
            for instance, max_instances in instance_dict.items():
                t = []
                for inum in xrange(max_instances+1):
                    hq = win32pdh.OpenQuery()
                    hcs = []
                    for item in ['ID Process', 'Creating Process ID']:
                        path = win32pdh.MakeCounterPath((None,object,instance,None,inum,item))
                        hcs.append(win32pdh.AddCounter(hq,path))
                    win32pdh.CollectQueryData(hq)
                    t.append(instance)
                    for hc in hcs:
                        type,val=win32pdh.GetFormattedCounterValue(hc,win32pdh.PDH_FMT_LONG)
                        t.append(val)
                        win32pdh.RemoveCounter(hc)
                    win32pdh.CloseQuery(hq)
                procs.append(t)
            return procs
        return locals()
    processTree = property(**processTree())

if __name__=="__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    procTree = ProcessTree()
    procTree.dump()
    print '='*80
    n = procTree.findForwards({'procId':6588})
    if (n):
        n.dump()
    else:
        print 'Cannot locate the desired Node.'
    print '='*80
    # ignore the proc's that were collected from the initial scan.
    # proc names must be 'python' or 'cmd'
    # use information about the list of top-level procs from the start-up process.
    d = procTree.procs_by_parentId()
    d.prettyPrint(title='procs_by_parentId',fOut=sys.stdout)

    #win_proc = WinProcesses()

    #test = win_proc.listprocesses()
    #print test

    #print 'pid=(%s)' % win_proc.getProcessIdByName('python')
    #print 'memory=(%s)' % win_proc.getProcessMemoryUsageByName('python')

    #l = EnumProcesses()
    #print '\n'.join(l)

    # +++ Make this into a method of an object above that knows how to return a process tree using the parent/child relationships where the
    # Parent is listed after the child.

    #procTree = ProcessTree()
    #procTree.dump()
    #print '='*80
    #_goal = None
    #while (1):
        #nodeless_parents = procTree.parents_without_nodes(goal=_goal)
        #if (_goal is not None):
            #procTree.dump()
            #print '='*80
        #if (len(nodeless_parents) > 0):
            #i = nodeless_parents[0]
            #procTree.root.addChild(ProcessNode(['root',i,-1]))
            #procTree.dump()
            #print '-'*80
            #_goal = i
        #else:
            #break
    #pass
