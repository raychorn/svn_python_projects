import wx
import wx.calendar
import  wx.lib.mixins.listctrl  as  listmix
import  wx.lib.rcsizer  as rcs

import sys
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.misc import threadpool

from vyperlogix.wx import mixins

from vyperlogix.hash import lists

import unicodedata

__utility_Q__ = threadpool.ThreadQueue(2)

class SalesForceLogin(wx.Dialog,mixins.EnableMixin,mixins.DisableMixin):	
    def __init__(self, parent, title, onProcess_callback=None, onClose_callback=None, callback_is_running_securely_for_developers=None):
        self.__onProcess_callback = onProcess_callback
        self.__onClose_callback = onClose_callback
	
        from vyperlogix.wx.pyax import SalesForceLoginModel
        self.__sf_login_model__ = SalesForceLoginModel.SalesForceLoginModel(callback_developers_check=callback_is_running_securely_for_developers)
        isStaging = self.__sf_login_model__.isStaging
	
        wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, (300, 160), style=wx.SYSTEM_MENU | wx.CAPTION | wx.STAY_ON_TOP) # | wx.CLOSE_BOX | wx.RESIZE_BORDER | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX
        self.panel = wx.Panel(self, -1)

        self.labelUsername = wx.StaticText(self.panel, -1, 'UserName:', (16,10), (65, 17))
        self.labelUsername.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.labelUsername.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.textUsername = wx.TextCtrl(self.panel, -1, 'username', (96,8), size=(185, 20))
        self.textUsername.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.textUsername.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.textUsername.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.labelPassword = wx.StaticText(self.panel, -1, 'Password:', (16,32), (65, 17))
        self.labelPassword.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.labelPassword.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.textPassword = wx.TextCtrl(self.panel, -1, 'password', (96,32), size=(185, 20), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.textPassword.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.textPassword.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.textPassword.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	servers = []
	for k,v in self.__sf_login_model__.sfServers.iteritems():
	    servers += v if (misc.isList(v)) else [v]
        self.cbServerEndPoints = wx.ComboBox(self.panel, -1, 'combobox for Server End-Points', (164,136), (180, 21), servers, style=wx.CB_READONLY | wx.CB_SORT)
        self.cbServerEndPoints.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.cbServerEndPoints.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.cbServerEndPoints.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
	self.cbServerEndPoints.SetSelection(0)

        self.textEndPoint = wx.TextCtrl(self.panel, -1, 'endpoint', (96,8), size=(300, 20))
        self.textEndPoint.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.textEndPoint.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.textEndPoint.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
	self.textEndPoint.SetValue(self.sf_login_model.get_endpoint(self.cbServerEndPoints.GetValue()))

        self.btnLogin = wx.Button(self.panel, -1, 'Login', (24,96), (75, 23))
        self.btnLogin.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.btnLogin.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.btnCancel = wx.Button(self.panel, -1, 'Cancel', (120,96), (75, 23))
        self.btnCancel.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.btnCancel.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.boxRadioButtons = wx.StaticBox(self.panel, -1, "SalesForce End-Points" )
        self.boxRadioButtons.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.boxRadioButtons.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        import salesforce_icon
        self.SetIcon(wx.IconFromBitmap(salesforce_icon.getsalesforce_iconBitmap()))

        vbox = wx.BoxSizer(wx.VERTICAL)

        hboxes = []

        box1 = wx.StaticBoxSizer( self.boxRadioButtons, wx.VERTICAL )
        sizer = rcs.RowColSizer()

	sizer.Add(self.cbServerEndPoints, row=0, col=1)
	sizer.Add(self.textEndPoint, row=1, col=1)

        box1.Add(sizer, 0, wx.ALIGN_LEFT | wx.ALL, 5 )

        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hboxes[-1].Add(self.labelUsername, 0, wx.RIGHT, 8)
        hboxes[-1].Add((5, -1))
        hboxes[-1].Add(self.textUsername, 1)
        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 1))

        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hboxes[-1].Add(self.labelPassword, 0, wx.RIGHT, 8)
        hboxes[-1].Add((5, -1))
        hboxes[-1].Add(self.textPassword, 1)
        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 1))

        vbox.Add(box1, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        vbox.Add((-1, 1))

        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hboxes[-1].Add(self.btnLogin, 0, wx.RIGHT, 8)
        hboxes[-1].Add((5, -1))
        hboxes[-1].Add(self.btnCancel, 1)
        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 1))

        self.panel.SetSizer(vbox)

        x = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        y = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self.SetSizeHints(300,160,x,y)
        vbox.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.onProcess, self.btnLogin)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.btnCancel)
	
        self.Bind(wx.EVT_COMBOBOX, self.OnSelectedServerEndPoints, self.cbServerEndPoints)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_TEXT_ENTER, self.onProcess, self.textPassword)

    def sf_login_model():
        doc = "sf_login_model"
        def fget(self):
            return self.__sf_login_model__
        return locals()
    sf_login_model = property(**sf_login_model())
    
    @threadpool.threadify(__utility_Q__)
    def onHide(self):
	while (self.IsShown()):
	    while (self.IsShown()):
		self.Hide()
	    print '%s.1' % (ObjectTypeName.objectSignature(self))
	    wx.MilliSleep(1000)

    def OnSelectedServerEndPoints(self, event):
	value = event.ClientData.GetValue()
	toks = self.textEndPoint.GetValue().split('/')
	i = 0
	if (toks[0].lower().find('http') > -1):
	    i = 2
	toks[i] = value
	new_value = '/'.join(toks)
	self.textEndPoint.SetValue(new_value)
    
    def onProcess(self, event):
	self.DisableChildren()
	self.sf_login_model.username = self.textUsername.GetValue()
	self.sf_login_model.password = self.textPassword.GetValue()
	self.sf_login_model.perform_login(self.textEndPoint.GetValue())
        if (callable(self.__onProcess_callback)):
            try:
                self.__onProcess_callback()
            except Exception, details:
                print >>sys.stderr, _utils.formattedException(details=details)

    def OnClose(self, event):
        if (callable(self.__onClose_callback)):
            try:
                self.__onClose_callback()
            except Exception, details:
                print >>sys.stderr, _utils.formattedException(details=details)

