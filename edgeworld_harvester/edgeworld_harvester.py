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

__target_window_name__ = 'Edgeworld'

__target_window_hwnd__ = None

__target_window_pid__ = None

__Q__ = threadpool.ThreadQueue(2)

__settling_mode__ = {'label':'Settling','count':4}

__listening_mode__ = {'label':'Listening','count':1}

__mode__ = __settling_mode__

__is_using_target_window__ = False

is_settling_mode = lambda mode:mode == __settling_mode__
is_listening_mode = lambda mode:mode == __listening_mode__

random.seed()

@threadpool.threadify(__Q__)
def onBackground():
    global __mode__
    num = 0
    alt_base_event = None
    alt_base_harvester_event = None
    main_base_event = None
    main_base_harvester_event = None
    while(1):
        while (is_settling_mode(__mode__)) and (len(__events__) < __mode__['count']):
            if ((num % 10) == 0):
                print __mode__
            sleep(0.1)
            num += 1
        while (1):
            print '(+++).onBackground().1 --> %s' % (__mode__)
            if (is_settling_mode(__mode__)):
                __mode__ = __listening_mode__
		alt_base_event = __events__[0]
		alt_base_harvester_event = __events__[1]
		main_base_event = __events__[2]
		main_base_harvester_event = __events__[3]
                misc.removeAll(__events__)
                print '(+++).onBackground().2 --> %s' % (__mode__)
                break
            elif (is_listening_mode(__mode__)):
                print '(+++).onBackground().3 --> (playing)'
		x,y = main_base_harvester_event.Position
		print '(+++).onBackground().4 --> (clicking) --> %s,%s for (%s)...' % (x,y,str(main_base_harvester_event))
		click(int(x)+int(_x1), int(y)+int(_y1))
		sleep(3)
		click(int(x)+int(_x2), int(y)+int(_y2))
		sleep(3)

		x,y = alt_base_event.Position
		print '(+++).onBackground().4a --> (clicking) --> %s,%s for (%s)...' % (x,y,str(alt_base_event))
		click(int(x), int(y))
		sleep(10)

		x,y = alt_base_harvester_event.Position
		print '(+++).onBackground().4b --> (clicking) --> %s,%s for (%s)...' % (x,y,str(alt_base_harvester_event))
		click(int(x)+int(_x1), int(y)+int(_y1))
		sleep(3)
		click(int(x)+int(_x2), int(y)+int(_y2))
		sleep(3)
		
		x,y = main_base_event.Position
		print '(+++).onBackground().4c --> (clicking) --> %s,%s for (%s)...' % (x,y,str(main_base_event))
		click(int(x), int(y))
		sleep(10)

		secs = random.randrange(_secs1,_secs2)
		print '(+++).onBackground().5 --> random sleep %s secs...' % (secs)
		sleep(secs)
            sleep(3)
    
def sleep(secs):
    time.sleep(secs)

def onclick(event):
    global __mode__, __is_using_target_window__, __target_window_hwnd__, __target_window_pid__
    if (__is_using_target_window__):
        print '(+++).onclick().0 --> %s, %s, %s, %s' % (event.Position,len(__events__),__mode__['count'],event.__dict__)
        if (len(__events__) < __mode__['count']):
            if (is_settling_mode(__mode__)):
                print '(+++).onclick().1 --> %s' % (__mode__)
                __events__.append(event)
                print '(+++).onclick().2 --> %s' % (len(__events__))
            elif (is_listening_mode(__mode__)):
                print '(+++).onclick().3 --> Position=%s, event=%s' % (event.Position, event.__dict__)
                __events__.append(event)
                print '(+++).onclick().4 --> %s' % (len(__events__))
    else:
        __is_using_target_window__ = str(event.__dict__['WindowName']).find(__target_window_name__) > -1
        if (__is_using_target_window__):
            __target_window_hwnd__ = win32gui.GetForegroundWindow()
            _, __target_window_pid__ = win32process.GetWindowThreadProcessId(__target_window_hwnd__)
        print '(+++).onclick().5 --> %s, %s, %s, %s' % (event.Position,len(__events__),__mode__['count'],event.__dict__)
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

	if (_isHelp):
	    ppArgs()
	    sys.exit()

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
	onBackground()
	hm = pyHook.HookManager()
	hm.SubscribeMouseAllButtonsDown(onclick)
	hm.HookMouse()
	pythoncom.PumpMessages()
	hm.UnhookMouse()
	print 'END !!!'
