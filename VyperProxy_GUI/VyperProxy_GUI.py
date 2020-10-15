import wx
from wx.lib.wordwrap import wordwrap

import string

import os, sys
import time
import traceback

from vyperlogix import oodb

from vyperlogix.hash import lists

from vyperlogix.daemon.daemon import Log

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.misc import threadpool

from vyperlogix.misc import ObjectTypeName

from vyperlogix.sf.hostify import hostify

from vyperlogix.wx.PopUpDialog import wx_PopUp_Dialog

from wx.lib.wordwrap import wordwrap

from VyperProxy_version import ProductVersion
from VyperProxy_version import explain_version

_current_version = ProductVersion.community_version

is_checkbox_value_true = lambda value:str(value).lower() in ['true','1','yes','ok']

__version__ = '1.0.0.0'
s_productName = 'Vyper-Proxy'
__productName__ = '%s %s v%s' % (s_productName,explain_version(_current_version),__version__)

_info_Copyright = "(c). Copyright %s, Vyper Logix Corp." % (_utils.timeStampLocalTime(format=_utils.formatDate_YYYY()))

_info_site_address = 'www.vyperlogix.com'

__copyright__ = """[**], All Rights Reserved.

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH 
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE 
AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL 
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION 
OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING 
OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF 
THIS SOFTWARE !

USE AT YOUR OWN RISK."""

__description__  = '''{{ PRODUCT_NAME }} is a high-powered HTTP 1.1 Proxy that serves the web content for 3 instances of any single HTTP 1.1 Web App such as but not limited to Django. 

{{ PRODUCT_NAME }} has been known to perform better than the Apache 2.2.8 Load Balancer when Apache is serving content for 3 Django Apps.

{{ PRODUCT_NAME }} has been known to make the Apache 2.2.8 Load Balancer perform 2x faster (2x more Requests Per Second) when Apache is serving content through {{ PRODUCT_NAME }} and {{ PRODUCT_NAME }} is configured with at-least 3 Proxies.
'''

__copyright__ = '  '.join(__copyright__.replace('[**]',_info_Copyright).split('\n'))

_developers = ["Mr. Python"]
_writers = ['Mr. Nelson', 'Mr. Bailey']
_artists = ['Mr. Simon']
_translators = ['Miss Sofie']

__ChangeLog__ = """
[*2a*]
(**) Version 1.0.0:
Initial Community Edition Release.
[*2b*]
"""

s = [l for l in __ChangeLog__.split('\n') if (l.find('(**) ') > -1)]
if (len(s) > 0):
    __version__ = s[0].split(':')[0].split()[-1]
else:
    __version__ = 'UNKNOWN'

assert __version__ != 'UNKNOWN', 'Oops, cannot determine the current version number for "%s".' % (s_productName)
__productName__ = '%s %s v%s' % (s_productName,explain_version(_current_version),__version__)

__ChangeLog__ = __ChangeLog__.replace('[*2a*]','%s %s %s' % ('='*5,'Begin','='*5)).replace('[*2b*]','%s %s   %s' % ('='*5,'End','='*5)).replace('(**) ','')

_isRunning = True

_thread_Q = threadpool.ThreadQueue(100)

ID_ICON_TIMER = wx.NewId()

class MyTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIconBar()

        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=1)
        self.Bind(wx.EVT_MENU, self.OnTaskBarDeactivate, id=2)
        #self.Bind(wx.EVT_MENU, self.OnTaskBarReset, id=3)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=4)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, 'Show')
        menu.Append(2, 'Hide')
        #menu.Append(3, 'Reset')
        menu.Append(4, 'Exit')
        return menu

    def OnTaskBarReset(self, event):
        self._refreshIcon()

    def OnTaskBarClose(self, event):
        self.frame.Close()

    def OnTaskBarActivate(self, event):
        if not self.frame.IsShown():
            self.frame.Show()

    def OnTaskBarDeactivate(self, event):
        if self.frame.IsShown():
            self.frame.Hide()

    def SetIconBar(self):
        '''Sets the icon bar hover text...'''
        import icon2
        self.SetIcon(wx.IconFromBitmap(icon2.geticon2Bitmap()))

