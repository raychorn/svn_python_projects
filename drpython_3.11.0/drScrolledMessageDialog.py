#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   DrPython is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#Scrolled Message Dialog

import wx
import sys, traceback

class ScrolledMessageDialog(wx.Dialog):
    def __init__(self, parent, message, title, position = wx.DefaultPosition, size = wx.Size(400, 300)):
        wx.Dialog.__init__(self, parent, -1, title, position, size, wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.ID_CLOSE = 101

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.cmdSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btnClose = wx.Button(self, self.ID_CLOSE, "&Close")
        self.cmdSizer.Add(self.btnClose, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.btnClose.SetDefault()

        slist = traceback.format_tb(sys.exc_info()[2])
        l = len(slist)
        if l > 0:
            x = 0
            rstring = ""
            while x < l:
                rstring = rstring + slist[x]
                x = x + 1
            tracebackstring = "Traceback (most recent call last):\n" + rstring \
            + str(sys.exc_info()[0]).lstrip("exceptions.") + ": " + str(sys.exc_info()[1])
            message = message + "\n\n\n" + tracebackstring

        self.txtMessage = wx.TextCtrl(self, -1, message, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE | wx.TE_READONLY)
        #[ 1357735 ] Change from Text to Html Messages; don't know wheter to apply or not
        #self.txtMessage = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO)
        #self.txtMessage.AppendToPage('<body bgcolor="#FFFFF0">'+message+'</body>')
        
        self.theSizer.Add(self.txtMessage, 9, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.cmdSizer, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_BUTTON,  self.OnbtnClose, id=self.ID_CLOSE)

        self.btnClose.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnbtnClose(self, event):
        self.Close(1)

    def OnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close(1)

def ShowMessage(parent, message, title, position = wx.DefaultPosition, size = wx.Size(400, 300)):
    d = ScrolledMessageDialog(parent, message, title, position, size)
    d.ShowModal()
    d.Destroy()