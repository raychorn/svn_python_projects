import re
import os, sys
from glob import glob

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.hash.lists import HashedLists

from vyperlogix.sockets import getip

from vyperlogix.sockets import netstat

___is___ = True
try:
    from vyperlogix.win import WinProcesses
except ImportError, ex:
    ___is___ = False
    print _utils.formattedException(details=ex)

___can_wmi___ = True
try:
    import wmi
except ImportError, ex:
    ___can_wmi___ = False
    print _utils.formattedException(details=ex)

___can_win32gui___ = True
try:
    import win32gui
except ImportError, ex:
    ___can_win32gui___ = False
    print _utils.formattedException(details=ex)

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

import ctypes
 
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
 
def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        try:
            import win32process
            threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
        except:
            threadId, processId = (None,None)
        titles.append('%s --> (%s)'  % (buff.value,processId))
    return True

if (__name__ == '__main__'):
    #for f in sys.path:
        #print f
        
    #w = WinProcesses.Win32Processes()
    #print w.listprocesses()
    
    #print '='*40

    procs2 = procs = HashedLists()
    
    print '___can_wmi___ --> %s' % (___can_wmi___)
    if (___is___):
        wp = WinProcesses.WinProcesses()
        plist = wp.procNamesAndPIDs()
        for p in [list(p) for p in plist]:
            procs[p[0]] = p[-1]
        #print '\n'.join(['(***) %s --> %s'%(p) for p in plist])
        #print '='*40
        #procs.prettyPrint()
        procs2 = procs.insideOut()
        #print '='*40
        #print '='*40
        #procs2.prettyPrint()
    else:
        print '___is___ --> %s' % (___is___)

    #print WinProcesses.EnumProcesses()

    print '='*40
    
    #if (___can_win32gui___):
        #w = WindowMgr()
        #print '#'*40
        #items = [".*cmd.*",".*ic4vc.*",".*web.*",".*"]
        #for item in items:
            #print item
            #print w.find_window_wildcard(item)
            #print '#'*40
    #else:
        #print '___can_win32gui___ --> %s' % (___can_win32gui___)
    
    #titles = []
    #EnumWindows(EnumWindowsProc(foreach_window), 0)
    #print '\n'.join(titles)
    
    __targets__ = []

    def callback(data,targets,regex):
        try:
            results = regex.findall(data['title'])
            if (len(results) > 0):
                targets.append(data)
        except:
            pass
    
    def _hwndCallback(hwnd, extra):
        try:
            import win32process
            threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
        except:
            threadId, processId = (None,None)
        wTitle = win32gui.GetWindowText(hwnd)
        item = {'hwnd':hwnd,'pid':processId,'title':wTitle,'class':win32gui.GetClassName(hwnd)}
        try:
            if (callable(extra['callback'])):
                extra['callback'](item,extra['targets'],extra['regex'])
        except:
            pass
        try:
            extra['items'].append(item)
        except:
            pass
    
    hwndList = []
    __re__ = re.compile("start.*-.*ic4vc.*_.*webserver.*..*cmd", re.MULTILINE)
    #__re__ = re.compile(".*", re.MULTILINE)
    try:
        import win32gui
        win32gui.EnumWindows(_hwndCallback, {'callback':callback,'targets':__targets__,'items':hwndList,'regex':__re__})
    except:
        pass
    __fmt__ = lambda item:', '.join(['%s=%s'%(k,v) for k,v in item.iteritems()])
    #print '\n'.join([__fmt__(t) for t in hwndList])

    print '#'*40

    for t in __targets__:
        print __fmt__(t)
        procname = misc.unpack(procs2[t['pid']])
        print procname
        if (str(procname).lower() == 'cmd.exe'):
            toks = str(t['title']).split(' - ')
            fpath = toks[-1]
            fdir = None
            fname = None
            fpat = None
            f = None
            files = []
            __fname__ = None
            if (os.path.exists(fpath)):
                fdir = os.path.dirname(fpath).replace(os.sep,'/')
                fname = os.path.basename(fpath)
            if (fname):
                ftoks = os.path.splitext(fname)
                fpat = ftoks[0].replace('#','')+ftoks[-1]
            if (fpat):
                ftoks = os.path.splitext(fpat)
                f = '%s/*%s*%s' % (fdir,ftoks[0],ftoks[-1])
                print 'f=%s' % (f)
                files = glob(f)
            print 'title=%s (%s) --> (%s) --> (%s) --> (%s) --> (%s)' % (t['title'],toks,fpath,fname,fpat,f)
            print 'len(files)=%s' % (len(files))
            if (len(files) > 0):
                print 'files=%s' % (files)
                for f in files:
                    ftoks = os.path.splitext(os.path.basename(f))
                    if (len(_utils.alpha_numeric_only(ftoks[0][0])) != 0):
                        __fname__ = f
            if (__fname__):
                n = netstat.NetStat()
                __ip__ = getip.get_ip_address_by_socket()
                print '(!!!) __fname__=%s' % (__fname__)
                print '(!!!) __ip__=%s' % (__ip__)
                print '-'*40
                print '\n'.join(n.ports)
                print '-'*40
                print '\n'.join(n.listeners)
                print '-'*40
    #print '\n'.join([__fmt__(t) for t in __targets__])

    print '#'*40
    
    #procTree = WinProcesses.ProcessTree()
    #print procTree.dump()
    