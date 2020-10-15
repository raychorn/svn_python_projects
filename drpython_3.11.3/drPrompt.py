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

#The Prompt

import os.path, re
import wx
import wx.stc
from drProperty import *
import drEncoding
import drKeywords
import drSTC

reserved = [wx.stc.STC_CMD_NEWLINE, wx.stc.STC_CMD_CHARLEFT,
wx.stc.STC_CMD_CHARRIGHT, wx.stc.STC_CMD_LINEUP, wx.stc.STC_CMD_LINEDOWN,
wx.stc.STC_CMD_DELETEBACK, wx.stc.STC_CMD_HOME]

class DrPrompt(drSTC.DrStyledTextControl):
    def __init__(self, parent, id, grandparent):
        drSTC.DrStyledTextControl.__init__(self, parent, id, grandparent)

        #Maximum Number of Commands to Keep Track of in Prompt
        self.MAX_PROMPT_COMMANDS = 25
        self.CommandArray = []
        self.CommandArrayPos = -1

        self.IsAPrompt = True

        self.editpoint = 0

        #Process
        self.process = None
        self.pid = -1
        self.pythonintepreter = 0

        self.commandinprogress = False

        #Goto Traceback:
        self.reTFilename = re.compile('\".*\"')
        #self.reTLinenumber = re.compile('line.*\d')
        #AB:
        self.reTLinenumber = re.compile('line \d+')

        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.foundvalidline = False

        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnModified, id=id)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_UPDATE_UI,  self.RunCheck, id=id)

        #Horrible hack by AB:
        #I don't know why, but on Linux wx.EVT_IDLE doesn't work without focus
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_TIMER, self.OnIdle)
            self.t1 = wx.Timer(self)
            self.t1.Start(500)
        else:
            self.Bind(wx.EVT_IDLE, self.OnIdle)
        #End AB
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnGotoSelectedLine)

    def _addoutput(self, checkinput=True):
        wx.Usleep(25)
        a = ''
        if checkinput and self.process.IsInputAvailable():
            a = self._getoutput(self.inputstream)
        if self.process.IsErrorAvailable():
            a += self._getoutput(self.errorstream)
        self.AddText(a)
        return a

    def _getoutput(self, targetstream):
        #used to get the output of a command in the prompt, and immediately add it to the prompt.
        added = False
        while not added:
            if targetstream.CanRead():
                text = targetstream.read()
                added = True
        return text

    def _waitforoutput(self, targetoutput):
        '''
        Dangerous!  Only use this if you know what you are doing.
        Waits for output that has not yet appeared to show up
        in either the stdout or stderr of the current process.
        '''

        # For some reasons, sometimes the python interpreter hangs,
        # waiting for something to read on stdin.
        # To solve this problems, we write an extra EOL on stdin
        self.outputstream.write('\n') #patch by Luca Falavigna - dktrkranz, 07/04/2008, thanks
        text = ''
        while True:
            if text.find(targetoutput) > -1:
                return
            #patch [ 1356168 ] Python and Import All Sometimes Jam Up
            #reverting: this freezes the pc.
