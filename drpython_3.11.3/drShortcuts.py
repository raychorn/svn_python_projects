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

#Shortcuts

import re
import wx.stc
import wx

wxKeyDictionary = {wx.WXK_F1:'F1',
wx.WXK_F2:'F2',
wx.WXK_F3:'F3',
wx.WXK_F4:'F4',
wx.WXK_F5:'F5',
wx.WXK_F6:'F6',
wx.WXK_F7:'F7',
wx.WXK_F8:'F8',
wx.WXK_F9:'F9',
wx.WXK_F10:'F10',
wx.WXK_F11:'F11',
wx.WXK_F12:'F12',
wx.WXK_MENU:'Menu',
wx.WXK_PAUSE:'Pause',
wx.WXK_CAPITAL:'CAPS',
wx.WXK_PRIOR:'Page Up',
wx.WXK_NEXT:'Page Down',
wx.WXK_END:'End',
wx.WXK_HOME:'Home',
wx.WXK_LEFT:'Left',
wx.WXK_UP:'Up',
wx.WXK_RIGHT:'Right',
wx.WXK_DOWN:'Down',
wx.WXK_INSERT:'Insert',
wx.WXK_PRINT:'Print',
wx.WXK_BACK:'Backspace',
wx.WXK_TAB:'Tab',
wx.WXK_RETURN:'Enter',
wx.WXK_ESCAPE:'Esc',
wx.WXK_SPACE:'Space',
wx.WXK_DELETE:'Delete',
wx.WXK_ADD:'+',
wx.WXK_SUBTRACT:'-',
wx.WXK_SEPARATOR:'_',
wx.WXK_MULTIPLY:'*',
wx.WXK_DIVIDE:'/',
wx.WXK_ADD:'+',
wx.WXK_NUMPAD_SPACE:'Numpad Space',
wx.WXK_NUMPAD_TAB:'Numpad Tab',
wx.WXK_NUMPAD_ENTER:'Enter',
wx.WXK_NUMPAD_F1:'Numpad F1',
wx.WXK_NUMPAD_F2:'Numpad F2',
wx.WXK_NUMPAD_F3:'Numpad F3',
wx.WXK_NUMPAD_F4:'Numpad F4',
wx.WXK_NUMPAD_HOME:'Numpad Home',
wx.WXK_NUMPAD_LEFT:'Numpad Left',
wx.WXK_NUMPAD_UP:'Numpad Up',
wx.WXK_NUMPAD_RIGHT:'Numpad Right',
wx.WXK_NUMPAD_DOWN:'Numpad Down',
wx.WXK_NUMPAD_PRIOR:'Numpad Page Up',
wx.WXK_NUMPAD_PAGEUP:'Numpad Page Up',
wx.WXK_NUMPAD_NEXT:'Numpad Page Down',
wx.WXK_NUMPAD_PAGEDOWN:'Numpad Page Down',
wx.WXK_NUMPAD_END:'Numpad End',
wx.WXK_NUMPAD_BEGIN:'Numpad Begin',
wx.WXK_NUMPAD_INSERT:'Numpad Insert',
wx.WXK_NUMPAD_DELETE:'Numpad Delete',
wx.WXK_NUMPAD_EQUAL:'Numpad =',
wx.WXK_NUMPAD_MULTIPLY:'Numpad *',
wx.WXK_NUMPAD_ADD:'Numpad +',
wx.WXK_NUMPAD_SEPARATOR:'Numpad _',
wx.WXK_NUMPAD_SUBTRACT:'Numpad -',
wx.WXK_NUMPAD_DECIMAL:'Numpad .',
wx.WXK_NUMPAD_DIVIDE:'Numpad /'}

recontrol = re.compile('Control')
reshift = re.compile('Shift')
realt = re.compile('Alt')
remeta = re.compile('Meta')
rekeycode = re.compile('\d+')

def MatchControl(shortcut):
    return recontrol.search(shortcut) is not None

def MatchShift(shortcut):
    return reshift.search(shortcut) is not None

def MatchAlt(shortcut):
    return realt.search(shortcut) is not None

def MatchMeta(shortcut):
    return remeta.search(shortcut) is not None

