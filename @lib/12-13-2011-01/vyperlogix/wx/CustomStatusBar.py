import time

import wx

_status_bar_notification = [] # contains tuples where t[0] is the message and t[-1] is the number of seconds or -1 for longer.
last_status_bar_notification = '' # contains the last message that was on the status bar - gets displayed when no other message is available.

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent, log, isDebug=False):
        wx.StatusBar.__init__(self, parent, -1)

        self.SetFieldsCount(3)
	
	self.__isDebug = isDebug if (isinstance(isDebug, bool)) else False

        self.SetStatusWidths([-4, -1, -2])
        self.log = log
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.SetStatusText("Online", 0)

        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

    def isDebug():
        doc = "isDebug"
        def fget(self):
            return self.__isDebug
        def fset(self, isDebug):
            self.__isDebug = isDebug
        return locals()
    isDebug = property(**isDebug())
    
    def appendStatusBarNotification(self,message,seconds):
	_status_bar_notification.append((message,seconds))
	
    def Notify(self):
	global _status_bar_notification, last_status_bar_notification
        
        t = time.localtime(time.time())
        st = time.strftime("%A %d-%b-%Y   %I:%M:%S %p", t)
        self.SetStatusText(st, self.GetFieldsCount()-1)
	st = (last_status_bar_notification,15)
	if (len(_status_bar_notification) > 0):
	    st = _status_bar_notification[0]
	    _status_bar_notification = _status_bar_notification[1:]
	    if (st[-1] == -1):
		st[-1] = 15
	    if (st[-1] > -1):
		i = st[-1]
		i -= 1
		if (i > 0):
		    st = (st[0],i)
		    _status_bar_notification.insert(0,st)
		    if (len(st[0]) > 0):
			last_status_bar_notification = st[0]
		    if (self.log):
			self.log.WriteText("tick...\n")
	if (self.isDebug):
	    print 'st=%s' % (str(st))
	self.SetStatusText(st[0], 0)

    def OnSize(self, evt):
        self.sizeChanged = True

    def OnIdle(self, evt):
        if self.sizeChanged:
            pass

