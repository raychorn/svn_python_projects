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

#Prefs Dialog for File Dialog

import wx, wx.lib.dialogs
import drScrolledMessageDialog

#*******************************************************************************************************
class drEditTwoStringsDialog(wx.Dialog):
    def __init__(self, parent, label1, label2, title):
        wx.Dialog.__init__(self, parent, -1, title, wx.Point(50, 50), wx.Size(-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)

        self.txt1 = wx.TextCtrl(self, -1, '', size=(300, -1))
        self.txt2 = wx.TextCtrl(self, -1, '', size=(300, -1))

        self.btnCancel = wx.Button(self, 1, '&Cancel')
        self.btnOk = wx.Button(self, 2, '&Ok')

        self.theSizer = wx.FlexGridSizer(3, 2, 5, 10)

        self.theSizer.Add(wx.StaticText(self, -1, label1), 1, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, label2), 1, wx.EXPAND)
        self.theSizer.Add(self.txt1, 1, wx.SHAPED)
        self.theSizer.Add(self.txt2, 1, wx.SHAPED)
        self.theSizer.Add(self.btnCancel, 1, wx.SHAPED)
        self.theSizer.Add(self.btnOk, 1, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=2)

    def GetValues(self):
        return self.txt1.GetValue(), self.txt2.GetValue()

    def OnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnOk(self, event):
        self.EndModal(wx.ID_OK)

    def SetValues(self, value1, value2):
        self.txt1.SetValue(value1)
        self.txt2.SetValue(value2)

#*******************************************************************************************************

class drFilePrefsDialogBase(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, wx.Point(50, 50), wx.Size(-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)
        wx.Yield()

        self.parent = parent

        self.ID_ADD = 1003
        self.ID_REMOVE = 1004

        self.ID_CANCEL = 1005
        self.ID_OK = 1006

        self.ID_LIST = 1300

        self.ID_UP = 1111
        self.ID_DOWN = 2222

        self.btnUp = wx.Button(self, self.ID_UP, " Up ")
        self.btnAdd = wx.Button(self, self.ID_ADD, " Add ")
        self.btnRemove = wx.Button(self, self.ID_REMOVE, " Remove ")
        self.btnDown = wx.Button(self, self.ID_DOWN, " Down ")

        self.btnCancel = wx.Button(self, self.ID_CANCEL, "&Cancel")
        self.btnOk = wx.Button(self, self.ID_OK, "&Ok")

        self.lstItems = wx.ListView(self, self.ID_LIST, size=(500, 350), style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        self.items = []

        self.theSizer = wx.FlexGridSizer(4, 2, 5, 10)
        #self.theSizer = wx.BoxSizer(wx.VERTICAL)
        #self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.menubuttonSizer = wx.BoxSizer(wx.VERTICAL)
        #self.okcancelSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnAdd, 0, wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnUp, 0, wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnDown, 0, wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnRemove, 0, wx.SHAPED)

        self.theSizer.Add(self.menubuttonSizer, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.lstItems, 0,  wx.SHAPED | wx.ALIGN_CENTER)

        self.theSizer.Add(self.btnCancel, 0, wx.SHAPED | wx.ALIGN_LEFT)
        self.theSizer.Add(self.btnOk, 0, wx.SHAPED | wx.ALIGN_RIGHT)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON,  self.OnbtnUp, id=self.ID_UP)
        self.Bind(wx.EVT_BUTTON,  self.OnAdd, id=self.ID_ADD)
        self.Bind(wx.EVT_BUTTON,  self.OnRemove, id=self.ID_REMOVE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnDown, id=self.ID_DOWN)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnOk, id=self.ID_OK)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivate, id=self.ID_LIST)

    def OnActivate(self, event):
        sel = self.lstItems.GetFirstSelected()
        if sel == -1:
            return
        d = drEditTwoStringsDialog(self, self.dlabel1, self.dlabel2, 'Edit ' + self.dtitle)
        d.SetValues(self.lstItems.GetItemText(sel), self.lstItems.GetItem(sel, 1).GetText())
        answer = d.ShowModal()
        v = d.GetValues()
        d.Destroy()

        if answer == wx.ID_OK:
            y = self.lstItems.GetItemCount()
            self.lstItems.InsertStringItem(y, v[0])
            self.lstItems.SetStringItem(y, 1, v[1])

    def OnAdd(self, event):
        d = drEditTwoStringsDialog(self, self.dlabel1, self.dlabel2, 'Add ' + self.dtitle)
        answer = d.ShowModal()
        v = d.GetValues()
        d.Destroy()

        if answer == wx.ID_OK:
            y = self.lstItems.GetItemCount()
            self.lstItems.InsertStringItem(y, v[0])
            self.lstItems.SetStringItem(y, 1, v[1])

    def OnbtnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnbtnDown(self, event):
        sel = self.lstItems.GetFirstSelected()
        if sel < self.lstItems.GetItemCount()-1 and sel > -1:
            txt = self.lstItems.GetItemText(sel)
            value = self.lstItems.GetItem(sel, 1).GetText()
            self.lstItems.DeleteItem(sel)
            self.lstItems.Select(sel, False)
            self.lstItems.InsertStringItem(sel+1, txt)
            self.lstItems.SetStringItem(sel+1, 1, value)
            self.lstItems.Select(sel+1, True)

    def OnbtnOk(self, event):
        self.EndModal(wx.ID_OK)

    def OnbtnUp(self, event):
        sel = self.lstItems.GetFirstSelected()
        if sel > 0:
            txt = self.lstItems.GetItemText(sel)
            value = self.lstItems.GetItem(sel, 1).GetText()
            self.lstItems.DeleteItem(sel)
            self.lstItems.InsertStringItem(sel-1, txt)
            self.lstItems.SetStringItem(sel-1, 1, value)
            self.lstItems.Select(sel, False)
            self.lstItems.Select(sel-1, True)

    def OnRemove(self, event):
        sel = self.lstItems.GetFirstSelected()
        if sel == -1:
            drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Remove", "Mistake")
            return

        self.lstItems.DeleteItem(sel)
        if sel > 0:
            self.lstItems.Select(sel-1, True)

    def SetColumns(self, label1, label2):
        self.lstItems.InsertColumn(0, label1)
        self.lstItems.InsertColumn(1, label2)

        self.lstItems.SetColumnWidth(0, 250)
        self.lstItems.SetColumnWidth(1, 250)

    def SetDialog(self, label1, label2, title):
        self.dlabel1 = label1
        self.dlabel2 = label2
        self.dtitle= title

