#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#    DrPython is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#GetKey Dialog

import drShortcuts
import wx

class drGetTextCtrl(wx.TextCtrl):
    def __init__(self, parent, ignorestring, grandparent):
        #Bug-Report With Fix, Christian Daven.
        wx.TextCtrl.__init__(self, parent, -1, "Hit A Key", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_PROCESS_TAB|wx.TE_PROCESS_ENTER)

        self.ancestor = grandparent

        self.valuestring = ''

        self.allowControl = not (ignorestring.find("Control") > -1)
        self.allowShift = not (ignorestring.find("Shift") > -1)
        self.allowMeta = not (ignorestring.find("Meta") > -1)
        self.allowAlt = not (ignorestring.find("Alt") > -1)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def GetValue(self):
        return self.valuestring

    def OnKeyDown(self, event):
        keystr = ""
        keycode = event.GetKeyCode()
        if (keycode == wx.WXK_CONTROL) or (keycode == 309) or (keycode == wx.WXK_SHIFT):
            return
        if event.ControlDown() and self.allowControl:
            keystr = "Control"
        if event.ShiftDown() and self.allowShift:
            keystr = keystr + "Shift"
        if event.AltDown() and self.allowAlt:
            keystr = keystr + "Alt"
        if event.MetaDown() and self.allowMeta:
            keystr = keystr + "Meta"
        keystr = keystr + str(keycode)
        self.SetValue(keystr)

    def SetValue(self, value):
        self.valuestring = value

        vstring = ''
        if drShortcuts.MatchControl(value):
            vstring += "Control + "
        if drShortcuts.MatchShift(value):
            vstring += "Shift + "
        if drShortcuts.MatchAlt(value):
            vstring += "Alt + "
        if drShortcuts.MatchMeta(value):
            vstring += "Meta + "

        vstring = vstring + drShortcuts.GetKeycodeStringFromShortcut(value)

        wx.TextCtrl.SetValue(self, vstring)

class drGetKeyDialog(wx.Dialog):

    def __init__(self, parent, ignorestring, grandparent):
        wx.Dialog.__init__(self, parent, -1, ("Hit A Key"), wx.DefaultPosition, wx.Size(200, 200), wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.txtKey = drGetTextCtrl(self, ignorestring, grandparent)
        self.theSizer.Add(self.txtKey, 1, wx.EXPAND)
        self.btnClear = wx.Button(self, 102, "Clear")
        self.btnClose = wx.Button(self, 101, "&Close")

        self.theSizer.Add(self.btnClear, 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnClose, 1, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.txtKey.SetFocus()

        self.Bind(wx.EVT_BUTTON, self.OnbtnClose, id=101)
        self.Bind(wx.EVT_BUTTON, self.OnbtnClear, id=102)

    def SetKeyString(self, keystring):
        if drShortcuts.GetKeycodeFromShortcut(keystring):
            self.txtKey.SetValue(keystring)
        else:
            self.txtKey.SetValue("Hit A Key")

    def GetKeyString(self):
        y = self.txtKey.GetValue()
        if y == "Hit A Key":
            return ""
        return y

    def OnbtnClear(self, event):
        self.txtKey.SetValue("Hit A Key")

    def OnbtnClose(self, event):
        self.EndModal(0)