def BuildShortcutString(keycode, control, shift, alt, meta):
    keystr = ""

    if control:
        keystr = "Control"
    if shift:
        keystr = keystr + "Shift"
    if alt:
        keystr = keystr + "Alt"
    if meta:
        keystr = keystr + "Meta"
    keystr = keystr + str(keycode)

    return keystr

def GetKeycodeStringFromShortcut(shortcut):
    kstr = rekeycode.search(shortcut)
    if kstr is not None:
        return kstr.group()
    return ''

def GetKeycodeFromShortcut(shortcut):
    kstr = rekeycode.search(shortcut)
    if kstr is not None:
        try:
            k = int(kstr.group())
        except:
            return 0
        return k
    return 0

def GetShortcutLabel(shortcut):
    label = ''

    if MatchControl(shortcut):
        label += 'Ctrl+'
    if MatchShift(shortcut):
        label += 'Shift+'
    if MatchAlt(shortcut):
        label += 'Alt+'
    if MatchMeta(shortcut):
        label += 'Meta+'

    try:
        kc = GetKeycodeFromShortcut(shortcut)
    except:
        return ''

    if wxKeyDictionary.has_key(kc):
        label += wxKeyDictionary[kc]
        return label

    if kc < 128:
        label += chr(kc)
        return label

    return ''


def GetDefaultSTCShortcut(stcindex):
    shortcut = [
    ["Back Tab", wx.WXK_TAB, "Shift"],
    ["Cancel", wx.WXK_ESCAPE, ""],
    ["Char Left", wx.WXK_LEFT, ""],
    ["Char Left Extend", wx.WXK_LEFT, "Shift"],
    ["Char Left Rect Extend", wx.WXK_LEFT, "Shift, Alt"],
    ["Char Right", wx.WXK_RIGHT, ""],
    ["Char Right Extend", wx.WXK_RIGHT, "Shift"],
    ["Char Right Rect Extend", wx.WXK_RIGHT, "Shift, Alt"],
    ["Copy", ord('C'), "Control"],
    ["Cut", ord('X'), "Control"],
    ["Delete", wx.WXK_DELETE, ""],
    ["Delete Back", wx.WXK_BACK, ""],
    ["Delete Back Not Line", wx.WXK_BACK, "Shift"],
    ["Delete Line Left", -1, ""],
    ["Delete Line Right", wx.WXK_DELETE, "Control, Shift"],
    ["Delete Word Left", -1, ""],
    ["Delete Word Right", wx.WXK_DELETE, "Control"],
    ["Document End", wx.WXK_END, "Control"],
    ["Document End Extend", wx.WXK_END, "Control, Shift"],
    ["Document Start", wx.WXK_HOME, "Control"],
    ["Document Start Extend", wx.WXK_HOME, "Control, Shift"],
    ["Form Feed", -1, ""],
    ["Home",-1, ""], # See Visible Character Home
    ["Home Display", wx.WXK_HOME, "Alt"],
    ["Home Display Extend", -1, ""],
    ["Home Extend", wx.WXK_HOME, "Shift"],
    ["Home Rect Extend", wx.WXK_HOME, "Shift, Alt"],
    ["Line Cut", ord('Y'), "Control"],
    ["Line Delete", -1, ""],
    ["Line Down", wx.WXK_DOWN, ""],
    ["Line Down Extend", wx.WXK_DOWN, "Shift"],
    ["Line Down Rect Extend", wx.WXK_DOWN, "Shift, Alt"],
    ["Line Duplicate", ord('D'), "Control"],
    ["Line End", wx.WXK_END, ""],
    ["Line End Display", wx.WXK_END, "Alt"],
    ["Line End Display Extend", -1, ""],
    ["Line End Extend", wx.WXK_END, "Shift"],
    ["Line End Rect Extend", wx.WXK_END, "Shift, Alt"],
    ["Line Scroll Down", wx.WXK_DOWN, "Control"],
    ["Line Scroll Up", wx.WXK_UP, "Control"],
    ["Line Transpose", ord('X'), "Alt"],
    ["Line Up", wx.WXK_UP, ""],
    ["Line Up Extend", wx.WXK_UP, "Shift"],
    ["Line Up Rect Extend", wx.WXK_UP, "Shift, Alt"],
    ["Lowercase", ord('U'), "Control"],
    ["New Line", wx.WXK_RETURN, ""],
    ["Page Down", wx.WXK_NEXT, ""],
    ["Page Down Extend", wx.WXK_NEXT, "Shift"],
    ["Page Down Rect Extend", wx.WXK_NEXT, "Shift, Alt"],
    ["Page Up", wx.WXK_PRIOR, ""],
    ["Page Up Extend", wx.WXK_PRIOR, "Shift"],
    ["Page Up Rect Extend", wx.WXK_PRIOR, "Shift, Alt"],
    ["Paste", ord('V'), "Control"],
    ["Redo", ord('Z'), "Control, Shift"],
    ["Select All", ord('A'), "Control"],
    ["Tab", wx.WXK_TAB, ""],
    ["Toggle Overtype", wx.WXK_INSERT, ""],
    ["Undo", ord('Z'), "Control"],
    ["Uppercase", ord('U'), "Control, Shift"],
    ["Visible Character Home",  wx.WXK_HOME, ""], #Begin of Line
    ["Visible Character Home Extend", -1, ""],
    ["World Left", wx.WXK_LEFT, "Control"],
    ["Word Left Extend", wx.WXK_LEFT, "Control, Shift"],
    ["Word Part Left", wx.WXK_LEFT, "Alt"],
    ["Word Part Left Extend", -1, ""],
    ["Word Part Right", wx.WXK_RIGHT, "Alt"],
    ["Word Part Right Extend", -1, ""],
    ["Word Right", wx.WXK_RIGHT, "Control"],
    ["Word Right Extend", wx.WXK_RIGHT, "Control, Shift"],
    ["Zoom In", ord('+'), "Control"],
    ["Zoom Out", ord('-'), "Control"]
    ][stcindex]

    return (shortcut[2] + str(shortcut[1]))


