
# Created with FarPy GUIE v0.5.5

import wx
import wx.calendar
import  wx.lib.mixins.listctrl  as  listmix

import sys
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

from vyperlogix.wx.mixins import EnableMixin
from vyperlogix.wx.mixins import DisableMixin

import unicodedata

class Dialog(wx.Frame, EnableMixin, DisableMixin):	
    def __init__(self, parent, title='Dialog'):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, (700, 500), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        
        self.btnProcess = wx.Button(self.panel, -1, 'Submit', (24,216), (80, 30))
        self.btnProcess.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
        self.btnProcess.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.btnProcess.SetToolTip(wx.ToolTip('Click this button to begin the process.'))

        vbox = wx.BoxSizer(wx.VERTICAL)

        hboxes = []
        
        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.btnProcess, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        vbox2.Add((-1, 1))
        hboxes[-1].Add(vbox2, 1)

        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox.Add((-1, 1))

        self.panel.SetSizer(vbox)

        x = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        y = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self.SetSizeHints(700,500,x,y)
        vbox.Fit(self)
        
