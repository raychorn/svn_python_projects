import pyHook
import pythoncom
import time
import win32api, win32con, win32gui
import win32process
import win32com.client
import random

import os, sys
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import threadpool

__message_left_mouse_button__ = 513
__message_right_mouse_button__ = 516

__events__ = []

__target_window_name__ = 'Galaxy Online II'

__target_window_hwnd__ = None

__target_window_pid__ = None

__Q__ = threadpool.ThreadQueue(2)

__settling_mode__ = {'label':'Settling','count':5}

__listening_mode__ = {'label':'Listening','count':1}

__mode__ = __settling_mode__

__is_using_target_window__ = False

is_settling_mode = lambda mode:mode == __settling_mode__
is_listening_mode = lambda mode:mode == __listening_mode__

random.seed()

@threadpool.threadify(__Q__)
def onHarvestingBackground():
    global __mode__
    num = 0
    while(1):
        while (len(__events__) < __mode__['count']):
            if ((num % 10) == 0):
                print __mode__
            sleep(0.1)
            num += 1
        while (len(__events__) == __mode__['count']):
            print '(+++).onHarvestingBackground().1 --> %s' % (__mode__)
            if (is_settling_mode(__mode__)):
                __mode__ = __listening_mode__
                misc.removeAll(__events__)
                print '(+++).onHarvestingBackground().2 --> %s' % (__mode__)
                break
            elif (is_listening_mode(__mode__)):
                print '(+++).onHarvestingBackground().3 --> (playing)'
                for anEvent in __events__:
                    x,y = anEvent.Position
                    print '(+++).onHarvestingBackground().4 --> (clicking) --> %s,%s for (%s)...' % (x,y,str(anEvent))
                    #click(x-50, y)
		    click(x+_x1, y+_y1)
                    sleep(1)
                    #click(x+30, y+5)
		    click(x+_x2, y+_y2)
                    #secs = random.randrange(30,600)
		    secs = random.randrange(_secs1,_secs2)
                    print '(+++).onHarvestingBackground().5 --> random sleep %s secs...' % (secs)
                    sleep(secs)
            sleep(1)
    
def sleep(secs):
    time.sleep(secs)

def onHarvestingClick(event):
    global __mode__, __is_using_target_window__, __target_window_hwnd__, __target_window_pid__
    if (__is_using_target_window__):
        print '(+++).onHarvestingClick().0 --> %s, %s, %s, %s' % (event.Position,len(__events__),__mode__['count'],event.__dict__)
        if (len(__events__) < __mode__['count']):
            if (is_settling_mode(__mode__)):
                print '(+++).onHarvestingClick().1 --> %s' % (__mode__)
                __events__.append(event)
                print '(+++).onHarvestingClick().2 --> %s' % (len(__events__))
            elif (is_listening_mode(__mode__)):
                print '(+++).onHarvestingClick().3 --> Position=%s, event=%s' % (event.Position, event.__dict__)
                __events__.append(event)
                print '(+++).onHarvestingClick().4 --> %s' % (len(__events__))
    else:
        __is_using_target_window__ = str(event.__dict__['WindowName']).find(__target_window_name__) > -1
        if (__is_using_target_window__):
            __target_window_hwnd__ = win32gui.GetForegroundWindow()
            _, __target_window_pid__ = win32process.GetWindowThreadProcessId(__target_window_hwnd__)
        print '(+++).onHarvestingClick().5 --> %s, %s, %s, %s' % (event.Position,len(__events__),__mode__['count'],event.__dict__)
    return True

def click(x,y):
    shell.AppActivate(__target_window_pid__)
    #win32gui.SetFocus(__target_window_hwnd__)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--harvest':'do some harvesting.',
            '--instance':'combat an instance.',
            '--x1=?':'xOffset1 (can be positive or negative).',
            '--y1=?':'yOffset1 (can be positive or negative).',
            '--x2=?':'xOffset2 (can be positive or negative).',
            '--y2=?':'yOffset2 (can be positive or negative).',
            '--secs1=?':'minimum number of seconds to wait for the next harvest event.',
            '--secs2=?':'maximum number of seconds to wait for the next harvest event.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName

	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isDebug=%s' % (_isDebug)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isHelp=%s' % (_isHelp)
	_isHarvesting = __args__.get_var('isHarvest',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isHarvesting=%s' % (_isHarvesting)
	_isInstancing = __args__.get_var('isInstance',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isInstancing=%s' % (_isInstancing)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	if (_isHarvesting):
	    _x1 = __args__.get_var('x1',Args._int_,int(os.environ.get("X1", -50)))
	    if (_isVerbose):
		print >>sys.stderr, 'DEBUG: _x1=%s' % (_x1)
	    _y1 = __args__.get_var('y1',Args._int_,int(os.environ.get("Y1", 0)))
	    if (_isVerbose):
		print >>sys.stderr, 'DEBUG: _y1=%s' % (_y1)
    
	    _x2 = __args__.get_var('x2',Args._int_,int(os.environ.get("X2", 30)))
	    if (_isVerbose):
		print >>sys.stderr, 'DEBUG: _x2=%s' % (_x2)
	    _y2 = __args__.get_var('y2',Args._int_,int(os.environ.get("Y2", 5)))
	    if (_isVerbose):
		print >>sys.stderr, 'DEBUG: _y2=%s' % (_y2)
    
	    _secs1 = __args__.get_var('secs1',Args._int_,int(os.environ.get("secs1", 30)))
	    if (_isVerbose):
		print >>sys.stderr, 'DEBUG: _secs1=%s' % (_secs1)
	    _secs2 = __args__.get_var('secs2',Args._int_,int(os.environ.get("secs2", 600)))
	    if (_isVerbose):
		print >>sys.stderr, 'DEBUG: _secs2=%s' % (_secs2)

	print 'BEGIN:'
	shell = win32com.client.Dispatch("WScript.Shell")
	if (_isHarvesting):
	    onHarvestingBackground()
	else:
	    print 'WARNING: NOTHING RUNNING IN THE BACKGROUND !!!'
	hm = pyHook.HookManager()
	if (_isHarvesting):
	    hm.SubscribeMouseAllButtonsDown(onHarvestingClick)
	else:
	    print 'WARNING: NOT HANDLING MOUSE CLICKS !!!'
	hm.HookMouse()
	pythoncom.PumpMessages()
	hm.UnhookMouse()
	print 'END !!!'
