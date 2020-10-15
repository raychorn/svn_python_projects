import os,sys
import time

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')
if (not isUsingWindows):
    print 'WARNING: You CANNOT use pywinauto unless you are using the Windows OS... Please try the installation again.'
    os._exit(1)

#################################################################################################################################################
## See also: http://pywinauto.googlecode.com/hg/pywinauto/docs/index.html#installation
#################################################################################################################################################
from pywinauto import __version__
if (__version__ == '0.4.0'):
    try:
	from pywinauto import application
    except:
	print 'WARNING: You did not install the correct version of something pywinauto requires... Please try the installation again.'
	os._exit(1)
    from pywinauto import findwindows
else:
    print 'WARNING: You did not install the correct version of pywinauto... Please try the installation again.'
    os._exit(1)

import win32api, win32con, win32gui
import win32process
import win32com.client

import pyHook
import pythoncom

__url__ = 'https://lam-933.dev.core.rackspace.com '

__windowName__ = u'Mozilla Firefox Start Page - Mozilla Firefox'

__coreLogin__ = u'CORE:.*Login'
__coreWelcome__ = u'CORE:.*Welcome'

__coreUsername__ = 'melissa.biles'
__corePassword__ = 'qwerty'

shell = win32com.client.Dispatch("WScript.Shell")

def findWindowUsing(regex):
    n = 0
    while (1):
        try:
            app = application.Application().connect_(title_re=regex)
            window = app.window_(title_re=regex)
            w_handle = findwindows.find_windows(title_re=regex, class_name='MozillaWindowClass')[0]
            break
        except Exception, ex:
            pass
        n += 1
        if (n > 4):
            print 'WARNING: Seems someone forgot to logout of Core... So please do so now.'
            return None,None
        time.sleep(1)
    return window,w_handle

def onHandleClick(event):
    print '(+++).onHandleClick().1 --> event=%s' % (event.__dict__)
    __is_using_target_window__ = str(event.__dict__['WindowName']).find('CORE:') > -1
    if (__is_using_target_window__):
	print '(+++).onHandleClick().1 --> __is_using_target_window__=%s' % (__is_using_target_window__)
	__target_window_hwnd__ = win32gui.GetForegroundWindow()
	_, __target_window_pid__ = win32process.GetWindowThreadProcessId(__target_window_hwnd__)
    print '(+++).onHandleClick().2 --> %s, %s, %s, %s' % (event.Position,len(__events__),__mode__['count'],event.__dict__)
    return True

def issueMouseClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

pwa_app = application.Application()
fpath = 'C:/Program Files (x86)/Mozilla Firefox/firefox.exe'
if (os.path.exists(fpath)):
    app = application.Application().start_(r"%s %s"%(fpath,__url__))
    mozilla,w_handle = findWindowUsing(__coreLogin__)
    if (mozilla is not None) and (w_handle is not None):
        window = pwa_app.window_(handle=w_handle)
        print 'w_handle=%s' % (w_handle)
        _, __target_window_pid__ = win32process.GetWindowThreadProcessId(w_handle)
        shell.AppActivate(__target_window_pid__)
        window.SetFocus()
        mozilla.TypeKeys('^A')
        time.sleep(1)
        mozilla.TypeKeys(__coreUsername__)
        time.sleep(1)
        mozilla.TypeKeys('{TAB}')
        time.sleep(1)
        mozilla.TypeKeys(__corePassword__)
        time.sleep(1)
        mozilla.TypeKeys('{ENTER}')
        time.sleep(1)

    mozilla,w_handle = findWindowUsing(__coreWelcome__)
    if (mozilla is not None) and (w_handle is not None):
        window = pwa_app.window_(handle=w_handle)
        print 'w_handle=%s' % (w_handle)
        _, __target_window_pid__ = win32process.GetWindowThreadProcessId(w_handle)
    
        #### Select the Main Menu for Core ####
        mozilla.TypeKeys('{ESC}')
        time.sleep(1)
        mozilla.TypeKeys('{TAB}')
        time.sleep(1)
        mozilla.TypeKeys('{TAB}')
        time.sleep(1)
        #### Select the CORE Menu for Core ####
        mozilla.TypeKeys('{ENTER}')
        time.sleep(1)
        
        #################################################################################
	## The following block of code is useful when you need to figure-out the 
	## position of a mouse click event since you cannot always use TAB navigation
	## to move the focus around the Core content other than certain selected areas.
	#################################################################################
        if (0):
            print 'INFO: Select the menu item you want to choose later on...'
            hm = pyHook.HookManager()
            hm.SubscribeMouseAllButtonsDown(onHandleClick)
            hm.HookMouse()
            pythoncom.PumpMessages()
            hm.UnhookMouse()
	
	issueMouseClick(161,355)  # This clicks on the MaintCal Admin menu item - this may seem a bit crude for now but it works for me.
    else:
        print 'WARNING: hey, are you sure Core is able to run at-all ?!?'
else:
    print 'WARNING: Cannot find "%s".' % (fpath)
