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

#Shortcuts File

import drPrefsFile
from drShortcuts import BuildShortcutString, GetKeycodeStringFromShortcut, MatchControl, MatchShift, MatchAlt, MatchMeta

def GetShortcutList():
    #Shortcut List

    return ["Check Syntax", "Close",
    "Close All Documents", "Close All Other Documents",
    "Close Prompt",
    "Comment", "Customize Shortcuts",
    "Customize Pop Up Menu", "Customize ToolBar", "Dedent",
    "Dynamic DrScript", "End", "Exit", "Expand All", "Find",
    "Find And Complete", "Find Next",
    "Find Previous", "First Document", "Fold All", "Go To",
    "Go To Block End", "Go To Block Start",
    "Go To Class End", "Go To Class Start",
    "Go To Def End", "Go To Def Start",
    "Help", "Indent", "Insert Regular Expression", "Insert Separator",
    "Last Document", "New", "Next Document", "Open",
    "Open Imported Module",
    "Preferences", "Previous Document", "Print File",
    "Print Prompt", "Print Setup", "Python",
    "Reload File", "Replace",
    "Restore From Backup", "Run", "Save", "Save All Documents", "Save As",
    "Save Prompt Output To File", "Set Arguments",
    "Source Browser Go To",
    "Toggle Fold",
    "Toggle Maximize", "Toggle Prompt","Toggle Source Browser", "Toggle View Whitespace",
    "UnComment",
    "View In Left Panel", "View In Right Panel", "View In Top Panel",
    "View Python Docs", "View Regular Expression Howto", "View WxWidgets Docs"]

def GetSTCShortcutList():
    #STC Shortcuts:
    return ["Back Tab", "Cancel", "Char Left", "Char Left Extend", "Char Left Rect Extend",
    "Char Right", "Char Right Extend", "Char Right Rect Extend", "Copy", "Cut",
    "Delete", "Delete Back", "Delete Back Not Line",
    "Delete Line Left", "Delete Line Right",
    "Delete Word Left", "Delete Word Right",
    "Document End", "Document End Extend",
    "Document Start", "Document Start Extend",
    "Form Feed", "Home",
    "Home Display", "Home Display Extend",
    "Home Extend", "Home Rect Extend", "Line Cut", "Line Delete",
    "Line Down", "Line Down Extend", "Line Down Rect Extend", "Line Duplicate", "Line End",
    "Line End Display", "Line End Display Extend",
    "Line End Extend", "Line End Rect Extend", "Line Scroll Down",
    "Line Scroll Up", "Line Transpose", "Line Up",
    "Line Up Extend", "Line Up Rect Extend", "Lowercase", "New Line",
    "Page Down", "Page Down Extend", "Page Down Rect Extend", "Page Up",
    "Page Up Extend", "Page Up Rect Extend", "Paste", "Redo", "Select All",
    "Tab", "Toggle Overtype", "Undo",
    "Uppercase", "Visible Character Home",
    "Visible Character Home Extend", "World Left",
    "Word Left Extend", "Word Part Left", "Word Part Left Extend",
    "Word Part Right", "Word Part Right Extend",
    "Word Right", "Word Right Extend",
    "Zoom In", "Zoom Out"]

def IsBuiltIn(name):
    return 1

def GetDefaultProgramShortcuts(ShortcutList):
    shortcutArray = []

    l = len(ShortcutList)
    x = 0
    while x < l:
        shortcutArray.append('')
        x = x + 1

    return shortcutArray

def GetDefaultSTCShortcuts():
    return GetDefaultProgramShortcuts(GetSTCShortcutList())

def GetDefaultShortcuts():
    import sys
    if sys.platform.find("linux") > -1:
        ignorestring = "Meta,"
    else:
        ignorestring = ""

    sA = GetDefaultProgramShortcuts(GetShortcutList())

    return sA, ignorestring