class MainFrame(wx.App):
    def OnInit(self):
        import VyperProxy_Dialog
        self.__child_frame = VyperProxy_Dialog.Dialog(None, title=__productName__, notifyStatusBar=self.notifyStatusBar)
        self.__child_frame.Center(wx.BOTH)
        self.__child_frame.Show(True)
        self.SetTopWindow(self.__child_frame)

        self.__child_frame.__taskbar_icon = MyTaskBarIcon(self)
        self.__child_frame.Centre()

        import icon2
        self.__child_frame.SetIcon(wx.IconFromBitmap(icon2.geticon2Bitmap()))

        from vyperlogix.wx import CustomStatusBar
        self.statusBar = CustomStatusBar.CustomStatusBar(self.__child_frame, None)
        self.__child_frame.SetStatusBar(self.statusBar)
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusWidths([-5, -3])

        # Menu Bar
        self.top_frame_menubar = wx.MenuBar()
        self.file_menu_item = wx.Menu()
        self.exit_menu_item = wx.MenuItem(self.file_menu_item, wx.NewId(), "Exit", "", wx.ITEM_NORMAL)

        self.file_menu_item.AppendItem(self.exit_menu_item)
        self.top_frame_menubar.Append(self.file_menu_item, "File")

        self.help_menu_item = wx.Menu()
        self.about_menu_item = wx.MenuItem(self.help_menu_item, wx.NewId(), "About", "", wx.ITEM_NORMAL)
        self.help_menu_item.AppendItem(self.about_menu_item)
        self.changelog_menu_item = wx.MenuItem(self.help_menu_item, wx.NewId(), "Change Log", "", wx.ITEM_NORMAL)
        self.help_menu_item.AppendItem(self.changelog_menu_item)
        self.top_frame_menubar.Append(self.help_menu_item, "Help")

        self.__child_frame.SetMenuBar(self.top_frame_menubar)
        # Menu Bar end

        self.Bind(wx.EVT_MENU, self.OnClose, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.onAbout, self.about_menu_item)
        self.Bind(wx.EVT_MENU, self.onChangeLog, self.changelog_menu_item)

        #self.Bind(wx.EVT_BUTTON, self.onProcess, self.__child_frame.btnProcess)

        self.__child_frame.Bind(wx.EVT_CLOSE, self.OnClose)

        self.__isAppClosed = False
        self.__isAppClosing = False

        self.__isDialogClosed = False

        self.__timer = None

        self.__callback_TimerHandler = None

        self.__child_frame.Bind(wx.EVT_TIMER, self.TimerHandler)

        return True
    
    def notifyStatusBar(self,message,seconds):
	if (message.find('not acceptable') > -1):
	    self.__child_frame.btnStartProxy.Disable()
	else:
	    self.__child_frame.btnStartProxy.Enable()
	self.statusBar.appendStatusBarNotification(message,seconds)

    def isDialogClosed():
        doc = "isDialogClosed"
        def fget(self):
            return self.__isDialogClosed
        return locals()
    isDialogClosed = property(**isDialogClosed())

    def progressTimerHandler(self):
        print 'self.count is "%s", self.number is "%s".' % (self.count,self.number)
        if (self.count == self.number):
            print 'self.callback_ProgressDialogDone()'
            self.callback_ProgressDialogDone()
            self.__isDialogClosed = True
        else:
            count = (float(self.count)/float(self.number))*100.0
            self.gauge_panel.count = count
            self.gauge_panel.update()

    def progressTimerHandlerWaitForThreads(self):
        from vyperlogix.misc import ObjectTypeName
        #print 'self.count is "%s", self.number is "%s".' % (self.count,self.number)
        if (self.count == self.number):
            #print '_thread_Q.join()'
            _thread_Q.join()
            self.callback_ProgressDialogDone()
            self.__isDialogClosed = True
        else:
            count = (float(self.count)/float(self.number))*100.0
            self.gauge_panel.count = count
            self.gauge_panel.update()

    def TimerHandler(self, event):
        if (callable(self.__callback_TimerHandler)):
            self.__callback_TimerHandler()

    def startTimer(self):
        self.__timer = wx.Timer(self.__child_frame)
        self.__timer.Start(250)

    def stopTimer(self):
        if (self.__timer):
            self.__timer.Stop()
            self.__timer = None

    def callback_ProgressDialogError(self):
        self.stopTimer()
        wx_PopUp_Dialog(parent=self.__child_frame,msg='There is nothing to do.',title='WARNING',styles=wx.ICON_WARNING)

    def callback_ProgressDialogDone(self):
        self.stopTimer()
        if (not self.isDialogClosed):
            self.gauge_panel.closeDialog()
            self.__isDialogClosed = True
            if (callable(self.__onProcessingDone)):
                try:
                    self.__onProcessingDone()
                finally:
                    self.__onProcessingDone = None

    def onProcess1(self, event):
        wx_PopUp_Dialog(parent=self.__child_frame,msg='Processing',title='INFORMATION',styles=wx.ICON_INFORMATION)

    def onProcessDone(self):
        wx_PopUp_Dialog(parent=self.__child_frame,msg='Processing Done !',title='INFORMATION',styles=wx.ICON_INFORMATION)

    @threadpool.threadify(_thread_Q)
    def doProcessing(self,frame):
        from vyperlogix.misc import ObjectTypeName
        n = 10
        try:
            if (n > 0):
                i = 1
                frame.number = n
                print >>sys.stdout, '%s :: frame.number is "%s".' % (ObjectTypeName.objectSignature(self),frame.number)
                for i in xrange(0,frame.number+1):
                    frame.count = i
                    wx.MilliSleep(1000)
        except Exception, details:
            _details = _utils.formattedException(details)
            print >>sys.stderr, _details

    def onProcess(self, event):
        from vyperlogix.wx.ProgressDialogPanel import ProgressDialogPanel
        self.gauge_panel = ProgressDialogPanel(self.__child_frame,title='Processing')
        self.gauge_panel.Centre(wx.BOTH)
        self.__isDialogClosed = False
        self.__callback_TimerHandler = self.progressTimerHandler
        self.__onProcessingDone = self.onProcessDone
        self.doProcessing(self)
        self.startTimer()

    def onChangeLog(self, event):
        from vyperlogix.wx.ChangeLogDialog import ChangeLogDialog
        self.__changeLog_dialog__ = ChangeLogDialog(None, 'ChangeLog for %s' % (s_productName))
        self.__changeLog_dialog__.tbChangeLog.SetValue(__ChangeLog__)
        self.__changeLog_dialog__.Show()
        self.__changeLog_dialog__.CenterOnParent()

    def onAbout(self, event):
        x = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X) / 2
        y = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        info = wx.AboutDialogInfo()
        info.Name = s_productName
        info.Version = __version__
        info.Copyright = _info_Copyright
        info.Description = wordwrap(
            __description__.replace('{{ PRODUCT_NAME }}',__productName__),
            x, wx.ClientDC(self.__child_frame))
        info.WebSite = ("http://%s" % (_info_site_address), "%s Home Page" % (__productName__))

        info.License = wordwrap(__copyright__, x, wx.ClientDC(self.__child_frame))

        import icon2
        info.SetIcon(wx.IconFromBitmap(icon2.geticon2Bitmap()))

        for n in _developers:
            info.AddDeveloper(n)
        for n in _writers:
            info.AddDocWriter(n)
        for n in _artists:
            info.AddArtist(n)
        for n in _translators:
            info.AddTranslator(n)

        popup = wx.AboutBox(info)

    def _OnClose(self):
        global _isRunning
        if (not self.__isAppClosing):
            self.__isAppClosing = True
            _isRunning = False
            self._OnExit()
            self.__child_frame.__taskbar_icon.RemoveIcon()
            self.__child_frame.__taskbar_icon.Destroy()
            del self.__child_frame.__taskbar_icon
            self.__child_frame.Destroy()
            del self.__child_frame
            self.__isAppClosed = True
            sys.exit()

    def OnClose(self, event):
        self._OnClose()

    def _OnExit(self):
        _thread_Q.join()
        if (not _isBeingDebugged):
            sys.stdout.close()
        sys.stderr.close()

    def OnExit(self):
        if (not self.__isAppClosed):
            self._OnClose()
        self._onExit()
        del self
        sys.exit()

    def Close(self):
        self.OnExit()

    def IsShown(self):
        return self.__child_frame.IsShown()

    def Show(self):
        self.__child_frame.Show()

    def Hide(self):
        self.__child_frame.Hide()

