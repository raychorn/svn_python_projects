import pyHook
import pythoncom
import time
import win32api, win32con, win32gui
import win32process
import win32com.client
import random

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
def onBackground():
    global __mode__
    num = 0
    while(1):
        while (len(__events__) < __mode__['count']):
            if ((num % 10) == 0):
                print __mode__
            sleep(0.1)
            num += 1
        while (len(__events__) == __mode__['count']):
            print '(+++).onBackground().1 --> %s' % (__mode__)
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
                    click(x-50, y)
                    sleep(1)
                    click(x+30, y+5)
                    secs = random.randrange(30,600)
                    print '(+++).onBackground().5 --> random sleep %s secs...' % (secs)
                    sleep(secs)
            sleep(1)
    
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

print 'BEGIN:'
shell = win32com.client.Dispatch("WScript.Shell")
onBackground()
hm = pyHook.HookManager()
hm.SubscribeMouseAllButtonsDown(onclick)
hm.HookMouse()
pythoncom.PumpMessages()
hm.UnhookMouse()
print 'END !!!'