#            while text.find(targetoutput) < 0:
#                wx.Yield()
            text = self._addoutput()

    def AddEncodedText(self, text):
        try:
            etext = drEncoding.EncodeText(self.grandparent, text)
            wx.stc.StyledTextCtrl.AddText(self, etext)
        except:
            print 'Error Encoding Text'

    def AddText(self, text):
        ro = self.GetReadOnly()
        self.SetReadOnly(0)
        self.AddEncodedText(text)
        self.SetReadOnly(ro)

    def ExecuteCommands(self, text):
        '''Executes Commands Separated by '\n' '''
        if not text:
            return
        self._addoutput()
        self.commandinprogress = True
        text = text.rstrip()
        commands = text.split('\n')
        for command in commands:
            command += '\n'
            self._addoutput()
            try:
                etext = drEncoding.EncodeText(self.grandparent, command)
            except:
                print 'Error Encoding Text'
                return
            self.outputstream.write(etext)
            self.GotoPos(self.GetLength())
            wx.stc.StyledTextCtrl.AddText(self, etext)
            self._addoutput((len(command) > 1))
            self.editpoint = self.GetLength()
            self.ScrollToLine(self.LineFromPosition(self.editpoint))
        self.commandinprogress = False

    def GetEditPoint(self):
        return self.editpoint

    def InsertEncodedText(self, pos, text):
        try:
            etext = drEncoding.EncodeText(self.grandparent, text)
            wx.stc.StyledTextCtrl.InsertText(self, pos, etext)
        except:
            print 'Error Encoding Text'

    def InsertText(self, pos, text):
        ro = self.GetReadOnly()
        self.SetReadOnly(0)
        self.InsertEncodedText(pos, text)
        self.SetReadOnly(ro)

    def OnIdle(self, event):
        if (self.process is not None) and (not self.commandinprogress):
            if self.inputstream.CanRead():
                text = self.inputstream.read()
                self.AddEncodedText(text)
                self.EmptyUndoBuffer()
                self.editpoint = self.GetLength()
                self.GotoPos(self.editpoint)
                self.ScrollToLine(self.LineFromPosition(self.editpoint))
            if self.errorstream.CanRead():
                text = self.errorstream.read()
                self.AddEncodedText(text)
                self.EmptyUndoBuffer()
                self.editpoint = self.GetLength()
                self.GotoPos(self.editpoint)
                self.ScrollToLine(self.LineFromPosition(self.editpoint))

    def OnGotoSelectedLine(self, event):
        self.foundvalidline = False

        self.grandparent.PPost(self.grandparent.EVT_DRPY_PROMPT_GOTO)

        line = self.GetLine(self.GetCurrentLine())

        #pattern for lua error output?
        if not self.foundvalidline:
            #lua: .../path/../filename.lua:180: attempt to call ...
            root, ext = os.path.splitext(self.grandparent.txtDocument.filename)
            if ext == '.lua':
                if line.startswith("lua: "):
                    findpattern = "lua:"
                    pos = line.rfind(findpattern)
                    if pos != -1:
                        pos1 = pos + len(findpattern)
                        pos2 = line[pos1:].find(':')
                        if pos2 != -1:
                            self.gotolinenumber = int (line[pos1 : pos1 + pos2]) - 1
                            self.foundvalidline = True
                            self.gotofilename = self.grandparent.txtDocument.filename
                            #if another file is imported, this could be processed more accurate
                

        #pattern for traceback?
        if not self.foundvalidline:
          fn = self.reTFilename.search(line)
          ln = self.reTLinenumber.search(line)
          if (fn is not None) and (ln is not None):
              self.foundvalidline = True
              self.gotofilename = fn.group().strip('\"')
              try:
                  self.gotolinenumber = int(ln.group().strip('line ')) - 1
              except:
                  self.gotolinenumber = 0
        
        #pattern for pycheckeroutput?
        if not self.foundvalidline:
            line = line.replace ('\\', '/')
            pos = line.find (': ')
            if pos > -1:
                s = line[:pos]
                split = s.rsplit(':', 1)
                if len (split):
                    self.foundvalidline = True
                    self.gotofilename = split[0]
                    try:
                        self.gotolinenumber = int(split[1]) - 1
                    except:
                        self.gotolinenumber = 0
                   
                
        if self.foundvalidline:
            if os.path.exists(self.gotofilename):
                self.grandparent.OpenOrSwitchToFile(self.gotofilename, editRecentFiles=False)

                #self.grandparent.txtDocument.ScrollToLine(linenumber)
                #patch: [ 1366679 ] Goto Line Should Not Display At Top Of Window
                top = self.gotolinenumber - self.grandparent.txtDocument.LinesOnScreen()/2
                if top < 0:
                    top = 0
                self.grandparent.txtDocument.ScrollToLine(top)
                
                self.grandparent.txtDocument.GotoLine(self.gotolinenumber)
                self.grandparent.txtDocument.EnsureCaretVisible()
                self.grandparent.txtDocument.SetFocus()

    def CheckAndCorrectAsciiText(self, text):
        newtext = str()
        corrected = False
        for c in text:
            if ord(c) > 127:
                c = '-'
                corrected = True
            newtext = newtext + c
        return newtext, corrected
    
    def OnKeyDown(self, event):
        if self.pid == -1:
            return
        result = self.grandparent.RunShortcuts(event)
        if result > -1:
            pos = self.GetCurrentPos()
            if not self.pid == -1:
                if (pos >= self.editpoint) and (result == wx.stc.STC_CMD_NEWLINE):
                    self.commandinprogress = True

                    text = self.GetTextRange(self.editpoint, self.GetLength())
                    l = len(self.CommandArray)
                    if l < self.MAX_PROMPT_COMMANDS:
                        if text in self.CommandArray:
                            self.CommandArray.pop(self.CommandArray.index(text))
                        self.CommandArray.insert(0, text)
                        self.CommandArrayPos = -1
                    else:
                        self.CommandArray.pop()
                        self.CommandArray.insert(0, text)
                        self.CommandArrayPos = -1
                    if not text:
                        text = '\n'
                        self.GotoPos(self.GetLength())
                        self.AddText(self.GetEndOfLineCharacter())
                    elif text[-1] != '\n':
                        text += '\n'
                        self.GotoPos(self.GetLength())
                        self.AddText(self.GetEndOfLineCharacter())
                    try:
                        etext = drEncoding.EncodeText(self.grandparent, text)
                    except:
                        print 'Error Encoding Text'
                        return

                    #ugly hack, but otherwise, drpython crashes
                    etext, corrected = self.CheckAndCorrectAsciiText(etext)
                    if corrected:
                        self.grandparent.ShowMessage("Sorry, only ascii codes until 127 possible.\nOtherwiese the program crashes", "DrPython Error")
                    
                    self.outputstream.write(etext)
                    self.GotoPos(self.GetLength())
                    self._addoutput()

                    self.editpoint = self.GetLength()
                    self.ScrollToLine(self.LineFromPosition(self.editpoint))
                    self.commandinprogress = False
                elif result == wx.stc.STC_CMD_LINEUP:
                    l = len(self.CommandArray)
                    if self.CommandArray:
                        if (self.CommandArrayPos + 1) < l:
                            self.GotoPos(self.editpoint)
                            self.SetTargetStart(self.editpoint)
                            self.SetTargetEnd(self.GetLength())
                            self.CommandArrayPos = self.CommandArrayPos + 1
                            self.ReplaceTarget(self.CommandArray[self.CommandArrayPos])

                elif result == wx.stc.STC_CMD_LINEDOWN:
                    if (len(self.CommandArray) > 0):
                        self.GotoPos(self.editpoint)
                        self.SetTargetStart(self.editpoint)
                        self.SetTargetEnd(self.GetLength())
                        if (self.CommandArrayPos - 1) > -1:
                            self.CommandArrayPos = self.CommandArrayPos - 1
                            self.ReplaceTarget(self.CommandArray[self.CommandArrayPos])
                        else:
                            if (self.CommandArrayPos - 1) > -2:
                                self.CommandArrayPos = self.CommandArrayPos - 1
                            self.ReplaceTarget("")

            if ((pos > self.editpoint) and (result in reserved)) or \
                (pos >= self.editpoint) and (result == wx.stc.STC_CMD_CHARRIGHT):
                event.Skip()

    def OnKeyUp(self, event):
        if self.pid == -1:
            event.Skip()
            return
        keycode = event.GetKeyCode()
        #franz: pos was not used
        if keycode == wx.WXK_HOME:
            if self.GetCurrentPos() < self.editpoint:
                self.GotoPos(self.editpoint)
            return
        elif keycode == wx.WXK_PRIOR:
            if self.GetCurrentPos() < self.editpoint:
                self.GotoPos(self.editpoint)
            return
        if keycode == wx.WXK_RETURN: #patch from merwinb, 2009-0728, thanks (Prompt window scrolls to wrong position)
            self.GotoPos(self.GetCurrentPos())
        event.Skip()

    def OnModified(self, event):
        if not (self.grandparent.prefs.promptwordwrap):
            ll = self.TextWidth(wx.stc.STC_STYLE_DEFAULT, "OOO")
            x = 0
            spaces = ""
            while x < self.grandparent.prefs.prompttabwidth:
                spaces = spaces + " "
                x = x + 1
            current_width = self.GetScrollWidth()
            line = self.GetCurLine()[0].replace('\t', spaces)
            actual_width = self.TextWidth(wx.stc.STC_STYLE_DEFAULT, line)
            if current_width < actual_width:
                self.SetScrollWidth(actual_width + ll)

    def RunCheck(self, event):
        if (self.GetCurrentPos() < self.editpoint) or (self.pid == -1):
            self.SetReadOnly(1)
        else:
            self.SetReadOnly(0)

    def SetupPrefsPrompt(self, notmdiupdate = 1):
        self.SetEndAtLastLine(not self.grandparent.prefs.promptscrollextrapage)

        if notmdiupdate:
            self.SetViewWhiteSpace(self.grandparent.prefs.promptwhitespaceisvisible)
            self.SetViewEOL(self.grandparent.prefs.promptwhitespaceisvisible and self.grandparent.prefs.vieweol)

        if self.grandparent.prefs.promptwordwrap:
            self.SetWrapMode(wx.stc.STC_WRAP_WORD)
        else:
            self.SetWrapMode(wx.stc.STC_WRAP_NONE)
        if self.grandparent.prefs.prompteolmode == 1:
            self.SetEOLMode(wx.stc.STC_EOL_CRLF)
        elif self.grandparent.prefs.prompteolmode == 2:
            self.SetEOLMode(wx.stc.STC_EOL_CR)
        else:
            self.SetEOLMode(wx.stc.STC_EOL_LF)
        self.SetTabWidth(self.grandparent.prefs.prompttabwidth)
        self.SetUseTabs(self.grandparent.prefs.promptusetabs)
        self.SetMarginWidth(1, self.grandparent.prefs.promptmarginwidth)

        if self.grandparent.prefs.promptusestyles:

            self.SetKeyWords(0, drKeywords.GetKeyWords(0))

            self.SetLexer(drKeywords.GetLexer(0))

            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, self.grandparent.prefs.txtPromptStyleDictionary[0])

            self.StyleClearAll()

            self.StartStyling(0, 0xff)

            self.SetCaretWidth(self.grandparent.prefs.promptcaretwidth)

            self.SetCaretForeground(self.grandparent.prefs.txtPromptStyleDictionary[15])

            if self.grandparent.prefs.promptusestyles < 2:
                self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, self.grandparent.prefs.txtPromptStyleDictionary[1])
                self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, self.grandparent.prefs.txtPromptStyleDictionary[2])
                self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, self.grandparent.prefs.txtPromptStyleDictionary[3])
                self.StyleSetSpec(wx.stc.STC_P_CHARACTER, self.grandparent.prefs.txtPromptStyleDictionary[4])
                self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, self.grandparent.prefs.txtPromptStyleDictionary[5])
                self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, self.grandparent.prefs.txtPromptStyleDictionary[6])
                self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, self.grandparent.prefs.txtPromptStyleDictionary[7])
                self.StyleSetSpec(wx.stc.STC_P_DEFNAME, self.grandparent.prefs.txtPromptStyleDictionary[8])
                self.StyleSetSpec(wx.stc.STC_P_WORD, self.grandparent.prefs.txtPromptStyleDictionary[9])
                self.StyleSetSpec(wx.stc.STC_P_NUMBER, self.grandparent.prefs.txtPromptStyleDictionary[10])
                self.StyleSetSpec(wx.stc.STC_P_OPERATOR, self.grandparent.prefs.txtPromptStyleDictionary[11])
                self.StyleSetSpec(wx.stc.STC_P_STRING, self.grandparent.prefs.txtPromptStyleDictionary[12])
                self.StyleSetSpec(wx.stc.STC_P_STRINGEOL, self.grandparent.prefs.txtPromptStyleDictionary[13])
                self.StyleSetSpec(wx.stc.STC_P_TRIPLE, self.grandparent.prefs.txtPromptStyleDictionary[14])
                self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, self.grandparent.prefs.txtPromptStyleDictionary[14])

                self.SetSelForeground(1, getStyleProperty("fore", self.grandparent.prefs.txtPromptStyleDictionary[16]))
                self.SetSelBackground(1, getStyleProperty("back", self.grandparent.prefs.txtPromptStyleDictionary[16]))

    def SetText(self, text):
        ro = self.GetReadOnly()
        self.SetReadOnly(0)
        wx.stc.StyledTextCtrl.SetText(self, text)
        self.SetReadOnly(ro)

    def SetSelectedText(self, text):
        ro = self.GetReadOnly()
        self.SetReadOnly(0)
        self.SetTargetStart(self.GetSelectionStart())
        self.SetTargetEnd(self.GetSelectionEnd())
        self.ReplaceTarget(text)
        self.SetReadOnly(ro)
