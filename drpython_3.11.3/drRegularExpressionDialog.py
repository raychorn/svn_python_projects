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

#Regular Expression Dialog

import os
import re
import wx
import drScrolledMessageDialog
import drFileDialog

wildcard = "Text File (*.txt)|*.txt|All files (*)|*"

class drRETextCtrl(wx.TextCtrl):
    def __init__(self, parent, id, value, pos, size):
        wx.TextCtrl.__init__(self, parent, id, value, pos, size)

        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.GetParent().OnbtnCancel(event)
        elif event.GetKeyCode() == wx.WXK_RETURN:
            self.GetParent().OnbtnOk(event)
        else:
            event.Skip()


class drRegularExpressionDialog(wx.Frame):
    def __init__(self, parent, id, title, prompthasfocus = 0, infiles = 0):

        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.ID_OK = 1001
        self.ID_CANCEL = 1002

        self.ID_LOAD = 1003
        self.ID_SAVE = 1004

        self.ID_ANYCHARACTER = 1010
        self.ID_ANYCHARACTERD = 10101
        self.ID_ANYCHARACTERND = 10102
        self.ID_ANYCHARACTERW = 10103
        self.ID_ANYCHARACTERNW = 10104
        self.ID_ANYCHARACTERA = 10105
        self.ID_ANYCHARACTERNA = 10106
        self.ID_SETOFCHARACTERS = 10107
        self.ID_START = 1011
        self.ID_END = 1012
        self.ID_STARTD = 1111
        self.ID_ENDD = 1112
        self.ID_EDGEW = 1211
        self.ID_EDGENW = 1212
        self.ID_REPSZEROPLUS = 1013
        self.ID_REPSONEPLUS = 1014
        self.ID_REPSZEROORONE = 1015
        self.ID_REPSN = 1016
        self.ID_GROUP = 1017
        self.ID_OR = 10171
        self.ID_POSITIVE_LOOKAHEAD = 1018
        self.ID_NEGATIVE_LOOKAHEAD = 1019
        self.ID_POSITIVE_LOOKBEHIND = 1118
        self.ID_NEGATIVE_LOOKBEHIND = 1119

        self.ID_INSERT_NORMAL_TEXT = 1050

        self.insert = (title == "Insert Regular Expression")

        self.theSizer = wx.FlexGridSizer(0, 1, 5, 10)

        okcancelSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.parent = parent
        self.prompthasfocus = prompthasfocus

        #that part of code is ugly
        if self.insert:
            self.drpyframe = self.parent
        elif not infiles:
            self.drpyframe = self.parent.GetParent()
        else:
            self.drpyframe = self.parent.GetGrandParent()

        self.defaultdirectory = self.drpyframe.prefs.defaultdirectory
        self.enablefeedback = self.drpyframe.prefs.enablefeedback
        self.filedialogparent = self.drpyframe
        self.regdatdirectory = os.path.join(self.drpyframe.datdirectory, 'regex')
        if not os.path.exists(self.regdatdirectory):
            os.mkdir(self.regdatdirectory)

        #end of uglpy part of code

        FileMenu = wx.Menu()
        FileMenu.Append(self.ID_LOAD, "&Load", " Load Regular Expression")
        FileMenu.Append(self.ID_SAVE, "&Save", " Save Regular Expression")

        TextMenu = wx.Menu()
        TextMenu.Append(self.ID_INSERT_NORMAL_TEXT, "Normal Text")
        TextMenu.Append(self.ID_ANYCHARACTER, "Any Character  \".\"")
        TextMenu.Append(self.ID_ANYCHARACTERD, "Any Decimal Digit  \"\\d\"")
        TextMenu.Append(self.ID_ANYCHARACTERND, "Any Non Digit  \"\\D\"")
        TextMenu.Append(self.ID_ANYCHARACTERW, "Any Whitespace Character  \"\\s\"")
        TextMenu.Append(self.ID_ANYCHARACTERNW, "Any Non Whitespace Character  \"\\S\"")
        TextMenu.Append(self.ID_ANYCHARACTERA, "Any AlphaNumeric Character  \"\\w\"")
        TextMenu.Append(self.ID_ANYCHARACTERNA, "Any Non AlphaNumeric Character  \"\\W\"")
        TextMenu.Append(self.ID_SETOFCHARACTERS, "A Set of Characters  \"[ ]\"")

        RepetitionsMenu = wx.Menu()
        RepetitionsMenu.Append(self.ID_REPSZEROPLUS, "0 Or More  \"*\"")
        RepetitionsMenu.Append(self.ID_REPSONEPLUS, "1 Or More  \"+\"")
        RepetitionsMenu.Append(self.ID_REPSZEROORONE, "0 Or 1  \"?\"")
        RepetitionsMenu.Append(self.ID_REPSN, "n  \"{n}\"")

        LimitMenu = wx.Menu()
        LimitMenu.Append(self.ID_START, "The Start Of Each Line  \"^\"")
        LimitMenu.Append(self.ID_END, "The End Of Each Line  \"$\"")
        LimitMenu.Append(self.ID_STARTD, "The Start of the Document  \"\\A\"")
        LimitMenu.Append(self.ID_ENDD, "The End of the Document  \"\\Z\"")
        LimitMenu.Append(self.ID_EDGEW, "The Start or End of a Word  \"\\b\"")
        LimitMenu.Append(self.ID_EDGENW, "Text That is Not at Either End of a Word  \"\\B\"")

        lookMenu = wx.Menu()
        lookMenu.Append(self.ID_POSITIVE_LOOKAHEAD, "Lookahead: Positive  \"(?=)\"")
        lookMenu.Append(self.ID_NEGATIVE_LOOKAHEAD, "Lookahead: Negative  \"(?!)\"")
        lookMenu.Append(self.ID_POSITIVE_LOOKBEHIND, "Lookbehind: Positive  \"(?<=)\"")
        lookMenu.Append(self.ID_NEGATIVE_LOOKBEHIND, "Lookbehind: Negative  \"(?<!)\"")

        InsertMenu = wx.Menu()
        InsertMenu.AppendMenu(3001, "&Text", TextMenu)
        InsertMenu.AppendMenu(3002, "&Repetitions", RepetitionsMenu)
        InsertMenu.AppendMenu(3003, "&Match", LimitMenu)
        InsertMenu.AppendMenu(3004, "&Assertions", lookMenu)
        InsertMenu.Append(self.ID_OR, "&Or  \"|\"")
        InsertMenu.Append(self.ID_GROUP, "&Group  \"( )\"")

        menuBar = wx.MenuBar()
        menuBar.Append(FileMenu,"&File")
        menuBar.Append(InsertMenu,"&Insert")

        self.SetMenuBar(menuBar)

        self.txtRE = drRETextCtrl(self, -1, "", wx.DefaultPosition, (500, -1))

        self.btnOk = wx.Button(self, self.ID_OK, "&Ok")
        self.btnCancel = wx.Button(self, self.ID_CANCEL, "&Cancel")

        okcancelSizer.Add(self.btnOk, 1, wx.SHAPED)
        okcancelSizer.Add(self.btnCancel, 1, wx.SHAPED)

        self.theSizer.Add(self.txtRE, 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(okcancelSizer, 1, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.btnOk.SetDefault()
        self.txtRE.SetFocus()

        self.Bind(wx.EVT_BUTTON,  self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnOk, id=self.ID_OK)

        self.Bind(wx.EVT_MENU,  self.OnLoad, id=self.ID_LOAD)
        self.Bind(wx.EVT_MENU,  self.OnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacter, id=self.ID_ANYCHARACTER)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacterD, id=self.ID_ANYCHARACTERD)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacterND, id=self.ID_ANYCHARACTERND)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacterW, id=self.ID_ANYCHARACTERW)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacterNW, id=self.ID_ANYCHARACTERNW)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacterA, id=self.ID_ANYCHARACTERA)
        self.Bind(wx.EVT_MENU,  self.OnbtnAnyCharacterNA, id=self.ID_ANYCHARACTERNA)
        self.Bind(wx.EVT_MENU,  self.OnbtnSetOfCharacters, id=self.ID_SETOFCHARACTERS)
        self.Bind(wx.EVT_MENU,  self.OnbtnStart, id=self.ID_START)
        self.Bind(wx.EVT_MENU,  self.OnbtnEnd, id=self.ID_END)
        self.Bind(wx.EVT_MENU,  self.OnbtnStartD, id=self.ID_STARTD)
        self.Bind(wx.EVT_MENU,  self.OnbtnEndD, id=self.ID_ENDD)
        self.Bind(wx.EVT_MENU,  self.OnbtnEdgeW, id=self.ID_EDGEW)
        self.Bind(wx.EVT_MENU,  self.OnbtnEdgeNW, id=self.ID_EDGENW)
        self.Bind(wx.EVT_MENU,  self.OnbtnRepsZeroPlus, id=self.ID_REPSZEROPLUS)
        self.Bind(wx.EVT_MENU,  self.OnbtnRepsOnePlus, id=self.ID_REPSONEPLUS)
        self.Bind(wx.EVT_MENU,  self.OnbtnRepsZeroOrOne, id=self.ID_REPSZEROORONE)
        self.Bind(wx.EVT_MENU,  self.OnbtnRepsN, id=self.ID_REPSN)
        self.Bind(wx.EVT_MENU,  self.OnbtnOr, id=self.ID_OR)
        self.Bind(wx.EVT_MENU,  self.OnbtnGroup, id=self.ID_GROUP)
        self.Bind(wx.EVT_MENU,  self.OnbtnLookPositiveA, id=self.ID_POSITIVE_LOOKAHEAD)
        self.Bind(wx.EVT_MENU,  self.OnbtnLookNegativeA, id=self.ID_NEGATIVE_LOOKAHEAD)
        self.Bind(wx.EVT_MENU,  self.OnbtnLookPositiveB, id=self.ID_POSITIVE_LOOKBEHIND)
        self.Bind(wx.EVT_MENU,  self.OnbtnLookNegativeB, id=self.ID_NEGATIVE_LOOKBEHIND)

        self.Bind(wx.EVT_MENU,  self.OnbtnInsertNormalText, id=self.ID_INSERT_NORMAL_TEXT)

        if self.drpyframe.PLATFORM_IS_WIN:
            size = (500, 160)
        else:
            size = (500, 110)
        self.SetSize(size)

    def insertText(self, text):
        pos = self.txtRE.GetInsertionPoint()
        textRE = self.txtRE.GetValue()
        self.txtRE.SetValue(textRE[0:pos] + text + textRE[pos:])
        self.txtRE.SetInsertionPoint(pos + len(text))

    def OnbtnAnyCharacter(self, event):
        self.insertText('.')

    def OnbtnAnyCharacterA(self, event):
        self.insertText('\\w')

    def OnbtnAnyCharacterD(self, event):
        self.insertText('\\d')

    def OnbtnAnyCharacterNA(self, event):
        self.insertText('\\W')

    def OnbtnAnyCharacterND(self, event):
        self.insertText('\\D')

    def OnbtnAnyCharacterNW(self, event):
        self.insertText('\\S')

    def OnbtnAnyCharacterW(self, event):
        self.insertText('\\s')

    def OnbtnCancel(self, event):
        self.txtRE.SetValue("")
        self.Close(1)

    def OnbtnEdgeNW(self, event):
        self.insertText('\\B')

    def OnbtnEdgeW(self, event):
        self.insertText('\\b')

    def OnbtnEnd(self, event):
        self.insertText('$')

    def OnbtnEndD(self, event):
        self.insertText('\\Z')

    def OnbtnGroup(self, event):
        self.insertText('()')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnInsertNormalText(self, event):
        d = wx.TextEntryDialog(self, "Enter Normal Text", "Insert Normal Text", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            self.insertText(re.escape(v))

    def OnbtnLookNegativeA(self, event):
        self.insertText('(?!)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnLookPositiveA(self, event):
        self.insertText('(?=)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnLookNegativeB(self, event):
        self.insertText('(?<!)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnLookPositiveB(self, event):
        self.insertText('(?<=)')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnOk(self, event):
        self.Show(0)

        result = self.txtRE.GetValue()
        l = len(result)
        if l > 0:
            if self.insert:
                if self.prompthasfocus:
                    pos = self.parent.txtPrompt.GetCurrentPos()
                    self.parent.txtPrompt.InsertText(pos, result)
                    self.parent.txtPrompt.GotoPos(pos + l)
                else:
                    pos = self.parent.txtDocument.GetCurrentPos()
                    self.parent.txtDocument.InsertText(pos, result)
                    self.parent.txtDocument.GotoPos(pos + l)
            else:
                self.parent.txtSearchFor.SetValue(result)

        self.Close(1)

    def OnbtnOr(self, event):
        self.insertText('|')

    def OnbtnRepsN(self, event):
        d = wx.TextEntryDialog(self, "Enter The Desired Number of Repetitions:", "Insert N Repetitions", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            self.insertText('{' + v + '}')

    def OnbtnRepsOnePlus(self, event):
        self.insertText('+')

    def OnbtnRepsZeroOrOne(self, event):
        self.insertText('?')

    def OnbtnRepsZeroPlus(self, event):
        self.insertText('*')

    def OnbtnSetOfCharacters(self, event):
        self.insertText('[]')
        pos = self.txtRE.GetInsertionPoint()
        self.txtRE.SetInsertionPoint(pos - 1)

    def OnbtnStart(self, event):
        self.insertText('^')

    def OnbtnStartD(self, event):
        self.insertText('\\A')

    def OnLoad(self, event):
        dlg = drFileDialog.FileDialog(self.filedialogparent, "Load Regular Expression From", wildcard)
        if self.regdatdirectory:
            try:
                dlg.SetDirectory(self.regdatdirectory)
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Setting Default Directory To: " + self.regdatdirectory), "DrPython Error")
        if dlg.ShowModal() == wx.ID_OK:
            refile = dlg.GetPath().replace("\\", "/")
            try:
                f = open(refile, 'r')
                text = f.read()
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Reading From: " +  refile), "DrPython Error")
                text = ""
            if (text.find('\n') > -1) or (text.find('\r') > -1):
                drScrolledMessageDialog.ShowMessage(self, ("Error Reading From: " +  refile), "DrPython Error")
                text = ""
            self.txtRE.SetValue(text)

        dlg.Destroy()
        self.Raise()

    def OnSave(self, event):
        dlg = drFileDialog.FileDialog(self.filedialogparent, "Save Regular Expression As", wildcard, IsASaveDialog=True)
        if self.regdatdirectory:
            try:
                dlg.SetDirectory(self.regdatdirectory)
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Setting Default Directory To: " + self.regdatdirectory), "DrPython Error")
        if dlg.ShowModal() == wx.ID_OK:
            refile = dlg.GetPath().replace("\\", "/")
            if refile.lower()[-4:] != '.txt':
                refile += '.dma'
            try:
                f = open(refile, 'w')
                f.write(self.txtRE.GetValue())
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self, ("Error Writing To: " +  refile), "DrPython Error")
                return
            if self.enablefeedback:
                drScrolledMessageDialog.ShowMessage(self, ("Successfully Saved: " + refile), "Save Success")
            dlg.Destroy()
        self.Raise()
