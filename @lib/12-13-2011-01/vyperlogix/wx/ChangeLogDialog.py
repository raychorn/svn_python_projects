import wx
import wx.calendar
import  wx.lib.mixins.listctrl  as  listmix

import sys
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.wx import mixins

from vyperlogix.hash import lists

import unicodedata

class ChangeLogDialog(wx.Dialog):	
    def __init__(self, parent, title='Change Log'):
        wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, (700, 500), style=wx.CLOSE_BOX | wx.CAPTION | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.SYSTEM_MENU)
        self.panel = wx.Panel(self, -1)

        self.tbChangeLog = wx.TextCtrl(self.panel, -1, 'textbox', (0,0), size=(670, 420),style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.tbChangeLog.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.tbChangeLog.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.tbChangeLog.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.btnClose = wx.Button(self.panel, -1, 'Close', (0,24), (75, 23))
        self.btnClose.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.btnClose.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        import script_16x16
        self.SetIcon(wx.IconFromBitmap(script_16x16.getscript_16x16Bitmap()))

        self.Bind(wx.EVT_BUTTON, self.OnClose, self.btnClose)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hboxes = []

        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hboxes[-1].Add(self.tbChangeLog, 0, wx.EXPAND, 8)
        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 1))

        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))
        hboxes[-1].Add(self.btnClose, 0, wx.EXPAND, 8)
        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 1))

        self.panel.SetSizer(vbox)

        x = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        y = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        
        self.SetSizeHints(700,500,x,y)
        vbox.Fit(self)

    def OnClose(self, event):
	self.Destroy()
	del self