#*******************************************************************************************************

class drFilePrefsDialog(drFilePrefsDialogBase):
    def __init__(self, parent):
        drFilePrefsDialogBase.__init__(self, parent, 'Edit Wildcard')

        self.ancestor = parent.grandparent

        self.SetColumns('Label', 'File Pattern')

        self.SetDialog('Label:', 'File Pattern:', 'Wildcard Entry')

        self.txtConstant = wx.TextCtrl(self, -1, self.ancestor.prefs.constantwildcard, size=(500, -1))

        self.theSizer.Insert(2, wx.StaticText(self, -1, ' '), 1, wx.EXPAND)
        self.theSizer.Insert(3, wx.StaticText(self, -1, ' '), 1, wx.EXPAND)

        self.theSizer.Insert(4, wx.StaticText(self, -1, 'Constant Wildcard:'), 1, wx.EXPAND)
        self.theSizer.Insert(5, self.txtConstant, 0, wx.SHAPED)

        self.Fit()

        wcarray = self.ancestor.prefs.wildcard.split('|')

        l = len(wcarray) - 1

        x = 0
        while x < l:
            y = self.lstItems.GetItemCount()
            self.lstItems.InsertStringItem(y, wcarray[x])
            self.lstItems.SetStringItem(y, 1, wcarray[x+1])
            x += 2

    def GetConstantWildcard(self):
        return self.txtConstant.GetValue()

    def GetWildcard(self):
        l = self.lstItems.GetItemCount()
        if l < 1:
            return 'All Files (*)|*'
        wcstring = self.lstItems.GetItemText(0) + '|' + self.lstItems.GetItem(0, 1).GetText()
        x = 1
        while x < l:
            wcstring += '|' + self.lstItems.GetItemText(x) + '|' + self.lstItems.GetItem(x, 1).GetText()
            x += 1

        return wcstring

#*******************************************************************************************************

class drReplaceTableDialog(drFilePrefsDialogBase):
    def __init__(self, parent):
        drFilePrefsDialogBase.__init__(self, parent, 'Windows Shortcut Replace Table')

        self.btnUp.Show(False)
        self.btnDown.Show(False)

        self.SetColumns('Windows Pattern', 'Replace String')

        self.SetDialog('Windows Pattern:', 'Replace String:', 'Replace Table Entry')

        self.ancestor = parent.grandparent

        wcarray = self.ancestor.prefs.windowsshortcutreplacetable.split('#')

        l = len(wcarray)

        x = 0
        while x < l:
            y = self.lstItems.GetItemCount()
            if wcarray[x]:
                items = wcarray[x].split(',')
                self.lstItems.InsertStringItem(y, items[0])
                self.lstItems.SetStringItem(y, 1, items[1])
            x += 1

    def GetReplaceTable(self):
        l = self.lstItems.GetItemCount()
        if l < 1:
            return ''
        wcstring = self.lstItems.GetItemText(0) + ',' + self.lstItems.GetItem(0, 1).GetText()
        x = 1
        while x < l:
            wcstring += '#' + self.lstItems.GetItemText(x) + ',' + self.lstItems.GetItem(x, 1).GetText()
            x += 1

        return wcstring