def ReadSTCShortcuts(filename):
    f = open(filename, 'rb')
    text = f.read()
    f.close()

    shortcutArray = []
    shortcutNames = []

    x = 0
    progshortcutlist = GetSTCShortcutList()
    l = len(progshortcutlist)
    while x < l:
        shortcutNames.append(progshortcutlist[x])

        shortcuttext = drPrefsFile.ExtractPreferenceFromText(text, progshortcutlist[x])

        Keycode = drPrefsFile.ExtractPreferenceFromText(shortcuttext, "keycode")

        modifiers = drPrefsFile.ExtractPreferenceFromText(shortcuttext, "mod")

        shortcutArray.append(BuildShortcutString(Keycode, MatchControl(modifiers),
        MatchShift(modifiers), MatchAlt(modifiers), MatchMeta(modifiers)))

        x = x + 1

    return shortcutArray, shortcutNames, ''


def ReadShortcuts(filename, getIgnoreString = 1):
    shortcutNames = []
    if getIgnoreString:
        f = open(filename, 'rb')
        text = f.read()
        f.close()

        shortcutArray = []
        ignorestring = ""

        ignorestring = drPrefsFile.ExtractPreferenceFromText(text, "ignore")

        x = 0
        progshortcutlist = GetShortcutList()
        l = len(progshortcutlist)
        while x < l:
            shortcutNames.append(progshortcutlist[x])

            shortcuttext = drPrefsFile.ExtractPreferenceFromText(text, progshortcutlist[x])

            Keycode = drPrefsFile.ExtractPreferenceFromText(shortcuttext, "keycode")

            modifiers = drPrefsFile.ExtractPreferenceFromText(shortcuttext, "mod")

            shortcutArray.append(BuildShortcutString(Keycode, MatchControl(modifiers),
            MatchShift(modifiers), MatchAlt(modifiers), MatchMeta(modifiers)))

            x = x + 1
    else:
        f = open(filename, 'rb')

        shortcutArray = []
        ignorestring = ""

        x = 0

        line = f.readline()
        while len(line) > 0:
            s = line.find("<")
            e = line.find(">")
            if (s > -1) and (e > -1):
                shortcutNames.append(line[s+1:e])

                Keycode = drPrefsFile.ExtractPreferenceFromText(line, "keycode")

                modifiers = drPrefsFile.ExtractPreferenceFromText(line, "mod")

                shortcutArray.append(BuildShortcutString(Keycode, MatchControl(modifiers),
                MatchShift(modifiers), MatchAlt(modifiers), MatchMeta(modifiers)))

                x = x + 1
            line = f.readline()

        f.close()


    return shortcutArray, shortcutNames, ignorestring

def WriteShortcuts(filename, shortcuts, shortcutNames, ignorestring = "", writeIgnoreString = True):
    f = open(filename, 'wb')

    if writeIgnoreString:
        #Ignore String
        f.write("<ignore>" + ignorestring + "</ignore>\n")
    allowControl = not (ignorestring.find("Control") > -1)
    allowShift = not (ignorestring.find("Shift") > -1)
    allowMeta = not (ignorestring.find("Meta") > -1)
    allowAlt = not (ignorestring.find("Alt") > -1)

    l = len(shortcuts)
    x = 0
    while x < l:
        writestring = "<" + shortcutNames[x] + "><mod>"
        if MatchControl(shortcuts[x]) and allowControl:
            writestring = writestring + "Control,"
        if MatchShift(shortcuts[x]) and allowShift:
            writestring = writestring + "Shift,"
        if MatchAlt(shortcuts[x]) and allowAlt:
            writestring = writestring + "Alt,"
        if MatchMeta(shortcuts[x]) and allowMeta:
            writestring = writestring + "Meta,"
        writestring = writestring + "</mod><keycode>" + GetKeycodeStringFromShortcut(shortcuts[x]) + \
        "</keycode></" + shortcutNames[x] + ">\n"
        f.write(writestring)
        x = x + 1
    f.close()