def GetKeycodeText(keycode):
    wxkeycodes = [wx.WXK_BACK, wx.WXK_TAB, wx.WXK_RETURN, wx.WXK_ESCAPE, wx.WXK_SPACE, wx.WXK_DELETE, wx.WXK_START, wx.WXK_LBUTTON, wx.WXK_RBUTTON, wx.WXK_CANCEL, wx.WXK_MBUTTON, wx.WXK_CLEAR, wx.WXK_SHIFT, wx.WXK_CONTROL, wx.WXK_MENU, wx.WXK_PAUSE, wx.WXK_CAPITAL, wx.WXK_PRIOR, wx.WXK_NEXT, wx.WXK_END, wx.WXK_HOME, wx.WXK_LEFT, wx.WXK_UP, wx.WXK_RIGHT, wx.WXK_DOWN, wx.WXK_SELECT, wx.WXK_PRINT, wx.WXK_EXECUTE, wx.WXK_SNAPSHOT, wx.WXK_INSERT, wx.WXK_HELP, wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2, wx.WXK_NUMPAD3, wx.WXK_NUMPAD4, wx.WXK_NUMPAD5, wx.WXK_NUMPAD6, wx.WXK_NUMPAD7, wx.WXK_NUMPAD8, wx.WXK_NUMPAD9, wx.WXK_MULTIPLY, wx.WXK_ADD, wx.WXK_SEPARATOR, wx.WXK_SUBTRACT, wx.WXK_DECIMAL, wx.WXK_DIVIDE, wx.WXK_F1, wx.WXK_F2, wx.WXK_F3, wx.WXK_F4, wx.WXK_F5, wx.WXK_F6, wx.WXK_F7, wx.WXK_F8, wx.WXK_F9, wx.WXK_F10, wx.WXK_F11, wx.WXK_F12, wx.WXK_F13, wx.WXK_F14, wx.WXK_F15, wx.WXK_F16, wx.WXK_F17, wx.WXK_F18, wx.WXK_F19, wx.WXK_F20, wx.WXK_F21, wx.WXK_F22, wx.WXK_F23, wx.WXK_F24, wx.WXK_NUMLOCK, wx.WXK_SCROLL]
    wxkeynames = ["BACK", "TAB", "RETURN", "ESCAPE", "SPACE", "DELETE", "START", "LBUTTON", "RBUTTON", "CANCEL", "MBUTTON", "CLEAR", "SHIFT", "CONTROL", "MENU", "PAUSE", "CAPITAL", "PRIOR", "NEXT", "END", "HOME", "LEFT", "UP", "RIGHT", "DOWN", "SELECT", "PRINT", "EXECUTE", "SNAPSHOT", "INSERT", "HELP", "NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5", "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9", "MULTIPLY", "ADD", "SEPARATOR", "SUBTRACT", "DECIMAL", "DIVIDE", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24", "NUMLOCK", "SCROLL"]

    try:
        i = wxkeycodes.index(keycode)
        return True, wxkeynames[i]
    except:
        pass

    return False, ""

def GetSTCCommandList():
    return [wx.stc.STC_CMD_BACKTAB, wx.stc.STC_CMD_CANCEL,
    wx.stc.STC_CMD_CHARLEFT, wx.stc.STC_CMD_CHARLEFTEXTEND, wx.stc.STC_CMD_CHARLEFTRECTEXTEND,
    wx.stc.STC_CMD_CHARRIGHT, wx.stc.STC_CMD_CHARRIGHTEXTEND, wx.stc.STC_CMD_CHARRIGHTRECTEXTEND,
    wx.stc.STC_CMD_COPY, wx.stc.STC_CMD_CUT,
    wx.stc.STC_CMD_CLEAR,
    wx.stc.STC_CMD_DELETEBACK, wx.stc.STC_CMD_DELETEBACKNOTLINE,
    wx.stc.STC_CMD_DELLINELEFT, wx.stc.STC_CMD_DELLINERIGHT,
    wx.stc.STC_CMD_DELWORDLEFT, wx.stc.STC_CMD_DELWORDRIGHT,
    wx.stc.STC_CMD_DOCUMENTEND, wx.stc.STC_CMD_DOCUMENTENDEXTEND,
    wx.stc.STC_CMD_DOCUMENTSTART, wx.stc.STC_CMD_DOCUMENTSTARTEXTEND,
    wx.stc.STC_CMD_FORMFEED, wx.stc.STC_CMD_HOME,
    wx.stc.STC_CMD_HOMEDISPLAY, wx.stc.STC_CMD_HOMEDISPLAYEXTEND,
    wx.stc.STC_CMD_HOMEEXTEND, wx.stc.STC_CMD_VCHOMERECTEXTEND, wx.stc.STC_CMD_LINECUT, wx.stc.STC_CMD_LINEDELETE,
    wx.stc.STC_CMD_LINEDOWN, wx.stc.STC_CMD_LINEDOWNEXTEND, wx.stc.STC_CMD_LINEDOWNRECTEXTEND,
    wx.stc.STC_CMD_LINEDUPLICATE, wx.stc.STC_CMD_LINEEND,
    wx.stc.STC_CMD_LINEENDDISPLAY, wx.stc.STC_CMD_LINEENDDISPLAYEXTEND,
    wx.stc.STC_CMD_LINEENDEXTEND, wx.stc.STC_CMD_LINEENDRECTEXTEND, wx.stc.STC_CMD_LINESCROLLDOWN,
    wx.stc.STC_CMD_LINESCROLLUP, wx.stc.STC_CMD_LINETRANSPOSE, wx.stc.STC_CMD_LINEUP,
    wx.stc.STC_CMD_LINEUPEXTEND, wx.stc.STC_CMD_LINEUPRECTEXTEND, wx.stc.STC_CMD_LOWERCASE, wx.stc.STC_CMD_NEWLINE,
    wx.stc.STC_CMD_PAGEDOWN, wx.stc.STC_CMD_PAGEDOWNEXTEND, wx.stc.STC_CMD_PAGEDOWNRECTEXTEND, wx.stc.STC_CMD_PAGEUP,
    wx.stc.STC_CMD_PAGEUPEXTEND, wx.stc.STC_CMD_PAGEUPRECTEXTEND, wx.stc.STC_CMD_PASTE,
    wx.stc.STC_CMD_REDO,
    wx.stc.STC_CMD_SELECTALL,
    wx.stc.STC_CMD_TAB, wx.stc.STC_CMD_EDITTOGGLEOVERTYPE, wx.stc.STC_CMD_UNDO,
    wx.stc.STC_CMD_UPPERCASE,
    wx.stc.STC_CMD_VCHOME, wx.stc.STC_CMD_VCHOMEEXTEND,
    wx.stc.STC_CMD_WORDLEFT,
    wx.stc.STC_CMD_WORDLEFTEXTEND, wx.stc.STC_CMD_WORDPARTLEFT,
    wx.stc.STC_CMD_WORDPARTLEFTEXTEND,
    wx.stc.STC_CMD_WORDPARTRIGHT, wx.stc.STC_CMD_WORDPARTRIGHTEXTEND,
    wx.stc.STC_CMD_WORDRIGHT, wx.stc.STC_CMD_WORDRIGHTEXTEND,
    wx.stc.STC_CMD_ZOOMIN, wx.stc.STC_CMD_ZOOMOUT]

def SetSTCShortcuts(stc, Shortcuts, useDefault = 0):
    #KeycodeArray = []
    wxDefArray = [wx.WXK_DOWN, wx.WXK_UP, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_HOME, wx.WXK_END, wx.WXK_PRIOR,
    wx.WXK_NEXT, wx.WXK_DELETE, wx.WXK_INSERT, wx.WXK_ESCAPE, wx.WXK_BACK, wx.WXK_TAB, wx.WXK_RETURN,
    wx.WXK_ADD, wx.WXK_SUBTRACT, wx.WXK_DIVIDE]
    PreDefArray = [wx.stc.STC_KEY_DOWN, wx.stc.STC_KEY_UP, wx.stc.STC_KEY_LEFT, wx.stc.STC_KEY_RIGHT, wx.stc.STC_KEY_HOME,
    wx.stc.STC_KEY_END, wx.stc.STC_KEY_PRIOR, wx.stc.STC_KEY_NEXT, wx.stc.STC_KEY_DELETE, wx.stc.STC_KEY_INSERT,
    wx.stc.STC_KEY_ESCAPE, wx.stc.STC_KEY_BACK, wx.stc.STC_KEY_TAB, wx.stc.STC_KEY_RETURN, wx.stc.STC_KEY_ADD,
    wx.stc.STC_KEY_SUBTRACT, wx.stc.STC_KEY_DIVIDE]

    #Note:  If stc.CmdKeyAssign is used, then DrPython will never process
    #       that combindation in the keybinding code.

    cmdlist = GetSTCCommandList()

    stc.CmdKeyClearAll()

    x = 0
    l = len(Shortcuts)
    while x < l:
        modifiers = 0

        if useDefault:
            Shortcuts[x] = GetDefaultSTCShortcut(x)

        ikeycode = GetKeycodeFromShortcut(Shortcuts[x])

        if MatchControl(Shortcuts[x]):
            modifiers = modifiers | wx.stc.STC_SCMOD_CTRL
        if MatchShift(Shortcuts[x]):
            modifiers = modifiers | wx.stc.STC_SCMOD_SHIFT
        if MatchAlt(Shortcuts[x]):
            modifiers = modifiers | wx.stc.STC_SCMOD_ALT

        if (ikeycode >= ord('A')) and (ikeycode <= ord('Z')):
            stc.CmdKeyAssign(ikeycode, modifiers, cmdlist[x])
        elif ikeycode in wxDefArray:
            i = wxDefArray.index(ikeycode)
            stc.CmdKeyAssign(PreDefArray[i], modifiers, cmdlist[x])
        x = x + 1

    return Shortcuts

def SetShortcuts(frame, Shortcuts, ShortcutNames, useDefault=0):

    shortcutsActionArray = []
    shortcutsArgumentsArray = []

    l = len(Shortcuts)
    x = 0
    while x < l:
        #File
        if(ShortcutNames[x] == "New"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('N'))
            shortcutsActionArray.append(frame.OnNew)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Open"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('O'))
            shortcutsActionArray.append(frame.OnOpen)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Open Imported Module"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('M'))
            shortcutsActionArray.append(frame.OnOpenImportedModule)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Save"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('S'))
            shortcutsActionArray.append(frame.OnSave)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Save As"):
            shortcutsActionArray.append(frame.OnSaveAs)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Save All Documents"):
            shortcutsActionArray.append(frame.OnSaveAll)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Save Prompt Output To File"):
            shortcutsActionArray.append(frame.OnSavePrompt)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Reload File"):
            shortcutsActionArray.append(frame.OnReload)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Restore From Backup"):
            shortcutsActionArray.append(frame.OnRestoreFromBackup)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Close"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('W'))
            shortcutsActionArray.append(frame.OnClose)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Close All Documents"):
            shortcutsActionArray.append(frame.OnCloseAllDocuments)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Close All Other Documents"):
            shortcutsActionArray.append(frame.OnCloseAllOtherDocuments)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Print Setup"):
            shortcutsActionArray.append(frame.OnPrintSetup)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Print File"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('P'))
            shortcutsActionArray.append(frame.OnPrint)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Print Prompt"):
            if useDefault:
                Shortcuts[x] = 'ControlShift' + str(ord('P'))
            shortcutsActionArray.append(frame.OnPrintPrompt)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Exit"):
            #applied patch from Cedric Delfosse (cdelfosse) of bug tracker : [ 1214909 ], on 11.04.2007:
            #ctrl_q_to_exit_as_default_shortcut.patch
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('Q'))
            shortcutsActionArray.append(frame.OnExit)
            shortcutsArgumentsArray.append("frame, event")

        #Tabs
        elif(ShortcutNames[x] == "Next Document"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F10)
            shortcutsActionArray.append(frame.OnSelectDocumentNext)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Previous Document"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F9)
            shortcutsActionArray.append(frame.OnSelectDocumentPrevious)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "First Document"):
            shortcutsActionArray.append(frame.OnSelectDocumentFirst)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Last Document"):
            shortcutsActionArray.append(frame.OnSelectDocumentLast)
            shortcutsArgumentsArray.append("frame, event")

        #Edit
        elif(ShortcutNames[x] == "Find"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('F'))
            shortcutsActionArray.append(frame.OnMenuFind)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Find Next"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F3)
            shortcutsActionArray.append(frame.OnMenuFindNext)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Find Previous"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(wx.WXK_F3)
            shortcutsActionArray.append(frame.OnMenuFindPrevious)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Replace"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('R'))
            shortcutsActionArray.append(frame.OnMenuReplace)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Find In Files"):
            shortcutsActionArray.append(frame.OnMenuFindInFiles)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Replace In Files"):
            shortcutsActionArray.append(frame.OnMenuReplaceInFiles)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Insert Regular Expression"):
            shortcutsActionArray.append(frame.OnInsertRegEx)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Insert Separator"):
            shortcutsActionArray.append(frame.OnInsertSeparator)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Comment"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('['))
            shortcutsActionArray.append(frame.OnCommentRegion)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "UnComment"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord(']'))
            shortcutsActionArray.append(frame.OnUnCommentRegion)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Indent"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('I'))
            shortcutsActionArray.append(frame.OnIndentRegion)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Dedent"):
            if useDefault:
                Shortcuts[x] = 'ControlShift' + str(ord('I'))
            shortcutsActionArray.append(frame.OnDedentRegion)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Find And Complete"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(wx.WXK_RETURN)
            shortcutsActionArray.append(frame.OnFindAndComplete)
            shortcutsArgumentsArray.append("frame, event")

        #View
        elif(ShortcutNames[x] == "Go To"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('G'))
            shortcutsActionArray.append(frame.OnGoTo)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Go To Block Start"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('B'))
            shortcutsActionArray.append(frame.OnGoToBlockStart)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Go To Block End"):
            if useDefault:
                Shortcuts[x] = 'ControlShift' + str(ord('B'))
            shortcutsActionArray.append(frame.OnGoToBlockEnd)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Go To Class Start"):
            shortcutsActionArray.append(frame.OnGoToClassStart)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Go To Class End"):
            shortcutsActionArray.append(frame.OnGoToClassEnd)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Go To Def Start"):
            shortcutsActionArray.append(frame.OnGoToDefStart)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Go To Def End"):
            shortcutsActionArray.append(frame.OnGoToDefEnd)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Toggle Fold"):
            shortcutsActionArray.append(frame.OnToggleFold)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Fold All"):
            shortcutsActionArray.append(frame.OnFoldAll)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Expand All"):
            shortcutsActionArray.append(frame.OnExpandAll)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Source Browser Go To"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(wx.WXK_F8)
            shortcutsActionArray.append(frame.OnSourceBrowserGoTo)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Toggle Source Browser"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F8)
            shortcutsActionArray.append(frame.OnToggleSourceBrowser)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Toggle View Whitespace"):
            if useDefault:
                Shortcuts[x] = 'ControlShift' + str(ord('W'))
            shortcutsActionArray.append(frame.OnToggleViewWhiteSpace)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Toggle Prompt"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F6)
            shortcutsActionArray.append(frame.OnTogglePrompt)
            shortcutsArgumentsArray.append("frame, event")

        elif(ShortcutNames[x] == "View In Left Panel"):
            shortcutsActionArray.append(frame.OnViewInLeftPanel)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "View In Right Panel"):
            shortcutsActionArray.append(frame.OnViewInRightPanel)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "View In Top Panel"):
            shortcutsActionArray.append(frame.OnViewInTopPanel)
            shortcutsArgumentsArray.append("frame, event")

        #Program
        elif(ShortcutNames[x] == "Check Syntax"):
            shortcutsActionArray.append(frame.OnCheckSyntax)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Run"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(ord('E'))
            shortcutsActionArray.append(frame.OnRun)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Set Arguments"):
            shortcutsActionArray.append(frame.OnSetArgs)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Python"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F7)
            shortcutsActionArray.append(frame.OnPython)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "End"):
            if useDefault:
                Shortcuts[x] = 'ControlShift' + str(ord('E'))
            shortcutsActionArray.append(frame.OnEnd)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Close Prompt"):
            shortcutsActionArray.append(frame.OnClosePrompt)
            shortcutsArgumentsArray.append("frame, event")

        #DrScript
        elif(ShortcutNames[x] == "Dynamic DrScript"):
            shortcutsActionArray.append(frame.dynamicdrscript)
            shortcutsArgumentsArray.append("frame, event")

        #Prefs
        elif(ShortcutNames[x] == "Preferences"):
            shortcutsActionArray.append(frame.OnPrefs)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Customize Shortcuts"):
            shortcutsActionArray.append(frame.OnCustomizeShortcuts)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Customize Pop Up Menu"):
            shortcutsActionArray.append(frame.OnCustomizePopUpMenu)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "Customize ToolBar"):
            shortcutsActionArray.append(frame.OnCustomizeToolBar)
            shortcutsArgumentsArray.append("frame, event")

        #Docs
        elif(ShortcutNames[x] == "Help"):
            if useDefault:
                Shortcuts[x] = str(wx.WXK_F1)
            shortcutsActionArray.append(frame.OnViewHelp)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "View Python Docs"):
            shortcutsActionArray.append(frame.OnViewPythonDocs)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "View WxWidgets Docs"):
            shortcutsActionArray.append(frame.OnViewWxWidgetsDocs)
            shortcutsArgumentsArray.append("frame, event")
        elif(ShortcutNames[x] == "View Regular Expression Howto"):
            shortcutsActionArray.append(frame.OnViewREHowtoDocs)
            shortcutsArgumentsArray.append("frame, event")

        #General
        elif(ShortcutNames[x] == "Toggle Maximize"):
            if useDefault:
                Shortcuts[x] = 'Control' + str(wx.WXK_F5)
            shortcutsActionArray.append(frame.Maximize)
            shortcutsArgumentsArray.append("maximize")

        elif(ShortcutNames[x] == "Inspect Tool"):
            if useDefault:
                Shortcuts[x] = 'Alt' + str(ord('T'))
            shortcutsActionArray.append(frame.OnOpenWidgetInspector)
            shortcutsArgumentsArray.append("frame, event")

        x = x + 1

    return Shortcuts, shortcutsActionArray, shortcutsArgumentsArray

