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

#Drag and Drop

import wx, wx.stc

#*******************************************************************************************************
#Submitted by Slim Amamou
#Modified by Daniel Pozmanter
#Modified again by Dan for 3.7.0
#   Reworked to add Text Drag and Drop Support
#   Thanks to Robin Dunn for the code.

class drDropTarget(wx.DropTarget):
    def __init__(self, window):
        wx.DropTarget.__init__(self)
        self.window = window.grandparent

        window.Bind(wx.stc.EVT_STC_START_DRAG, self.OnStartDrag, id=window.GetId())

        self.data = wx.DataObjectComposite()
        self.dtext = wx.TextDataObject()
        self.dfilename = wx.FileDataObject()
        self.data.Add(self.dtext, True)
        self.data.Add(self.dfilename)

        self.draginitiatedfromstc = False

        self.moddown = False

        self.SetDataObject(self.data)

    def DropFiles(self, filenames):
        filenames = map(lambda x: x.replace("\\", "/"), filenames)
        
        for fname in filenames:
            self.window.OpenOrSwitchToFile(fname)

    def DropText(self, text, point):
        if self.window.prefs.draganddropmode != 2:
            if self.draginitiatedfromstc:
                if ((self.window.prefs.draganddroptextmode == 0) and self.moddown) or \
                ((self.window.prefs.draganddroptextmode == 1) and (not self.moddown)):
                    self.window.txtDocument.SetSelectedText('')
            position = self.window.txtDocument.PositionFromPoint(point)
            self.window.txtDocument.InsertText(position, text)
            self.window.txtDocument.GotoPos(position+len(text))


    def OnDrop(self, x, y):
        if self.draginitiatedfromstc==1 and self.window.prefs.draganddropmode==2:
            return False
        else:
            return True
        
    def OnData(self, x, y, theData):
        self.GetData()
        if self.dtext.GetTextLength() > 1:
            self.DropText(self.dtext.GetText(), wx.Point(x, y))
            self.dtext.SetText('')
        else:
            self.DropFiles(self.dfilename.GetFilenames())

        self.draginitiatedfromstc = False

        return theData

    def OnStartDrag(self, event):
        self.draginitiatedfromstc = True

    def SetModifierDown(self, moddown):
        self.moddown = moddown