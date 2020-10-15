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

# drListBox

# because on gtk, the keyboard key don't jump to the correspondent entry
#"""ListBox on Linux"""

import wx

class drListBox(wx.ListBox):
    def __init__(self, parent, *args, **kwargs):
        super(drListBox, self).__init__(parent, *args, **kwargs)
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_KEY_DOWN, self.OnKey)

    def OnKey(self, event):
        i0 = self.GetSelection()
        i1 = None
        p = 10 #todo: calculate steps; here six is a good value (on windows)
        key = event.GetKeyCode()
        #print('key %d.' % key)
        if key >= 32 and key <= 127:
            s = chr(key)
            #start from actual pos
            for i in range(i0 + 1, self.GetCount()):
                t = self.GetString(i)[0].upper()
                if t == s:
                    i1 = i
                    break
            if i1 == None: #try again from begining
                for i in range(i0):
                    t = self.GetString(i)[0].upper()
                    if t == s:
                        i1 = i
                        break

        elif key == wx.WXK_UP:
            i1 = i0 - 1
        elif key == wx.WXK_DOWN:
            i1 = i0 + 1
        elif key == wx.WXK_PRIOR:
            i1 = i0 - p
        elif key == wx.WXK_NEXT:
            i1 = i0 + p
        elif key == wx.WXK_HOME:
            i1 = 0
        elif key == wx.WXK_END:
            i1 = self.GetCount()
        if  i1 is None:
            return
        i1 = max(i1,0)
        i1 = min(i1, self.GetCount() - 1)
        self.SetSelection(i1)
        #self.lb1.EnsureVisible(i1) #Doesn't work on gtk
        #todo: compare with windows
        self.SetFirstItem(i1)
        #event.Skip()


if __name__ == '__main__':
    app = wx.App()
    win = wx.Frame(None, title="Hello drListBox Test!")
    w = drListBox(win, choices=["APython", "DPython", "DrPython", "DwxPython", "ZPython"])
    w.SetFocus()
    w.SetSelection(0)
    win.Show()
    app.MainLoop()