def RunShortcuts(frame, event, stc, SplitView):
    keycode = event.GetKeyCode()

    #Treat Numpad Enter as Enter.
    if keycode == wx.WXK_NUMPAD_ENTER:
        keycode = wx.WXK_RETURN

    allowControl = not (frame.ShortcutsIgnoreString.find("Control") > -1)
    allowShift = not (frame.ShortcutsIgnoreString.find("Shift") > -1)
    allowAlt = not (frame.ShortcutsIgnoreString.find("Alt") > -1)
    allowMeta = not (frame.ShortcutsIgnoreString.find("Meta") > -1)

    control = (event.ControlDown() and allowControl)
    shift = (event.ShiftDown() and allowShift)
    alt = (event.AltDown() and allowAlt)
    meta = (event.MetaDown() and allowMeta)

    strkeycode = BuildShortcutString(keycode, control, shift, alt, meta)

    #Get the active stc:
    if stc is None:
        if frame.txtPrompt.GetSTCFocus():
            stc = frame.txtPrompt
        else:
            stc = frame.txtDocument

    allowControl = not (frame.ShortcutsIgnoreString.find("Control") > -1)
    allowShift = not (frame.ShortcutsIgnoreString.find("Shift") > -1)
    allowMeta = not (frame.ShortcutsIgnoreString.find("Meta") > -1)
    allowAlt = not (frame.ShortcutsIgnoreString.find("Alt") > -1)

    drstc = -1
    drpy = -1
    drscript = -1
    plugin = -1

    if strkeycode in frame.PluginShortcuts:
        plugin = frame.PluginShortcuts.index(strkeycode)
    if strkeycode in frame.STCShortcuts:
        drstc = frame.STCShortcuts.index(strkeycode)
    elif strkeycode in frame.Shortcuts:
        drpy = frame.Shortcuts.index(strkeycode)
    elif strkeycode in frame.DrScriptShortcuts:
        drscript = frame.DrScriptShortcuts.index(strkeycode)

    if plugin > -1:
        r = frame.PluginAction[plugin](event)
        if r is None or (r == 1):
            return -1

    if stc.IsAPrompt:
        if (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_NEWLINE) or \
        (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_CHARLEFT) or \
        (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_CHARRIGHT) or \
        (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_LINEUP) or \
        (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_LINEDOWN) or \
        (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_DELETEBACK) or \
        (frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_HOME):
            return frame.STCCOMMANDLIST[drstc]

    elif frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_DELETEBACK:
        return wx.stc.STC_CMD_DELETEBACK

    if drstc > -1 and (not drpy > -1) and (not drscript > -1):
        try:
            if frame.STCCOMMANDLIST[drstc] == wx.stc.STC_CMD_PASTE:
                stc.Paste()
            else:
                stc.CmdKeyExecute(frame.STCCOMMANDLIST[drstc])
        except:
            return -1
        return frame.STCCOMMANDLIST[drstc]
    if SplitView:
        return -1
    if drpy > -1 and (not drscript > -1) and (not drstc > -1):
        if frame.ShortcutsArgumentsArray[drpy] == "frame, event":
            frame.ShortcutsActionArray[drpy](event)
        elif frame.ShortcutsArgumentsArray[drpy] == "maximize":
            #Work Around Bug in wx.Python 2.5.1
            try:
                frame.ShortcutsActionArray[drpy](not frame.IsMaximized())
            except:
                pass
        return -1
    if drscript > -1 and (not drpy > -1) and (not drstc > -1):
        event.SetId(frame.ID_SCRIPT_BASE + drscript)
        frame.DrScriptShortcutsAction(event)
        return -1

    ignoreevent = False

    if frame.prefs.docignoretextfunctionkeys:
      if event.GetKeyCode() >= wx.WXK_F1 and event.GetKeyCode() <= wx.WXK_F24: #it inserts character, most users don't want
          ignoreevent = True

    if frame.prefs.docignorectrlpageupdown:
        if event.GetKeyCode() in [wx.WXK_PAGEUP, wx.WXK_PAGEDOWN]:
            if wx.GetKeyState(wx.WXK_CONTROL):
                ignoreevent = True

    if not ignoreevent:
        event.Skip()

    return -1
