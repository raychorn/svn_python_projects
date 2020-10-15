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

#Go To Source Browser

import re
import wx
from drSingleChoiceDialog import drSingleChoiceDialog

respacecount = re.compile(r'\S')

def GetMatches(text, resourcebrowser):
    matches = []
    positions = []

    matcher = resourcebrowser.finditer(text)

    try:
        match = matcher.next()
    except:
        match = None
    while match is not None:
        matches.append(match.group().replace('\t', '    '))
        positions.append(match.start())
        try:
            match = matcher.next()
        except:
            match = None

    return matches, positions

class drSourceBrowserGoToDialog(drSingleChoiceDialog):

    def __init__(self, parent, Document, matches, positions):
        drSingleChoiceDialog.__init__(self, parent, 'Source Browser Go To', matches, False, SetSizer=False)

        self.Document = Document

        self.positions = positions

        self.txtLine = wx.TextCtrl(self, -1, '', (0, 0), (350, -1), style=wx.TE_READONLY)
        self.txtDefinedIn = wx.TextCtrl(self, -1, '', (0, 0), (350, -1), style=wx.TE_READONLY)

        self.lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lineSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        self.lineSizer.Add(self.txtLine, 1, wx.EXPAND)
        self.lineSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)

        self.defSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.defSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        self.defSizer.Add(self.txtDefinedIn, 1, wx.EXPAND)
        self.defSizer.Add(wx.StaticText(self, -1, '  '), 0, wx.SHAPED)

        self.theSizer.Insert(2, wx.StaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Insert(3, self.lineSizer, 0, wx.EXPAND)
        self.theSizer.Insert(4, self.defSizer, 0, wx.EXPAND)

        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected, id=self.ID_CHOICES)

        self.OnSelected(None)

    def OnSelected(self, event):
        sel = self.listChoices.GetFirstSelected()
        if sel > -1:
            pos = self.listChoices.GetItemData(sel)

            spaces = respacecount.search(self.choices[pos]).start() - 1

            definedin = self.Document.GetFilenameTitle()

            if spaces > 0:
                x = pos
                while x > -1:
                    if (respacecount.search(self.choices[x]).start() - 1) < spaces:
                        definedin = self.choices[x].rstrip()
                        break
                    x -= 1

            linenumber = str(self.Document.LineFromPosition(self.positions[pos]) + 1)

            self.txtLine.SetValue('Line Number:      ' + linenumber)
            self.txtDefinedIn.SetValue('Defined In:    ' + definedin)

def SourceBrowserGoTo(frame, Document):
    compchar = Document.GetIndentationCharacter()
    resourcebrowser = re.compile(r'(^'+compchar+'*?class\s.*[(:])|(^'+compchar+'*?def\s.*[(:])|(^'+compchar+'*?import\s.*$)|(^'+compchar+'*?from\s.*$)', re.MULTILINE)
    text = Document.GetText()

    matches, positions = GetMatches(text, resourcebrowser)

    d = drSourceBrowserGoToDialog(frame, Document, matches, positions)
    answer = d.ShowModal()
    d.Destroy()

    if answer == wx.ID_OK:
        i = d.GetSelection()
        line = Document.LineFromPosition(positions[i])
        Document.EnsureVisible(line)
        Document.ScrollToLine(line)
        Document.GotoLine(line)
        Document.GotoPos(positions[i])

    Document.SetFocus()
    Document.SetSTCFocus(True)
