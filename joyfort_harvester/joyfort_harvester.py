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

from vyperlogix.sockets import SocketServer

__message_left_mouse_button__ = 513
__message_right_mouse_button__ = 516

__events__ = []

__target_window_name__ = 'S4 - Perseus'

__target_window_hwnd__ = None

__target_window_pid__ = None

__Q__ = threadpool.ThreadQueue(10)

__settling_mode__ = {'label':'Settling','count':16}

__listening_mode__ = {'label':'Listening','count':1,'waitSecs':15*60}

__mode__ = __settling_mode__

__is_using_target_window__ = False

is_settling_mode = lambda mode:mode == __settling_mode__
is_listening_mode = lambda mode:mode == __listening_mode__

is_events_count_less_than_expected_count = lambda events,mode:len(events) < mode['count']
__ignore_onclick_events__ = False

__shutdown__ = '___Shutdown___'
__ipAddr__ = '127.0.0.1'
__port__ = 55555
__bufSize__ = 4096

random.seed()

@threadpool.threadify(__Q__)
def onBackground():
    global __mode__, __ignore_onclick_events__
    num = 0
    while(1):
	while (is_settling_mode(__mode__)) and (is_events_count_less_than_expected_count(__events__,__mode__)):
            if ((num % 10) == 0):
                print '\tCOUNT: %d' % (len(__events__))
            sleep(0.1)
            num += 1
        while (1):
            if (is_settling_mode(__mode__)):
                __mode__ = __listening_mode__
		__mode__['beginWait'] = time.clock()
                print '\tMODE -> LISTENING !!!'
                break
            elif (is_listening_mode(__mode__)):
		if ((num % 10) == 0):
		    print '\tMODE -> PLAYING !!!'
		__mode__['currentWait'] = time.clock() - __mode__['beginWait']
		delta = float(__mode__['waitSecs']) - float(__mode__['currentWait'])
		pcent = 100.0 - ((delta / float(__mode__['waitSecs'])) * 100.0)
		print '\t%4.2f%%' % (pcent)
		
		if (__mode__['currentWait'] >= __mode__['waitSecs']):
		    __ignore_onclick_events__ = True
		    for ev in __events__:
			x,y = ev.Position
			print '\t%d,%d !!!' % (x,y)
			click(int(x), int(y))
			sleep(1)
		    __mode__['beginWait'] = time.clock()
		    __ignore_onclick_events__ = False
		num += 1
            sleep(1)
    
def sleep(secs):
    time.sleep(secs)

def distance(x1,y1,x2,y2):
    import math
    return math.sqrt(((x2-x1)+(y2-y1))**2)

def onclick(event):
    global __mode__, __is_using_target_window__, __target_window_hwnd__, __target_window_pid__
    if (not __ignore_onclick_events__):
	if (__is_using_target_window__):
	    if (is_events_count_less_than_expected_count(__events__,__mode__)):
		if (is_settling_mode(__mode__)):
		    print '\tRECORDING !!!'
		    __events__.append(event)
		elif (is_listening_mode(__mode__)):
		    print '\tLISTENING #%d !!!' % (len(__events__))
	else:
	    print '%s\n(%s)' % (event.__dict__['WindowName'],__target_window_name__)
	    __is_using_target_window__ = str(event.__dict__['WindowName']).find(__target_window_name__) > -1
	    print '__is_using_target_window__\n(%s)' % (__is_using_target_window__)
	    if (__is_using_target_window__):
		__target_window_hwnd__ = win32gui.GetForegroundWindow()
		_x_, __target_window_pid__ = win32process.GetWindowThreadProcessId(__target_window_hwnd__)
	    pass
    return True

def click(x,y):
    shell.AppActivate(__target_window_pid__)
    #win32gui.SetFocus(__target_window_hwnd__)
    win32api.SetCursorPos((x,y))
    sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def socketCallback(server,connHandle,data):
    response = {}
    print >>sys.stderr, '(socketCallback) :: server=(%s), connHandle=(%s)' % (str(server),str(connHandle))
    if (isinstance(data,str)):
        #response = processor.processXML(connHandle,data)
	print data
    #else:
        #response = ''.join(['<%s>%s</%s>' % (c[0],c[-1],c[0]) for c in XMLProcessor.LicenseLevels])
        #response = '<LicenseLevels>' + response + '</LicenseLevels>'
        #server.__send__(connHandle,response)
        #response = '<license>' + str(XMLProcessor.LicenseLevels(processor.isLicensed)).split('.')[-1] + '</license>'
        #server.__send__(connHandle,response)
        #response = ''.join(['<%s>%s</%s>' % (c[0],c[-1],c[0]) for c in XMLProcessor.Commands])
        #response = '<response><commands>' + response + '</commands>'
        #response += '<machineID>' + GetComputerName() + '</machineID></response>'
    json = {}
    return json

@threadpool.threadify(__Q__)
def SocketServerSetup():
    theServer = SocketServer.SocketServer()
    theServer.ipAddr = __ipAddr__
    theServer.port = __port__
    theServer.sShutdown = __shutdown__
    theServer.iBufSize = __bufSize__
    #theServer.acceptConnectionsFrom = []
    theServer.callBack = socketCallback
    theServer.isSwappingBits = True
    print '(main) :: theServer=(%s)' % (str(theServer))
    theServer.startup()
    print '(main) :: End of Main !'

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--winname=?':'Target Window Name.',
            '--events=?':'Number of events to capture.',
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

	_target_window_name = __args__.get_var('winname',Args._str_,os.environ.get("winname", __target_window_name__))
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _target_window_name=%s' % (_target_window_name)
	__target_window_name__ = _target_window_name

	_events = __args__.get_var('events',Args._int_,int(os.environ.get("EVENTS", 16)))
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _events=%s' % (_events)
	__settling_mode__['count'] = _events

	#_x2 = __args__.get_var('x2',Args._int_,int(os.environ.get("X2", 30)))
	#if (_isVerbose):
	    #print >>sys.stderr, 'DEBUG: _x2=%s' % (_x2)
	#_y2 = __args__.get_var('y2',Args._int_,int(os.environ.get("Y2", 5)))
	#if (_isVerbose):
	    #print >>sys.stderr, 'DEBUG: _y2=%s' % (_y2)

	#_secs1 = __args__.get_var('secs1',Args._int_,int(os.environ.get("secs1", 30)))
	#if (_isVerbose):
	    #print >>sys.stderr, 'DEBUG: _secs1=%s' % (_secs1)
	#_secs2 = __args__.get_var('secs2',Args._int_,int(os.environ.get("secs2", 600)))
	#if (_isVerbose):
	    #print >>sys.stderr, 'DEBUG: _secs2=%s' % (_secs2)

	print 'BEGIN:'
	#SocketServerSetup()
	shell = win32com.client.Dispatch("WScript.Shell")
	onBackground()
	hm = pyHook.HookManager()
	hm.SubscribeMouseAllButtonsDown(onclick)
	hm.HookMouse()
	pythoncom.PumpMessages()
	hm.UnhookMouse()
	print 'END !!!'
