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
#
#Some Folding Code From demo.py by Robin Dunn
#Some more from pype by Josiah Carlson

#The Document

import os.path, re
import wx
import wx.stc
from drProperty import *
import drKeywords
import drSTC
import drEncoding

#*******************************************************************************************************

class DrText(drSTC.DrStyledTextControl):
    def __init__(self, parent, id, grandparent, DynamicScript = 0, SplitView=0):
        drSTC.DrStyledTextControl.__init__(self, parent, id, grandparent)

        self.notebookparent = grandparent.documentnotebook

        self.indentationtype = 1
        if not self.grandparent.prefs.docusetabs[0]:
            self.indentationtype = -1

        self.filename = ""

        self.mtime = -1

        self.untitlednumber = 0

        self.lineendingsaremixed = 0

        self.IsActive = True

        self.filetype = 0

        self.encoding = '<Default Encoding>'

        self.SetupTabs()

        self.usestyles = (self.grandparent.prefs.docusestyles == 1)

        self.indentationstring = ""

        #Keyword Search/Context Sensitive Autoindent.
        self.rekeyword = re.compile(r"(\sreturn\b)|(\sbreak\b)|(\spass\b)|(\scontinue\b)|(\sraise\b)", re.MULTILINE)
        self.reslash = re.compile(r"\\\Z")

        self.renonwhitespace = re.compile('\S', re.M)

        self.DisableShortcuts = (SplitView == 1)

        if SplitView == -1:
            SplitView = 1

        self.IsSplitView = SplitView

        #Check this against Self.GetModify(), to ensure events are called too many times.
        self.modified = False

        self.DynamicScript = DynamicScript

        if not DynamicScript:
            self.targetPosition = 0
            self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnModified, id=id)
            self.Bind(wx.EVT_KEY_UP, self.OnPositionChanged)
            self.Bind(wx.EVT_LEFT_UP, self.OnPositionChanged)
        self.Bind(wx.EVT_UPDATE_UI,  self.OnUpdateUI, id=id)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.OnMarginClick, id=id)

    def _autoindent(self):
        pos = self.GetCurrentPos()

        #Strip trailing whitespace first.
        currentline = self.LineFromPosition(pos)
        lineendpos = self.GetLineEndPosition(currentline)
        if lineendpos > pos:
            self.SetTargetStart(pos)
            self.SetTargetEnd(lineendpos)
            t = self.GetTextRange(pos, lineendpos)
            self.ReplaceTarget(t.rstrip())

        #Look at last line
        pos = pos - 1
        clinenumber = self.LineFromPosition(pos)

        linenumber = clinenumber

        self.GotoPos(pos)

        self.GotoLine(clinenumber)

        numtabs = self.GetLineIndentation(clinenumber+1) / self.tabwidth

        if self.renonwhitespace.search(self.GetLine(clinenumber+1)) is not None:
            if self.renonwhitespace.search(self.GetLine(clinenumber)) is None:
                numtabs += self.GetLineIndentation(clinenumber) / self.tabwidth

        if numtabs == 0:
            numtabs = self.GetLineIndentation(linenumber) / self.tabwidth

        if (self.grandparent.prefs.docautoindent == 2) and (self.filetype == 0):
            checkat = self.GetLineEndPosition(linenumber) - 1
            if self.GetCharAt(checkat) == ord(':'):
                numtabs = numtabs + 1
            else:
                lastline = self.GetLine(linenumber)
                #Remove Comment:
                comment = lastline.find('#')
                if comment > -1:
                    lastline = lastline[:comment]
                if self.reslash.search(lastline.rstrip()) is None:
                    if self.rekeyword.search(lastline) is not None:
                        numtabs = numtabs - 1
        #Go to current line to add tabs

        self.SetTargetStart(pos+1)
        end = self.GetLineEndPosition(clinenumber+1)
        self.SetTargetEnd(end)

        self.ReplaceTarget(self.GetTextRange(pos+1, end).lstrip())

        pos = pos + 1
        self.GotoPos(pos)
        x = 0
        while x < numtabs:
            self.AddText(self.addchar)
            x = x + 1
        #/Auto Indent Code

        #Ensure proper keyboard navigation:
        self.CmdKeyExecute(wx.stc.STC_CMD_CHARLEFT)
        self.CmdKeyExecute(wx.stc.STC_CMD_CHARRIGHT)

    def CheckIndentationFor(self, type):
        text = self.GetText()
        if not text:
            return False

        if type == -1:
            return (self.respaces.search(text) is not None)
        else:
            return (self.retab.search(text) is not None)

    def EnsureVisible(self, linenumber):
        if self.grandparent.prefs.docfolding[self.filetype]:
            wx.stc.StyledTextCtrl.EnsureVisible(self, linenumber)

    def GetEncoding(self):
        return self.encoding

    def GetIndentationString(self):
        return self.addchar

    def GetIndentationEventText(self):
        cline, cpos = self.GetCurLine()
        nextline = self.GetLine(self.LineFromPosition(cpos)+1)

        return cline + nextline

    def GetFilename(self):
        if self.filename:
            return self.filename
        return "Untitled " + str(self.untitlednumber)

    def GetFilenameTitle(self):
        if self.filename:
            return os.path.split(self.filename)[1]
        return "Untitled " + str(self.untitlednumber)

    def OnModified(self, event):
        if self.DynamicScript:
            return
        if not self.IsSplitView:
            if self.grandparent.prefs.sourcebrowserautorefresh:
                if self.grandparent.SourceBrowser is not None:
                    self.grandparent.SourceBrowser.Browse()
            modify = self.GetModify()
            if (modify != self.modified) or (event is None):
                self.modified = modify
                if self.modified:
                    if self.IsActive:
                        self.notebookparent.SetPageImage(self.targetPosition, 3)
                    else:
                        self.notebookparent.SetPageImage(self.targetPosition, 1)
                    if not self.filename:
                        self.notebookparent.SetPageText(self.targetPosition, "Untitled " + str(self.untitlednumber))
                        self.grandparent.SetTitle("DrPython - Untitled " + str(self.untitlednumber) + ' [Modified]')
                    elif self.grandparent.GetTitle().find('[Modified]') == -1:
                        self.notebookparent.SetPageText(self.targetPosition, os.path.basename(self.filename))
                        self.grandparent.SetTitle("DrPython - " + self.filename + " [Modified]")
                else:
                    if self.IsActive:
                        self.notebookparent.SetPageImage(self.targetPosition, 2)
                    else:
                        self.notebookparent.SetPageImage(self.targetPosition, 0)
                    self.SetSavePoint()
                    if not self.filename:
                        self.notebookparent.SetPageText(self.targetPosition, "Untitled " + str(self.untitlednumber))
                        self.grandparent.SetTitle("DrPython - Untitled " + str(self.untitlednumber))
                    else:
                        self.notebookparent.SetPageText(self.targetPosition, os.path.basename(self.filename))
                        self.grandparent.SetTitle("DrPython - " + self.filename)

        if self.grandparent.prefs.docupdateindentation:
            #If deleting text, or undo/redo:
            if event is not None:
                modtype = event.GetModificationType()
                if (modtype & wx.stc.STC_MOD_DELETETEXT) or (modtype & wx.stc.STC_PERFORMED_UNDO) or \
                (modtype & wx.stc.STC_PERFORMED_REDO):
                    if (self.indentationtype == 0) or (self.indentationtype == 2):
                        result = self.CheckIndentation(self.GetText())
                    else:
                        hasit = self.CheckIndentationFor(self.indentationtype)
                        result = self.CheckIndentation(self.GetIndentationEventText())
                        if (result != self.indentationtype) and (result != 2):
                            result = 0
                        elif hasit:
                            result = self.indentationtype
                        else:
                            result = 2
                    self.indentationtype = result
                    self.setIndentationString()
                    return
                else:
                    result = self.CheckIndentation(self.GetIndentationEventText())
            else:
                result = self.CheckIndentation(self.GetText())

            if (result != self.indentationtype) and (result != 2):
                if (self.indentationtype == 0) or (result == 0) or \
                ((self.indentationtype + result) == 0):
                    self.indentationstring = "->MIXED"
                    result = 0
                else:
                    if result == -1:
                        self.indentationstring = "->SPACES"
                    elif result == 1:
                        self.indentationstring = "->TABS"
                self.indentationtype = result
            else:
                self.setIndentationString()
        else:
            self.indentationstring = ""

        if event is None:
            try:
                self.OnPositionChanged(None)
            except:
                pass

    def OnPositionChanged(self, event):
        if self.lineendingsaremixed:
            eolmodestr = "MIXED: "
        else:
            eolmodestr = ''
        emode = self.GetEOLMode()
        if emode == wx.stc.STC_EOL_CR:
            eolmodestr += "MAC"
        elif emode == wx.stc.STC_EOL_CRLF:
            eolmodestr += "WIN"
        else:
            eolmodestr += "UNIX"

        if self.GetOvertype():
            ovrstring = "OVR"
        else:
            ovrstring = "INS"

        self.grandparent.SetStatusText(("Line: %(line)s, Col: %(col)s   %(mode)s   %(ovrstring)s   %(ind)s" \
        % {"line": self.GetCurrentLine()+1, "col": self.GetColumn(self.GetCurrentPos()), \
        "mode": eolmodestr, "ovrstring": ovrstring, "ind": self.indentationstring}), 1)

        if event is not None:
            event.Skip()

    def OnUpdateUI(self, event):
        if (self.usestyles) and (self.grandparent.prefs.docparenthesismatching):
            #Code for parenthesis matching from wxPython Demo.
            # check for matching braces
            braceAtCaret = -1
            braceOpposite = -1
            charBefore = None
            caretPos = self.GetCurrentPos()

            if caretPos > 0:
                charBefore = self.GetCharAt(caretPos - 1)
                styleBefore = self.GetStyleAt(caretPos - 1)

            # check before
            if charBefore and chr(charBefore) in "[]{}()" and styleBefore == wx.stc.STC_P_OPERATOR:
                braceAtCaret = caretPos - 1

            # check after
            if braceAtCaret < 0:
                charAfter = self.GetCharAt(caretPos)
                styleAfter = self.GetStyleAt(caretPos)

                if charAfter and chr(charAfter) in "[]{}()" and styleAfter == wx.stc.STC_P_OPERATOR:
                    braceAtCaret = caretPos

            if braceAtCaret >= 0:
                braceOpposite = self.BraceMatch(braceAtCaret)

            if braceAtCaret != -1  and braceOpposite == -1:
                self.BraceBadLight(braceAtCaret)
            else:
                self.BraceHighlight(braceAtCaret, braceOpposite)
        event.Skip()

    def OnKeyDown(self, event):
        result = self.grandparent.RunShortcuts(event, self, self.DisableShortcuts)
        if result > -1:
            if (result == wx.stc.STC_CMD_NEWLINE) and (self.grandparent.prefs.docautoindent):
                self._autoindent()
            if result == wx.stc.STC_CMD_TAB:
                #Check Indentation for trailing spaces
                pos = self.GetCurrentPos()

                linenumber = self.LineFromPosition(pos)
                lpos = pos - self.PositionFromLine(linenumber) - 1

                #Only at the end of a line.
                end = self.GetLineEndPosition(linenumber)
                if pos != end:
                    return

                ltext = self.GetLine(linenumber).rstrip(self.GetEndOfLineCharacter())

                #only proceed if the text up to this point is whitespace.
                if self.renonwhitespace.search(ltext[:lpos]) is not None:
                    return

                #Get the position of where the full indentation ends:
                lnws = len(ltext.rstrip())
                fiendsat = lnws + (ltext[lnws:].count(self.addchar) * len(self.addchar))

                #Get the diff betwixt this and the current pos:
                difftwixt = len(ltext) - fiendsat

                if difftwixt > 0:
                    #Check to make sure you are just looking at spaces:
                    target = ltext[fiendsat:]
                    for a in target:
                        if a != ' ':
                            return

                    #Remove the extra spaces
                    self.SetTargetStart(pos - difftwixt)
                    self.SetTargetEnd(pos)
                    self.ReplaceTarget('')
                    #/Check Indentation for trailing spaces
            elif result == wx.stc.STC_CMD_DELETEBACK:
                #if self.indentationtype == -1:
                if self.indentationtype == -1 and self.grandparent.prefs.docuseintellibackspace[self.filetype]:
                    pos = self.GetCurrentPos() - 1
                    if chr(self.GetCharAt(pos)) == ' ':
                        x = 0
                        l = self.grandparent.prefs.doctabwidth[self.filetype]
                        while x < l:
                            c = chr(self.GetCharAt(pos))
                            if c == ' ':
                                self.CmdKeyExecute(wx.stc.STC_CMD_DELETEBACK)
                            else:
                                x = l
                            x += 1
                            pos = pos - 1
                    else:
                        event.Skip()
                else:
                    event.Skip()

    def OnMarginClick(self, event):
        # fold and unfold as needed
        if event.GetMargin() == 2:
            lineClicked = self.LineFromPosition(event.GetPosition())
            if self.GetFoldLevel(lineClicked) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                self.ToggleFold(lineClicked)

    def SetEncoding(self, encoding):
        self.encoding = encoding

    def setIndentationString(self):
        if self.indentationtype == 2:
            self.indentationstring = "->NONE"
        elif self.indentationtype == 1:
            self.indentationstring = "->TABS"
        elif self.indentationtype == 0:
            self.indentationstring = "->MIXED"
        elif self.indentationtype == -1:
            self.indentationstring = "->SPACES"

    def SetupLineNumbersMargin(self):
        if self.grandparent.prefs.docshowlinenumbers:
            linecount = self.GetLineCount()
            if linecount < 1000:
                linecount = 1000
            lstring = str(linecount * 100)
            textwidth = self.TextWidth(wx.stc.STC_STYLE_LINENUMBER, drEncoding.EncodeText(self.grandparent, lstring, self.encoding))
            self.SetMarginWidth(1, textwidth)
        else:
            self.SetMarginWidth(1, 0)

    def SetupPrefsDocument(self, notmdiupdate = 1):
        if self.grandparent.prefs.doconlyusedefaultsyntaxhighlighting:
            self.filetype = self.grandparent.prefs.docdefaultsyntaxhighlighting
        self.SetEndAtLastLine(not self.grandparent.prefs.docscrollextrapage)
        self.SetIndentationGuides(self.grandparent.prefs.docuseindentationguides)
        if (len(self.filename) == 0) and not self.GetModify():
            self.SetupTabs(self.indentationtype == 1)
        if self.grandparent.prefs.docfolding[self.filetype]:
            self.grandparent.viewmenu.Enable(self.grandparent.ID_FOLDING, True)
            self.SetMarginWidth(2, 12)
            self.SetMarginSensitive(2, True)
            self.SetProperty("fold", "1")
        else:
            self.grandparent.viewmenu.Enable(self.grandparent.ID_FOLDING, False)
            self.SetMarginWidth(2, 0)
            self.SetMarginSensitive(2, False)
            self.SetProperty("fold", "0")

        #LongLineCol from Chris McDonough

        #Adding if statement, else section myself, also added code to use line and/or background method:
        #I put the set edge color section in under styles.

        if self.grandparent.prefs.doclonglinecol > 0:
            self.SetEdgeColumn(self.grandparent.prefs.doclonglinecol)
            self.SetEdgeMode(wx.stc.STC_EDGE_LINE)
        elif self.grandparent.prefs.doclonglinecol < 0:
            self.SetEdgeColumn(abs(self.grandparent.prefs.doclonglinecol))
            self.SetEdgeMode(wx.stc.STC_EDGE_BACKGROUND)
        else:
            self.SetEdgeMode(wx.stc.STC_EDGE_NONE)

        #/LongLineCol from Chris McDonough

        self.SetupLineNumbersMargin()

        if notmdiupdate:
            self.SetViewWhiteSpace(self.grandparent.prefs.docwhitespaceisvisible)
            self.SetViewEOL(self.grandparent.prefs.docwhitespaceisvisible and self.grandparent.prefs.vieweol)

        self.SetTabWidth(self.grandparent.prefs.doctabwidth[self.filetype])

        if self.grandparent.prefs.docwordwrap[self.filetype]:
            self.SetWrapMode(wx.stc.STC_WRAP_WORD)
        else:
            self.SetWrapMode(wx.stc.STC_WRAP_NONE)

        self.SetKeyWords(0, drKeywords.GetKeyWords(self.filetype))

        self.SetLexer(drKeywords.GetLexer(self.filetype))

        indentguide = wx.LIGHT_GREY

        if (self.filetype == 0) or (self.filetype == 3):
            self.grandparent.prefs.txtDocumentStyleDictionary = self.grandparent.prefs.PythonStyleDictionary
            cursorstyle = self.grandparent.prefs.txtDocumentStyleDictionary[15]
            foldingstyle = self.grandparent.prefs.txtDocumentStyleDictionary[17]
            self.SetEdgeColour(self.grandparent.prefs.txtDocumentStyleDictionary[18])
            highlightlinestyle = self.grandparent.prefs.txtDocumentStyleDictionary[19]
            indentguide = self.grandparent.prefs.txtDocumentStyleDictionary[20]
        elif self.filetype == 1:
            self.grandparent.prefs.txtDocumentStyleDictionary = self.grandparent.prefs.CPPStyleDictionary
            cursorstyle = self.grandparent.prefs.txtDocumentStyleDictionary[17]
            foldingstyle = self.grandparent.prefs.txtDocumentStyleDictionary[19]
            self.SetEdgeColour(self.grandparent.prefs.txtDocumentStyleDictionary[20])
            highlightlinestyle = self.grandparent.prefs.txtDocumentStyleDictionary[21]
        elif self.filetype == 2:
            self.grandparent.prefs.txtDocumentStyleDictionary = self.grandparent.prefs.HTMLStyleDictionary
            cursorstyle = self.grandparent.prefs.txtDocumentStyleDictionary[18]
            foldingstyle = self.grandparent.prefs.txtDocumentStyleDictionary[20]
            self.SetEdgeColour(self.grandparent.prefs.txtDocumentStyleDictionary[21])
            highlightlinestyle = self.grandparent.prefs.txtDocumentStyleDictionary[22]

        #Folding:
        foldback = getStyleProperty("back", foldingstyle)
        foldfore = getStyleProperty("fore", foldingstyle)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED, foldback, foldfore)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, foldback, foldfore)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER, foldback, foldfore)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,wx.stc.STC_MARK_LCORNER, foldback, foldfore)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE, foldback, foldfore)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,wx.stc.STC_MARK_BOXPLUS, foldback, foldfore)
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,wx.stc.STC_MARK_BOXMINUS, foldback, foldfore)

        #Margin:
        self.marginbackground = foldback
        self.marginforeground = foldfore

        if self.grandparent.prefs.docusestyles:

            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, self.grandparent.prefs.txtDocumentStyleDictionary[0])

            self.StyleClearAll()

            self.StartStyling(0, 0xff)

            self.SetCaretForeground(cursorstyle)

            if self.grandparent.prefs.dochighlightcurrentline:
                self.SetCaretLineBack(highlightlinestyle)
                self.SetCaretLineVisible(True)
            else:
                self.SetCaretLineVisible(False)

            self.SetCaretWidth(self.grandparent.prefs.doccaretwidth)

            self.StyleSetForeground(wx.stc.STC_STYLE_INDENTGUIDE, indentguide)

            if (self.grandparent.prefs.docusestyles < 2) or (not self.filetype == 4):
                self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, self.grandparent.prefs.txtDocumentStyleDictionary[1])
                self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, self.grandparent.prefs.txtDocumentStyleDictionary[2])
                self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, self.grandparent.prefs.txtDocumentStyleDictionary[3])
                drKeywords.SetSTCStyles(self.grandparent, self, self.filetype)

    def SetTargetPosition(self, pos):
        self.targetPosition = pos

    def FoldAll(self, expanding):
        lineCount = self.GetLineCount()

        #Yup, this is different from the  demo.py stuff.
        #This is a really messed up hack of the pype.py and demo.py stuff to act
        #the way I want it to...
        #Folding is just ugly.

        #Set stuff up first...
        lines = []
        #franz: lineNum not referenced
        for line in xrange(lineCount):
            lines.append(line)
        lines.reverse()

        if not expanding:
            #Code Inspired by pype.py...Wake wx.stc.STC Up Before we fold!
            self.HideLines(0, lineCount-1)
            wx.Yield()
            self.ShowLines(0, lineCount-1)

            for line in xrange(lineCount):
                if self.GetFoldLevel(line) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                    self.SetFoldExpanded(line, 1)

        #Back to demo.py...mmmm, open source...Modified ever so slightly

        if expanding:
            #Modify the demo.py stuff to act like pype.py:
            for line in lines:
                a = self.GetLastChild(line, -1)
                self.ShowLines(line+1,a)
                self.SetFoldExpanded(line, True)
        else:
            #Get pype.py funky(Ever so slightly modified old bean)!
            for line in lines:
                a = self.GetLastChild(line, -1)
                self.HideLines(line+1,a)
                self.SetFoldExpanded(line, False)

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        #From demo.py (pype.py 1.1.8 uses it too!)
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels-1)
                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1
        return line
