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

#Single Choice Dialog (Keyboard Navigation, FindCompletion with TextCtrl Echo.)

import wx

#*******************************************************************************************************


class drSingleChoiceDialog(wx.Dialog):
    def __init__(self, parent, title, choices, sort=True, point=wx.DefaultPosition, size=(250, 300), SetSizer=True, header="", editbutton=""):
        wx.Dialog.__init__(self, parent, -1, title, point, size, wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.parent = parent

        self.ID_CHOICES = 101
        self.ID_TXT_STATIC = 102
        self.ID_TXT_CHOICE = 103

        self.ID_OK = 111
        self.ID_CANCEL = 112
        if editbutton:
            self.ID_EDIT = 113

        #/Constants

        #Components:

        self.listChoices = wx.ListView(self, self.ID_CHOICES, (0, 0), (300, 300), style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_NO_HEADER)

        if header:
            self.txtHeader = wx.StaticText(self, self.ID_TXT_STATIC, header, (0, 0), (300, -1))
        self.txtChoice = wx.TextCtrl (self, self.ID_TXT_CHOICE, '', (0, 0), (250, -1), style=wx.TE_READONLY)

        self.choices = choices[:]

        self.listChoices.InsertColumn(0, 'Choices')

        if sort:
            self.choices.sort()
            #self.choices.sort(lambda x,y: cmp(x.lower(), y.lower())) #case insensitve

        self.setupchoices()

        self.OnSize(None)

        self.btnOk = wx.Button(self, self.ID_OK, "  &Ok  ")

        #self.btnOk.SetDefault()

        self.btnCancel = wx.Button(self, self.ID_CANCEL, "  &Cancel  ")
        if editbutton:
            self.btnEdit = wx.Button(self, self.ID_EDIT, editbutton)

        #/Components

        #Sizer:

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.textSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.textSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_RIGHT)
        self.textSizer.Add(self.txtChoice, 1, wx.EXPAND)
        self.textSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)

        if header:
            self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)

            self.headerSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_RIGHT)
            self.headerSizer.Add(self.txtHeader, 1, wx.EXPAND)
            self.headerSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)


        self.listSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.listSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_RIGHT)
        self.listSizer.Add(self.listChoices, 1, wx.EXPAND)
        self.listSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)

        self.commandSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.commandSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_RIGHT)
        self.commandSizer.Add(self.btnCancel, 0, wx.SHAPED | wx.ALIGN_LEFT)
        if editbutton:
            self.commandSizer.Add(wx.StaticText(self, -1, '  '), 1, wx.SHAPED | wx.ALIGN_RIGHT)
            self.commandSizer.Add(self.btnEdit, 0, wx.SHAPED | wx.ALIGN_LEFT)
        self.commandSizer.Add(wx.StaticText(self, -1, '  '), 1, wx.EXPAND)
        self.commandSizer.Add(self.btnOk, 0, wx.SHAPED | wx.ALIGN_RIGHT)
        self.commandSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_RIGHT)

        self.theSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        if header:
            self.theSizer.Add(self.headerSizer, 0, wx.EXPAND)
            self.theSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Add(self.textSizer, 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Add(self.listSizer, 9, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Add(self.commandSizer, 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)

        self.SetAutoLayout(True)

        if SetSizer:
            self.SetSizerAndFit(self.theSizer)

        #/Sizer

        #Events:

        self.Bind(wx.EVT_BUTTON, self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnbtnOk, id=self.ID_OK)
        if editbutton:
            self.Bind(wx.EVT_BUTTON, self.OnbtnEdit, id=self.ID_EDIT)

        self.listChoices.Bind(wx.EVT_LEFT_DCLICK, self.OnbtnOk)
        self.txtChoice.Bind(wx.EVT_CHAR, self.OnChar)

        if wx.Platform == '__WXGTK__':
            self.txtChoice.SetFocus()
        else:
            self.Bind(wx.EVT_CHAR, self.OnChar)
            self.listChoices.Bind(wx.EVT_CHAR, self.OnChar)

        self.listChoices.Bind(wx.EVT_SIZE, self.OnSize)

        #/Events

        if self.listChoices.GetItemCount() > 0:
            self.listChoices.Select(0)
            self.listChoices.Focus(0)

        self.typedchoice = ''

    def GetSelection(self):
        return self.listChoices.GetItemData(self.listChoices.GetFirstSelected())

    def GetStringSelection(self):
        return self.listChoices.GetItemText(self.listChoices.GetFirstSelected())

    def OnbtnEdit(self, event):
        if self.listChoices.GetItemCount() > 0:
            self.EndModal(wx.ID_EDIT)
        else:
            self.EndModal(wx.ID_CANCEL)

    def OnbtnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnbtnOk(self, event):
        if self.listChoices.GetItemCount() > 0:
            self.EndModal(wx.ID_OK)
        else:
            self.EndModal(wx.ID_CANCEL)

    def OnChar(self, event):
        keycode = event.GetKeyCode()

        if keycode >= 32 and keycode <= 127:
            self.typedchoice += chr(keycode).lower()
            self.UpdateTypedChoice()
        elif keycode == wx.WXK_BACK:
            self.typedchoice = self.typedchoice[:-1]
            self.UpdateTypedChoice()

        if keycode in [wx.WXK_DOWN, wx.WXK_UP, wx.WXK_PAGEDOWN, wx.WXK_PAGEUP, wx.WXK_HOME, wx.WXK_END]:
            i = self.listChoices.GetFocusedItem()
            if keycode == wx.WXK_UP:
                i -= 1
            elif keycode == wx.WXK_DOWN:
                i += 1
            elif keycode == wx.WXK_HOME:
                i = 0
            elif keycode == wx.WXK_END:
                i = self.listChoices.GetItemCount() - 1
            elif keycode == wx.WXK_PAGEDOWN:
                i += self.listChoices.CountPerPage
            elif keycode == wx.WXK_PAGEUP:
                i -= self.listChoices.CountPerPage
            #min/max function?
            if i < 0:
                i = 0
            if i >= self.listChoices.GetItemCount():
                i = self.listChoices.GetItemCount() - 1
            #if (i < self.listChoices.GetItemCount()) and (i > -1):
            self.listChoices.Select(i)
            self.listChoices.Focus(i)
            return

        if keycode == wx.WXK_ESCAPE:
            self.OnbtnCancel(None)
        elif keycode == wx.WXK_RETURN:
            self.OnbtnOk(None)
        else:
            event.Skip()

    def OnSize(self, event):
        self.listChoices.SetColumnWidth(0, self.listChoices.GetSizeTuple()[0])
        if event is not None:
            event.Skip()

    def setupchoices(self, findstr=''):
        self.listChoices.DeleteAllItems()
        x = 0
        sofar = 0
        if findstr:
            for c in self.choices:
                a = c.lower()
                if a.find(findstr) > -1:
                    self.listChoices.InsertStringItem(sofar, c)
                    self.listChoices.SetItemData(sofar, x)
                    sofar += 1
                x += 1
        else:
            for c in self.choices:
                self.listChoices.InsertStringItem(x, c)
                self.listChoices.SetItemData(x, x)
                x += 1

    def UpdateTypedChoice(self):
        self.txtChoice.SetValue(self.typedchoice)
        if wx.Platform == '__WXGTK__':
            self.txtChoice.SetSelection(len (self.typedchoice), len(self.typedchoice))
        self.setupchoices(self.typedchoice)
        if self.listChoices.GetItemCount() > 0:
            self.listChoices.Select(0)
            self.listChoices.Focus(0)

if __name__ == '__main__':
    app = wx.App()
    w = drSingleChoiceDialog(None, "Test drSingleChoiceDialog:", ["a","b","c"], wx.CHOICEDLG_STYLE, header="Headertest") #optional headertest
    w.ShowModal()
    w.Destroy()
    app.MainLoop()