def main(argv=None):
    global _data_path

    if argv is None:
        argv = sys.argv

    _data_path = _utils.appDataFolder(prefix=_utils.getProgramName())
    _utils._makeDirs(_data_path)

    _log_path = os.path.dirname(sys.argv[0])

    if (not _isBeingDebugged):
        _stdOut = open(os.sep.join([_log_path,'stdout.txt']),'w')
        sys.stdout = Log(_stdOut)

    _stdErr = open(os.sep.join([_log_path,'stderr.txt']),'w')
    sys.stderr = Log(_stdErr)

    try:
        app = MainFrame(0)
        app.MainLoop()
    except Exception, exception:
        type, value, stack = sys.exc_info()
        formattedBacktrace = ''.join(traceback.format_exception(type, value, stack, 5))
        wx_PopUp_Dialog(parent=None,msg='An unexpected problem occurred:\n%s' % (formattedBacktrace),title='FATAL ERROR',styles=wx.ICON_ERROR)

def exception_callback(sections):
    _msg = 'EXCEPTION Causing Abend.\n%s' % '\n'.join(sections)
    print >>sys.stdout, _msg
    print >>sys.stderr, _msg
    sys.exit(1)

if __name__ == '__main__':
    _isBeingDebugged = _utils.isBeingDebugged

    if (not _isBeingDebugged):
        from vyperlogix.handlers.ExceptionHandler import *
        excp = ExceptionHandler()
        excp.callback = exception_callback

    from vyperlogix.misc._psyco import *
    importPsycoIfPossible(func=main,isVerbose=True)

    main()
