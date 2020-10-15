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

#The StyledTextControl Base Class

import re, string
import wx
import wx.stc
import drPopUp
import drShortcuts, drShortcutsFile
from drDragAndDrop import drDropTarget
from drFindReplaceDialog import drFinder

#*******************************************************************************************************

class DrStyledTextControl(wx.stc.StyledTextCtrl):
    def __init__(self, parent, id, grandparent):
        wx.stc.StyledTextCtrl.__init__(self, parent, id)

        #Constants:

        self.PYTHON_FILE = 0
        self.CPP_FILE = 1
        self.HTML_FILE = 2
        self.TEXT_FILE = 3

        self.IsAPrompt = False

        self.IndicatorSetStyle(0, wx.stc.STC_INDIC_HIDDEN)

        self.grandparent = grandparent

        self.Finder = drFinder(grandparent, self)

        #Python!!!!
        self.filetype = 0

        self.stclabelarray = drShortcutsFile.GetSTCShortcutList()
        self.stcactionarray = drShortcuts.GetSTCCommandList()

        self.ID_POPUP_BASE = 33000

        #Speed Optimization Submitted by Franz
        self.SetModEventMask(wx.stc.STC_PERFORMED_UNDO | wx.stc.STC_PERFORMED_REDO |\
        wx.stc.STC_MOD_DELETETEXT | wx.stc.STC_MOD_INSERTTEXT)

        self.droptarget = drDropTarget(self)

        self.SetDropTarget(self.droptarget)

        #WIERD!
        self.SetProperty("tab.timmy.whinge.level", "1")

        #Right Click Menu
        self.UsePopUp(0)

        self.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)

        self.SetMarginWidth(0, 0)
        self.SetMarginWidth(1, 0)
        self.SetMarginWidth(2, 0)

        self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)

        self.SetScrollWidth(1)

        self.retab = re.compile('^\t+', re.MULTILINE)
        self.respaces = re.compile('^ +', re.MULTILINE)
        self.remixedoutright = re.compile('(^\t+ )|(^ +\t)', re.MULTILINE)

        self.indentationtype = 2

        self.renonwhitespace = re.compile('\S')

        if self.grandparent.prefs.doceolmode[self.filetype] == 1:
            self.SetEOLMode(wx.stc.STC_EOL_CRLF)
        elif self.grandparent.prefs.doceolmode[self.filetype] == 2:
            self.SetEOLMode(wx.stc.STC_EOL_CR)
        else:
            self.SetEOLMode(wx.stc.STC_EOL_LF)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def CheckIndentation(self, text=None):
        if text is None:
            text = self.GetText()
        if not text:
            return 2

        tabs = (self.retab.search(text) is not None)
        spaces = (self.respaces.search(text) is not None)
        mixed = (self.remixedoutright.search(text) is not None)

        if mixed or (tabs and spaces):
            return 0
        elif tabs:
            return 1
        elif spaces:
            return -1
        return 2

    def EnsurePositionIsVisible(self, position):
        self.GotoPos(self.PositionFromLine(self.LineFromPosition(position)))

        self.EnsureCaretVisible()

        self.GotoPos(position)

        self.EnsureCaretVisible()

    def GetEndOfLineCharacter(self):
        emode = self.GetEOLMode()
        if emode == wx.stc.STC_EOL_CR:
            return '\r'
        elif emode == wx.stc.STC_EOL_CRLF:
            return '\r\n'
        return '\n'

    def GetIndentationCharacter(self):
        #What is this document using?
        result = self.CheckIndentation()
        if result == 0:
            if self.grandparent.prefs.docusetabs[self.filetype]:
                result = 1
            else:
                result = -1

        if result == 1:
            compchar = '\t'
        else:
            compchar = ' '

        return compchar

    def OnLeftDown(self, event):
        self.droptarget.SetModifierDown(event.ControlDown())
        if self.grandparent.prefs.draganddropmode != 1:
            pos = self.PositionFromPoint(wx.Point(event.GetX(), event.GetY()))
            s, e = self.GetSelection()
            if (pos > s) and (pos < e):
                self.SetSelection(pos, pos)
                return
        event.Skip()

    def OnPopUp(self, event):
        #fast context #ugly hack franz
        if event.ControlDown():
            import drAboutDialog
            dlg = drAboutDialog.drAboutDialog(self.grandparent)
            dlg.notebook.SetSelection(2)
            dlg.ShowModal()
        else:
            #end ugly hack franz
            drPopUp.OnPopUp(self, event)

    def OnPopUpMenu(self, event):
        drPopUp.OnPopUpMenu(self, event)

    def Paste(self):
        if wx.TheClipboard.IsOpened():
            wx.TheClipboard.Close()
        wx.TheClipboard.Open()
        tdo = wx.TextDataObject()
        data = wx.TheClipboard.GetData(tdo)
        if data:
            text = tdo.GetText()

            #Clean Up the Text:

            #Line Endings First:
            emode = self.GetEOLMode()
            if emode == wx.stc.STC_EOL_CR:
                text = self.grandparent.FormatMacReTarget.sub('\r', text)
            elif emode == wx.stc.STC_EOL_CRLF:
                text = self.grandparent.FormatWinReTarget.sub('\r\n', text)
            else:
                text = self.grandparent.FormatUnixReTarget.sub('\n', text)

            line, pos = self.GetCurLine()

            skipfirstline = self.renonwhitespace.search(line[:pos]) is not None

            #Now Indentation:
            if self.indentationtype == -1:
                text = self.SetToSpaces(-1, text)
            elif self.indentationtype == 1:
                text = self.SetToTabs(-1, text, skipfirstline)
            else:
                if self.grandparent.prefs.docusetabs[self.filetype]:
                    text = self.SetToTabs(-1, text, skipfirstline)
                else:
                    text = self.SetToSpaces(-1, text)
                if self.grandparent.prefs.docusetabs[self.filetype]:
                    self.indentationtype = 1
                else:
                    self.indentationtype = -1

            s, e = self.GetSelection()
            if (e - s) > 0:
                self.SetTargetStart(s)
                self.SetTargetEnd(e)
                self.ReplaceTarget(text)
                pos = self.GetCurrentPos()
            else:
                pos = self.GetCurrentPos()
                self.InsertText(pos, text)

            self.GotoPos(pos + len(text))

        self.OnModified(None)

        wx.TheClipboard.Close()

    def SetSelectedText(self, text):
        self.SetTargetStart(self.GetSelectionStart())
        self.SetTargetEnd(self.GetSelectionEnd())
        self.ReplaceTarget(text)

    def SetToSpaces(self, tabwidth=-1, text=''):
        print tabwidth
        if tabwidth < 0:
            tabwidth = self.grandparent.prefs.doctabwidth[self.filetype]
        #eol = self.GetEndOfLineCharacter()
        #regex = re.compile('(\S)|' + eol)
        SetTheText = False
        print "set", text
        if not text:
            text = self.GetText()
            SetTheText = True
        #lines = text.split(eol)
        #new_lines = []
        #for line in lines:
        #    result = regex.search(line + eol)
        #    if result is not None:
        #        end = result.start()
        #        new_lines.append(line[0:end].expandtabs(tabwidth) + line[end:])
        #    else:
        #        new_lines.append(line)
        #newtext = string.join(new_lines, eol)
        print "hi", tabwidth, text
        newtext = text.expandtabs(tabwidth)

        self.indentationtype = -1
        self.SetupTabs(False)
        if SetTheText:
            self.SetText(newtext)
        else:
            return newtext

    def SetToTabs(self, tabwidth=-1, text='', skipfirstline=False):
        if tabwidth < 0:
            tabwidth = self.grandparent.prefs.doctabwidth[self.filetype] - 1
        else:
            tabwidth -= 1
        eol = self.GetEndOfLineCharacter()
        regex = re.compile('(\S)|' + eol)
        #Create Target String
        y = 0
        oof = " "
        while y < tabwidth:
            oof = oof + " "
            y = y + 1
        #Continue
        if not text:
            text = self.GetText()
            SetTheText = True
        else:
            SetTheText = False
        lines = text.split(eol)
        new_lines = []
        x = 0
        for line in lines:
            result = regex.search(line + eol)
            if result is not None:
                end = result.start()
                newline = line[0:end].replace(oof, "\t")
                if x == 0 and skipfirstline:
                    newline = newline + line[end:]
                else:
                    newline = newline.replace(' ', '') + line[end:]
                new_lines.append(newline)
            else:
                new_lines.append(line)
            x += 1
        newtext = string.join(new_lines, eol)

        self.indentationtype = 1
        self.SetupTabs(True)

        if SetTheText:
            self.SetText(newtext)
        else:
            return newtext

    def SetupTabs(self, UseTabs=-1):
        if UseTabs == -1:
            UseTabs = self.grandparent.prefs.docusetabs[self.filetype]

        self.SetUseTabs(UseTabs)

        self.tabwidth = self.grandparent.prefs.doctabwidth[self.filetype]
        self.addchar = '\t'
        if not UseTabs:
            #franz: x not referenced
            self.addchar = "\t".expandtabs(self.tabwidth)
