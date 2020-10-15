import os
import sys
import psyco
from vyperlogix.win import WinProcesses
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint
import atexit
import wmi
import pprint

_isVerbose = False
_isProcList = False
_isProcWatcher = False

procName = ''

_fHand_logFileName = ''

def cmpFunc(x,y):
    val = 0
    if (x[0] < y[0]):
        val = -1
    elif (x[0] > y[0]):
        val = 1
    return val

def _getProcsList(_win_proc):
    procs = _win_proc.procNamesAndPIDs()
    procs.sort(cmpFunc)
    return [(str(p[0]),str(p[1])) for p in procs]

def getProcsList(_win_proc):
    myProcs = _getProcsList(_win_proc)
    myProcs.insert(0,('Process Name', 'PID (Process ID)'))
    pPretty = PrettyPrint.PrettyPrint('',myProcs,False,', ')
    pPretty.pprint()

def tupleListToDict(tList):
    d = {}
    for p in tList:
        value = p[-1]
        if (str(p[-1]).isdigit()):
            value = int(p[-1])
        d[p[0]] = value
        d[value] = p[0]
    return d

def Dummy(pName):
    pass

def procWatcher(pName, fCallback=Dummy):
    """This is a blocking function that sits and waits for the named process to be started."""
    c = wmi.WMI()
    if ( (isinstance(pName,str)) and (len(pName) > 0) ):
        _pid = win_proc.pidForProcByName(pName)
        isRunning = str(_pid).isdigit()

        if (not isRunning):
            watcher = c.watch_for (
                notification_type = "Creation",
                wmi_class = "Win32_Process",
                delay_secs = 2,
                Name = pName
            )
            print >>sys.stdout, '(procWatcher) :: Waiting for process named "%s" to be started.' % pName
            proc_created = watcher()
            print >>sys.stdout, '(procWatcher) :: Process Named "%s" has been started.' % pName
        if (str(type(fCallback)).find("'function'") > -1):
            try:
                fCallback(pName,win_proc.pidForProcByName(pName))
            except Exception, details:
                print >>sys.stderr, '(procWatcher) :: ERROR in CallBack due to "%s".' % str(details)
        if (_isProcWatcher):
            watcher = c.watch_for (
                notification_type = "Deletion",
                wmi_class = "Win32_Process",
                delay_secs = 2,
                Name = pName
            )
            print >>sys.stdout, '(procWatcher) :: Waiting for process named "%s" to be killed.' % pName
            proc_killed = watcher()
            print >>sys.stdout, '(procWatcher) :: Process Named "%s" has been killed.' % pName

def adjustRunningProcess(pName,pid):
    from vyperlogix.win import priority
    msg = '(adjustRunningProcess) :: Adjusting the process named "%s" with PID of "%s" to priority of "%s" (%s).' % (pName,pid,WinProcesses.Priorities.HIGH,int(WinProcesses.Priorities.HIGH))
    print >>sys.stdout, msg
    print >>sys.stderr, msg
    priority.setpriority(pid=pid,priority=4)
    win_proc.setProcessPriorityByPID(pid,WinProcesses.Priorities.HIGH.value)
    #pri = win_proc.getProcessPriorityByPID(pid)
    msg = '(adjustRunningProcess) :: Adjusted the process named "%s" with PID of "%s" to priority of "%s" (%s).' % (pName,pid,pri)
    print >>sys.stdout, msg
    print >>sys.stderr, msg

def main(_win_proc,_procName):
    if (_isProcList):
        getProcsList(_win_proc)
    elif (len(procName) > 0):
        while (_isProcWatcher == True):
            procWatcher(_procName,adjustRunningProcess)
            closeLogFile()
            openLogFile()
        else:
            procWatcher(_procName,adjustRunningProcess)

def termination():
    print >>sys.stdout, '(termination) :: Closing...'

def openLogFile():
    global _fHand_logFileName
    try:
        _fHand_logFileName = os.sep.join([os.curdir,_argsObj.programName+'.log'])
        _fHand_logFile = open(_fHand_logFileName,'w+')
        sys.stderr = _fHand_logFile
        #sys.stdout = _fHand_logFile
    except Exception, details:
        print >>sys.stderr, "Execution of Log File Creation failed:", details

def closeLogFile():
    try:
        sys.stderr.flush()
        sys.stderr.close()
    except Exception, details:
        print >>sys.stderr, "Execution of Log File Finalization failed:", details

args = {'--help':'displays this help text.',
        '--verbose':'output more stuff.',
        '--proclist':'get process list.',
        '--procWatcher':'watches for the named process to boost.',
        '--boost=process_name':'boost this process by name.'
        }

_argsObj = Args.Args(args)

try:
    _isHelp = _argsObj.booleans['isHelp']
except:
    _isHelp = False

if (_isHelp):
    print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)

    pArgs = [(k,args[k]) for k in args.keys()]
    pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
    pPretty.pprint()

try:
    _isVerbose = _argsObj.booleans['isVerbose']
except:
    _isVerbose = False

try:
    _isProcList = _argsObj.booleans['isProclist']
except:
    _isProcList = False

try:
    _isProcWatcher = _argsObj.booleans['isProcWatcher']
except:
    _isProcWatcher = False

try:
    procName = _argsObj.arguments['boost']
except:
    procName = ''

from vyperlogix.misc import _psyco

_stderr = sys.stderr
_stdout = sys.stdout
openLogFile()
try:
    _psyco.importPsycoIfPossible(func=main)
    atexit.register(termination)
    win_proc = WinProcesses.WinProcesses()
    main(win_proc,procName)
except Exception, details:
    print >>sys.stderr, "Execution of Main() failed:", details
sys.stderr = _stderr
sys.stdout = _stdout
