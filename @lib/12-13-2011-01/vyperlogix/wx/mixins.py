import wx

from vyperlogix.wx.PopUpDialog import wx_PopUp_Dialog

import os, sys
import Queue
from vyperlogix.misc import _utils

from vyperlogix.misc import ObjectTypeName

class DisableMixin():
    def DisableChildren(self):
        for w in self.GetChildren():
            try:
                for ww in w.GetChildren():
                    try:
                        ww.Disable()
                    except Exception, details:
                        print >>sys.stderr, _utils.formattedException(details=details)
            except:
                try:
                    w.Disable()
                except Exception, details:
                    print >>sys.stderr, _utils.formattedException(details=details)

class EnableMixin():	
    def EnableChildren(self):
        for w in self.GetChildren():
            try:
                for ww in w.GetChildren():
                    try:
                        ww.Enable()
                    except Exception, details:
                        print >>sys.stderr, _utils.formattedException(details=details)
            except:
                try:
                    w.Enable()
                except Exception, details:
                    print >>sys.stderr, _utils.formattedException(details=details)

class ListCtrlSelections():
    def set_selection(self,value):
        pass

    def get_selected_items(self):
        """
	Gets the selected items for the list control.
	Selection is returned as a list of selected indices,
	low to high.
	"""

        selection = []

        # start at -1 to get the first selected item
        current = -1
        while True:
            next = self.GetNextSelected(current)
            if next == -1:
                return selection

            selection.append(next)
            current = next
        return selection

    def GetNextSelected(self, current):
        """Returns next selected item, or -1 when no more"""

        return self.GetNextItem(current, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

class ProgressDialogMixin():	
    def ProgressDialogMixin_init(self):
	self.__number = 0
	self.__count = 0
        self.__timer = None
	self.__isDialogClosed = False
	self.__onProcessingDone = None
	self.__callback_TimerHandler = None
	self.__onProcessingDone = None
	self.__gauge_panel = None
	self.__thread_Q = None
	self.__timer_end_condition = lambda :True
	self.__callback_progressDialog_updated = None
	
	print >>sys.stdout, ObjectTypeName.objectSignature(self)

    def timer_end_condition():
        doc = "timer_end_condition"
        def fget(self):
            return self.__timer_end_condition
        def fset(self, timer_end_condition):
	    if (callable(timer_end_condition)):
		self.__timer_end_condition = timer_end_condition
        return locals()
    timer_end_condition = property(**timer_end_condition())
    
    def thread_Q():
        doc = "thread_Q"
        def fget(self):
            return self.__thread_Q
        def fset(self, thread_Q):
            self.__thread_Q = thread_Q
        return locals()
    thread_Q = property(**thread_Q())
    
    def gauge_panel():
        doc = "gauge_panel"
        def fget(self):
            return self.__gauge_panel
        def fset(self, gauge_panel):
            self.__gauge_panel = gauge_panel
	    self.__isDialogClosed = False
        return locals()
    gauge_panel = property(**gauge_panel())
    
    def number():
        doc = "number"
        def fget(self):
            return self.__number
        def fset(self, number):
            self.__number = number
	    print >> self.log, '%s :: number is "%d".' % (ObjectTypeName.objectSignature(self),number)
        return locals()
    number = property(**number())
    
    def count():
        doc = "count"
        def fget(self):
            return self.__count
        def fset(self, count):
            self.__count = count
	    print >> self.log, '%s :: count is "%d".' % (ObjectTypeName.objectSignature(self),count)
        return locals()
    count = property(**count())
    
    def isDialogClosed():
        doc = "isDialogClosed"
        def fget(self):
            return self.__isDialogClosed
        return locals()
    isDialogClosed = property(**isDialogClosed())
    
    def __callback_ProgressDialogDone(self):
	self.__stopTimer()
	if (not self.isDialogClosed):
	    try:
		self.gauge_panel.closeDialog()
	    except Exception, details:
		info_string = _utils.formattedException(details=details)
		print >> self.log, info_string
	    finally:
		self.__isDialogClosed = True
		if (callable(self.__onProcessingDone)):
		    try:
			self.__onProcessingDone()
		    except Exception, details:
			info_string = _utils.formattedException(details=details)
			print >> self.log, info_string
		    finally:
			self.__onProcessingDone = None
	    
    def __progressTimerHandler(self):
	if (self.timer_end_condition()) and ((self.count + self.number) > 0) and (self.count == self.number):
	    if (self.thread_Q is not None):
		print >>self.log, '_thread_Q.join()'
		_thread_Q.join()
	    self.__callback_ProgressDialogDone()
	else:
	    if (self.number != 0):
		count = (float(self.count)/float(self.number))*100.0
		self.gauge_panel.count = count
		self.gauge_panel.update()
		if (callable(self.__callback_progressDialog_updated)):
		    try:
			self.__callback_progressDialog_updated()
		    except Exception, details:
			info_string = _utils.formattedException(details=details)
			print >> self.log, info_string

    def __TimerHandler(self, event):
	if (callable(self.__callback_TimerHandler)):
	    self.__callback_TimerHandler()
	
    def startProgressDialog(self,wxParent,title='',callback_progressDialog_updated=None,callback_onProcessingDone=None,callback_timer_end_condition=None):
	'''wxParent is the Frame or Panel object instance to which the timer is bound.'''
	self.ProgressDialogMixin_init()
	from vyperlogix.wx.ProgressDialogPanel import ProgressDialogPanel
	self.gauge_panel = ProgressDialogPanel(wxParent,title=title)
	self.gauge_panel.Centre(wx.BOTH)
	try:
	    wxParent.Bind(wx.EVT_TIMER, self.__TimerHandler)
	    self.__timer = wx.Timer(wxParent)
	    self.__timer.Start(250)
	    self.__callback_TimerHandler = self.__progressTimerHandler
	    if (callable(callback_progressDialog_updated)):
		self.__callback_progressDialog_updated = callback_progressDialog_updated
	    if (callable(callback_onProcessingDone)):
		self.__onProcessingDone = callback_onProcessingDone
	    if (callable(callback_timer_end_condition)):
		self.timer_end_condition = callback_timer_end_condition
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >> self.log, info_string
    
    def __stopTimer(self):
        if (self.__timer):
            self.__timer.Stop()
	    self.__timer = None
    
class MessageQ_Mixin():
    def MessageQ_Mixin_init(self):
        self.__message_Q__ = Queue.Queue(100)
	self.isMessageQ_Empty = lambda :self.isMessageQEmpty

	print >>sys.stdout, ObjectTypeName.objectSignature(self)
	
    def messageQ():
        doc = "messageQ"
        def fget(self):
            return self.__message_Q__
        def fset(self, messageQ_size):
	    try:
		del self.__message_Q__
	    finally:
		self.__message_Q__ = Queue.Queue(messageQ_size)
        return locals()
    messageQ = property(**messageQ())
    
    def isMessageQEmpty():
        doc = "isMessageQEmpty"
        def fget(self):
            return self.messageQ.empty
        return locals()
    isMessageQEmpty = property(**isMessageQEmpty())
    
    def append_to_message_Q(self,msg):
	self.messageQ.put(msg,timeout=30)
	
    def process_message_Q(self):
	if (not self.messageQ.empty()):
	    msg = self.messageQ.get(timeout=5)
	    try:
		print >>self.log, msg
	    except Exception, details:
		info_string = _utils.formattedException(details=details)
		print >> sys.stderr, info_string
	    self.messageQ.task_done()
    
class SalesForceLogin_Mixin():
    def create_login_dialog(self,parent,title='Login to SalesForce',callback_onProcess=None,callback_onClose=None):
	self.__parent__ = parent
	self.__callback_onProcess = callback_onProcess
	self.__callback_onClose = callback_onClose
	from vyperlogix.wx.SalesForceLogin import SalesForceLogin
	self.__login_dialog__ = SalesForceLogin(None, title, onProcess_callback=self.__onProcess_LoginDialog, onClose_callback=self.__OnClose_LoginDialog)

    def login_dialog():
        doc = "login_dialog"
        def fget(self):
            return self.__login_dialog__
        return locals()
    login_dialog = property(**login_dialog())
    
    def parent():
        doc = "parent"
        def fget(self):
            return self.__parent__
        return locals()
    parent = property(**parent())
    
    def __onProcess_LoginDialog(self):
	try:
	    if (len(self.__login_dialog__.sf_login_model.lastError) > 0):
		self.__login_dialog__.EnableChildren()
		print >>sys.stderr, self.login_dialog.sf_login_model.lastError
		wx_PopUp_Dialog(parent=self.parent,msg=self.login_dialog.sf_login_model.lastError,title='ERROR',styles=wx.ICON_ERROR)
	    else:
		if (callable(self.__callback_onProcess)):
		    try:
			self.__callback_onProcess()
		    except Exception, details:
			_details = _utils.formattedException(details)
			print >>sys.stderr, _details
			wx_PopUp_Dialog(parent=self.parent,msg=_details,title='ERROR',styles=wx.ICON_INFORMATION | wx.CANCEL)
	except Exception, details:
	    _details = _utils.formattedException(details)
	    print >>sys.stderr, _details
	    wx_PopUp_Dialog(parent=self.parent,msg=_details,title='ERROR',styles=wx.ICON_INFORMATION | wx.CANCEL)
	
    def _close_LoginDialog(self):
	if (self.login_dialog is not None):
	    self.login_dialog.onHide()
	    self.parent.Hide()
	    self.parent.Show()
	    self.parent.Iconize(False)
    
    def __OnClose_LoginDialog(self):
	if (self.login_dialog is not None):
	    self._close_LoginDialog()
	    if (callable(self.__callback_onClose)):
		try:
		    self.__callback_onClose()
		except Exception, details:
		    _details = _utils.formattedException(details)
		    print >>sys.stderr, _details
		    wx_PopUp_Dialog(parent=self.parent,msg=_details,title='ERROR',styles=wx.ICON_INFORMATION | wx.CANCEL)
	    
class ChangeLogDialog_Mixin():
    def ChangeLog_title():
        doc = "ChangeLog_title, set this property with the s_productName"
        def fget(self):
	    val = ''
	    try:
		val = self.__ChangeLog_title__
	    except:
		val = self.__ChangeLog_title__ = ''
            return val
        def fset(self, s_productName):
	    self.__ChangeLog_title__ = 'ChangeLog for %s' % (s_productName)
        return locals()
    ChangeLog_title = property(**ChangeLog_title())
    
    def ChangeLog():
        doc = "ChangeLog, set this property with the __ChangeLog__ that is generally a global."
        def fget(self):
	    val = ''
	    try:
		val = self.__ChangeLog__
	    except:
		val = self.__ChangeLog__ = ''
            return val
        def fset(self, ChangeLog):
	    self.__ChangeLog__ = ChangeLog
        return locals()
    ChangeLog = property(**ChangeLog())
    
    def ChangeLog_binding():
        doc = "ChangeLog_binding self.ChangeLog_binding = self.changelog_menu_item"
        def fset(self, changelog_menu_item):
	    self.Bind(wx.EVT_MENU, self.onChangeLog, changelog_menu_item)
        return locals()
    ChangeLog_binding = property(**ChangeLog_binding())
    
    def onChangeLog(self, event):
	from vyperlogix.wx.ChangeLogDialog import ChangeLogDialog
	self.__changeLog_dialog__ = ChangeLogDialog(None, self.ChangeLog_title)
	self.__changeLog_dialog__.tbChangeLog.SetValue(self.ChangeLog)
	self.__changeLog_dialog__.Show()
	self.__changeLog_dialog__.CenterOnParent()
