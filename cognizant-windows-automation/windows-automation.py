import pyHook
import pythoncom
import time
import win32api, win32con, win32gui
import win32process
import win32com.client
import random

import os, sys

from vyperlogix import misc

from lists import SeqentialList

__url__ = 'https://lam-933.dev.core.rackspace.com '

###########################################################################
## Interactions:
##
## User Clicks
##
## (1) - Select the browser.
## (2) - Browser Address Bar - issue URL.
## (3) - Login username - issue username.
## (4) - Password - issue password.
## (5) - 
##
###########################################################################

__browser_address_bar__ = 'browser-address-bar'
__login_username__ = 'login-username'
__login_password__ = 'login-password'

__actions__ = [
    {'type':__browser_address_bar__},
    {'type':__login_username__},
    {'type':__login_password__}
]
__actions__ = SeqentialList(__actions__)

__is__ = lambda action,key,value:(action.get(key) == value) if (isinstance(action,dict)) else False

__is_browser_address_bar__ = lambda action:__is__(action,'type',__browser_address_bar__)
__is_login_username__ = lambda action:__is__(action,'type',__login_username__)
__is_login_password__ = lambda action:__is__(action,'type',__login_password__)

from threading import Thread
import threading

def threaded(func):
    def proxy(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return proxy

from Queue import Queue

class ThreadQueue(Queue):
    def __init__(self, maxsize, isDaemon=False):
        self.__stopevent = threading.Event()
        assert maxsize > 0, 'maxsize > 0 required for ThreadQueue class'
        Queue.__init__(self, maxsize)
        for i in xrange(maxsize):
            thread = Thread(target = self._worker)
            thread.setDaemon(isDaemon)
            thread.start()

    def getIsRunning(self):
        return not self.__stopevent.isSet()
    
    def setIsRunning(self,isRunning):
        if (not isRunning):
            self.__stopevent.set()
        
    def _worker(self):
        while not self.__stopevent.isSet():
            if (not self.isRunning):
                break
            try:
                func, args, kwargs = self.get()
                func(*args, **kwargs)
            except Exception, details:
		import traceback
                print >>sys.stderr, '(%s._worker).Error :: "%s".' % (self.__class__,str(details))
		print >>sys.stderr, traceback.format_exc()
                self.task_done()
                self.join()
                raise
            else:
                self.task_done()

    def addJob(self, func, *args, **kwargs):
        self.put((func, args, kwargs))

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.__shutdown__()

    def __shutdown__(self):
        self.__stopevent.set()
        self.join()

    isRunning = property(getIsRunning, setIsRunning)

def threadify(threadQ):
    assert threadQ.__class__ in [ThreadQueue], 'threadify decorator requires a ThreadQueue or Queue object instance, use Queue when threading is not required.'
    def decorator(func):
        def proxy(*args, **kwargs):
            threadQ.put((func, args, kwargs))
            return threadQ
        return proxy
    return decorator
###########################################################################

__message_left_mouse_button__ = 513
__message_right_mouse_button__ = 516

__events__ = []

__target_window_name__ = 'Mozilla Firefox'

__target_window_hwnd__ = None

__target_window_pid__ = None

__Q__ = ThreadQueue(2)

__settling_mode__ = {'label':'Settling','count':5}

__listening_mode__ = {'label':'Listening','count':1}

__mode__ = __settling_mode__

__is_using_target_window__ = False

is_settling_mode = lambda mode:mode == __settling_mode__
is_listening_mode = lambda mode:mode == __listening_mode__

random.seed()

@threadify(__Q__)
def onBackground():
    global __mode__
    num = 0
    while(1):
        while (len(__events__) < __mode__['count']):
            if ((num % 10) == 0):
                print __mode__
            sleep(0.1)
            num += 1
	#####################################################################
	## The following is where we begin to train the automation support.
	#####################################################################
        while (len(__events__) == __mode__['count']):
            print '(+++).onBackground().1 --> %s' % (__mode__)
	    ##################################################################################
	    ## When we are settling we have not yet been trained so we go into listening mode.
	    ##################################################################################
            if (is_settling_mode(__mode__)):
                __mode__ = __listening_mode__
                misc.removeAll(__events__)
                print '(+++).onBackground().2 --> %s' % (__mode__)
                break
            elif (is_listening_mode(__mode__)):
                print '(+++).onBackground().3 --> (playing)'
                for anEvent in __events__:
                    x,y = anEvent.Position
                    print '(+++).onBackground().4 --> (clicking) --> %s,%s for (%s)...' % (x,y,str(anEvent))
                    #issueClick(x-50, y)
		    issueClick(x+_x1, y+_y1)
                    sleep(1)
                    #issueClick(x+30, y+5)
		    issueClick(x+_x2, y+_y2)
                    #secs = random.randrange(30,600)
		    secs = random.randrange(_secs1,_secs2)
                    print '(+++).onBackground().5 --> random sleep %s secs...' % (secs)
                    sleep(secs)
            sleep(1)
    
def sleep(secs):
    time.sleep(secs)

def onHandleClick(event):
    global __mode__, __is_using_target_window__, __target_window_hwnd__, __target_window_pid__
    if (__is_using_target_window__):
	anAction = __actions__.next()
        print '(+++).onHandleClick().0 --> (%s) --> %s, %s, %s, %s' % (anAction,event.Position,len(__events__),__mode__['count'],event.__dict__)
	__events__.append(event)
	if (__is_browser_address_bar__(anAction)):
	    print '(2)'
	elif (__is_login_username__(anAction)):
	    print '(3)'
	elif (__is_login_password__(anAction)):
	    print '(4)'
    else:
        __is_using_target_window__ = str(event.__dict__['WindowName']).find(__target_window_name__) > -1
        if (__is_using_target_window__):
	    print '(+++).onHandleClick().5 --> __is_using_target_window__=%s' % (__is_using_target_window__)
            __target_window_hwnd__ = win32gui.GetForegroundWindow()
            _, __target_window_pid__ = win32process.GetWindowThreadProcessId(__target_window_hwnd__)
        print '(+++).onHandleClick().6 --> %s, %s, %s, %s' % (event.Position,len(__events__),__mode__['count'],event.__dict__)
    return True

def issueClick(x,y):
    shell.AppActivate(__target_window_pid__)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def issueKeystrokes(x,y):
    shell.AppActivate(__target_window_pid__)
    win32api.SetCursorPos((x,y))
    win32api.keybd_event()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

if (__name__ == '__main__'):
    print 'BEGIN:'
    shell = win32com.client.Dispatch("WScript.Shell")
    onBackground()
    hm = pyHook.HookManager()
    hm.SubscribeMouseAllButtonsDown(onHandleClick)
    hm.HookMouse()
    pythoncom.PumpMessages()
    hm.UnhookMouse()
    print 'END !!!'
