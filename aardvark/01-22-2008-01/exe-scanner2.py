import os
import sys
import psyco
from ioTimeAnalysis import *
from threadpool import *
import traceback
import win32api
import win32file
from Queue import Queue
import threading
from sortedDictionary import *
import copy
from getFileVersionInfo import *

_isVerbose = False

_pool = Pool(1000)

_files_queue = Queue()

_master_dict = {}

_ShowVer_exe = 'ShowVer.exe'

_ShowVer_cmd = 'ShowVers.cmd'

_resultsFolderName = 'exe-scanner'

_SystemVolumeInformation_symbol = 'System Volume Information'

def filterFolderRoot(fname):
    toks = fname.split('\\')
    tokens = []
    for t in toks:
	if (len(t) > 0):
	    tokens.append(t)
    return '\\'.join(tokens)

def PrintSpaceReport(drive):
    sectorsPerCluster, bytesPerSector, numFreeClusters, totalNumClusters = win32file.GetDiskFreeSpace(drive + ":\\")
    sectorsPerCluster = long(sectorsPerCluster)
    bytesPerSector = long(bytesPerSector)
    numFreeClusters = long(numFreeClusters)
    totalNumClusters = long(totalNumClusters)
    print
    print "Drive:     ", drive + ":\\"
    print "FreeSpace: ", (numFreeClusters * sectorsPerCluster * bytesPerSector) / (1024 * 1024), "MB"
    print "TotalSpace:", (totalNumClusters * sectorsPerCluster * bytesPerSector) / (1024 * 1024), "MB"
    print "UsedSpace: ", ((totalNumClusters - numFreeClusters ) * sectorsPerCluster * bytesPerSector) / (1024 * 1024), "MB"

def driveTypeName(drive_type):
    if (drive_type == win32file.DRIVE_CDROM):
	return 'DRIVE_CDROM'
    elif (drive_type == win32file.DRIVE_FIXED):
	return 'DRIVE_FIXED'
    elif (drive_type == win32file.DRIVE_NO_ROOT_DIR):
	return 'DRIVE_NO_ROOT_DIR'
    elif (drive_type == win32file.DRIVE_RAMDISK):
	return 'DRIVE_RAMDISK'
    elif (drive_type == win32file.DRIVE_REMOTE):
	return 'DRIVE_REMOTE'
    elif (drive_type == win32file.DRIVE_REMOVABLE):
	return 'DRIVE_REMOVABLE'
    elif (drive_type == win32file.DRIVE_UNKNOWN):
	return 'DRIVE_UNKNOWN'
    return ''

def GetDrives(typeName='',op='==') : 
    "Returns a list of valid drives on this system, in order" 
    _drives = []
    toks = []
    _toks = win32api.GetLogicalDriveStrings().split('\000')
    try:
	dt = driveTypeName(typeName)
	if (len(dt) > 0):
	    typemask = typeName
	else:
	    typeName = str(typeName).split('.')[-1]
	    typemask = eval('win32file.%s' % typeName)
    except:
	typemask = 0xffffffff
    for t in _toks:
	if (len(t.strip()) > 0):
	    toks.append(t)
    drives = []
    for d in toks:
	dt = win32file.GetDriveType(d)
	bool = False
	if (op.lower() == '=='):
	    bool = (typemask == dt)
	else:
	    bool = (typemask & dt)
	if (bool):
	    drives.append([d,driveTypeName(dt)])
    return drives

def getWindowsSystemRoot():
    return os.environ['SystemRoot']

def destCmdName():
    return '%s%s%s' % (_resultsFolderName,os.sep,_ShowVer_cmd)

@threadpool(_pool)
def gatherExeVersionInfo(fname):
    _master_dict[fname] = getFileVersionInfo(fname)

@threadpool(_pool)
def queueFile(root,f):
    fname = filterFolderRoot(root+os.sep+f)
    _files_queue.put(fname)
    gatherExeVersionInfo(fname)

@threadpool(_pool)
def scanFolder(root,_files):
    d = {}
    for f in [f for f in _files]:
	tname = str(f.split('.')[-1]).strip().lower()
	if (d.has_key(tname) == False):
	    d[tname] = []
	d[tname].append(f)
    if (d.has_key('exe')):
	for x in d['exe']:
	    queueFile(root,x)

@threadpool(_pool)
def exeScanFolder(top,topdown):
    for root, dirs, files in os.walk(top, topdown):
	scanFolder(root,files)

def exeScan(top,sysRootFolder):
    print '(exeScan) :: top=(%s)' % top
    _sysRootFolder = sysRootFolder+os.sep
    toks = sysRootFolder.split(os.sep)
    sviName = toks[0] + os.sep + _SystemVolumeInformation_symbol
    for root, dirs, files in os.walk(top, topdown=True):
	_root = filterFolderRoot(root)+os.sep
	for d in dirs:
	    dn = _root+d
	    if (dn.endswith(os.sep) == False):
		dn += os.sep
	    if ( (dn.startswith(_sysRootFolder) == False) and (dn.startswith(sviName) == False) ):
		exeScanFolder(dn,True)
	break

@threadpool(_pool)
def exeScanThreaded(top,sysRootFolder):
    return exeScan(top,sysRootFolder)

def queue2Dict(q):
    d = {}
    try:
	while (q.qsize() > 0):
	    f = q.get()
	    d[f] = f
    except:
	pass
    return d

def queue2SortedList(q):
    l = []
    try:
	while (q.qsize() > 0):
	    f = q.get()
	    l.append(f)
    except:
	pass
    l.sort()
    return l

def main():
    drives = GetDrives(win32file.DRIVE_FIXED)
    sysRootFolder = getWindowsSystemRoot()
    print '(main) :: sysRootFolder=(%s)' % sysRootFolder
    print '(main) :: drives=(%s)' % str(drives)
    if (os.path.exists(_resultsFolderName) == False):
	os.mkdir(_resultsFolderName)
    destCmd = destCmdName()
    if (os.path.exists(destCmd)):
	os.remove(destCmd)
    for d in drives:
	print '(main) :: d=(%s)' % str(d)
	top = str(d[0])
	if (top.endswith(top) != os.sep):
	    top += os.sep
	ioBeginTime('exeScan.%s' % top)
	files = exeScanThreaded(top,sysRootFolder)
	ioEndTime('exeScan.%s' % top)
	break
    _pool.join()
    ioTimeAnalysisReport()
    print '\nThere are %d executable files.\n' % (_files_queue.qsize())
    list = queue2SortedList(_files_queue)
    for l in list:
	versInfo = _master_dict[l]
	codepage_id = versInfo.keys()[0]
	print 'fname=(%s)' % (l)
	dInfo = versInfo[codepage_id]
	for k in dInfo.keys():
	    print '\t%s=(%s)' % (k,dInfo[k])
    print '\n'

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
    print '--help                      ... displays this help text.'
    print '--verbose                   ... output more stuff.'
else:
    for i in xrange(len(sys.argv)):
	bool = (sys.argv[i].find('--match=') > -1)
	if (bool): 
	    toks = sys.argv[i].split('=')
	    _strategy = toks[1]
	elif (sys.argv[i].find('--verbose') > -1):
	    _isVerbose = True
psyco.bind(main)
main()
