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

#Menus

import os.path
import wx

class drMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)

        self.parent = parent
        self.bitmapdirectory = self.parent.programdirectory + "/bitmaps/16/"

    def Append(self, id, label, LaunchesDialog = False, AmpersandAt = -1, AbsoluteLabel=''):
        ''' Appends the item, any applicable bitmap, and also any keyboard shortcut. '''

        item = wx.MenuItem(self, id, self.parent.getmenulabel(label, LaunchesDialog, AmpersandAt, AbsoluteLabel))

        bitmap = self.bitmapdirectory + label + '.png'
        if os.path.exists(bitmap):
            item.SetBitmap(wx.BitmapFromImage(wx.Image(bitmap, wx.BITMAP_TYPE_PNG)))

        return self.AppendItem(item)
