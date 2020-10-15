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

#Shortcuts Dialog

import os.path, re
import wx, wx.lib.dialogs
import drScrolledMessageDialog
from drGetKeyDialog import drGetKeyDialog
import drShortcutsFile
import drShortcuts
from drShortcuts import MatchControl, MatchShift, MatchAlt, MatchMeta

def ShortcutIsAlreadyTaken(TargetShortcut, ShortcutArrays, CurrentShortcut = None):
    if drShortcuts.GetKeycodeStringFromShortcut(TargetShortcut) == "":
        return -1
    i = 0
    for ShortcutArray in ShortcutArrays:
        for Shortcut in ShortcutArray:
            if Shortcut == TargetShortcut:
                if CurrentShortcut is not None:
                    if not CurrentShortcut == TargetShortcut:
                        return i
                else:
                    return i
        i += 1
    return -1

def GetShortcuts(filename, frame):
    try:
        f = file(filename, 'r')
        text = f.read()
        f.close()
    except:
        drScrolledMessageDialog.ShowMessage(frame, 'File error with: "' + filename + '".', "ERROR")
        return ""

    reShortcuts = re.compile(r'^\s*?DrFrame\.AddPluginShortcutFunction\(.*\)', re.MULTILINE)

    allShortcuts = reShortcuts.findall(text)

    ShortcutsArray = []

    for s in allShortcuts:
        #From the Left most '('
        start = s.find('(')
        #To the Right most ')'
        end = s.rfind(')')

        if (start > -1) and (end > -1):
            s = s[start+1:end]
            i = s.find(',')
            e = i + 1 + s[i+1:].find(',')
            argfunctionname = s[i+1:e].strip().strip('"')

            ShortcutsArray.append(argfunctionname)

    return ShortcutsArray

class drShortcutPanel(wx.Panel):

    def __init__(self, parent, id, wxSize):

        wx.Panel.__init__(self, parent, id, size=wxSize)

        self.ID_GET_KEY = 403

        self.shortcutIndex = -1
        self.listIndex = 0

        self.theSizer = wx.FlexGridSizer(7, 3, 5, 10)

        self.txtKeyChar = wx.TextCtrl(self, id, size=wx.Size(100, -1), style=wx.TE_READONLY)

        self.txtKeyCode = wx.TextCtrl(self, id, size=wx.Size(100, -1), style=wx.TE_READONLY)

        self.chkAlt = wx.CheckBox(self, id, "")
        self.chkControl = wx.CheckBox(self, id, "")
        self.chkMeta = wx.CheckBox(self, id, "")
        self.chkShift = wx.CheckBox(self, id, "")

        self.chkAlt.Enable(False)
        self.chkControl.Enable(False)
        self.chkMeta.Enable(False)
        self.chkShift.Enable(False)

        self.btnGetKey = wx.Button(self, self.ID_GET_KEY, "Get Key")

        self.parent = parent

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Key Char:"), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.txtKeyChar, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Key Code:"), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.txtKeyCode, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Alt:"), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.chkAlt, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Control"), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.chkControl, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Meta:"), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.chkMeta, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Shift:"), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.chkShift, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(self.btnGetKey, 1, wx.ALIGN_LEFT | wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnbtnGetKey, id=self.ID_GET_KEY)

    def OnbtnGetKey(self, event):
        oldv = self.parent.ShortcutsArray[self.listIndex][self.shortcutIndex]
        d = drGetKeyDialog(self, self.parent.txtIgnore.GetValue(), self.parent)
        d.SetKeyString(oldv)
        d.ShowModal()
        newv = d.GetKeyString()
        d.Destroy()
        alreadytaken = ShortcutIsAlreadyTaken(newv, self.parent.ShortcutsArray, oldv)
        if alreadytaken > -1:
            if alreadytaken == 0:
                takenby = self.parent.parent.ShortcutNames[self.parent.ShortcutsArray[alreadytaken].index(newv)]
            elif alreadytaken == 1:
                takenby = self.parent.parent.STCShortcutNames[self.parent.ShortcutsArray[alreadytaken].index(newv)]
            elif alreadytaken == 2:
                takenby = self.parent.parent.DrScriptShortcutNames[self.parent.ShortcutsArray[alreadytaken].index(newv)]
            else:
                takenby = self.parent.PluginShortcutNameList[alreadytaken-3][self.parent.ShortcutsArray[alreadytaken].index(newv)]
            drScrolledMessageDialog.ShowMessage(self, ('The Shortcut "' + newv + \
            '"\nis already being used by "' + takenby + '".\nDrPython will politely ignore your request.'),\
            "Shortcut Already Taken")
            return
        self.parent.ShortcutsArray[self.listIndex][self.shortcutIndex] = newv
        self.SetShortcut(self.parent.ShortcutsArray[self.listIndex][self.shortcutIndex], self.shortcutIndex, self.listIndex)

    def Reset(self):
        self.txtKeyChar.SetValue("")
        self.txtKeyCode.SetValue("")

        self.chkAlt.SetValue(False)
        self.chkControl.SetValue(False)
        self.chkMeta.SetValue(False)
        self.chkShift.SetValue(False)

    def SetShortcut(self, shortcut, shortcutIndex, listIndex):
        try:
            self.shortcutIndex = shortcutIndex
            self.listIndex = listIndex

            keycode = drShortcuts.GetKeycodeFromShortcut(shortcut)

            if keycode:
                found, text = drShortcuts.GetKeycodeText(keycode)
                if found:
                    self.txtKeyChar.SetValue(text)
                elif (keycode < 0) or (keycode > 256):
                    self.txtKeyChar.SetValue("UnKnown")
                else:
                    self.txtKeyChar.SetValue(chr(keycode))
            else:
                self.txtKeyChar.SetValue("None")

            self.txtKeyCode.SetValue(str(keycode))

            self.chkAlt.SetValue(drShortcuts.MatchAlt(shortcut))
            self.chkControl.SetValue(drShortcuts.MatchControl(shortcut))
            self.chkMeta.SetValue(drShortcuts.MatchMeta(shortcut))
            self.chkShift.SetValue(drShortcuts.MatchShift(shortcut))
        except:
            drScrolledMessageDialog.ShowMessage(self.parent, "Error Selecting Shortcut", "DrPython Error")
            return


class drShortcutsDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, ("Customize Shortcuts"), wx.DefaultPosition, wx.Size(-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)

        wx.Yield()

        self.ID_SHORTCUTS = 1001

        self.ID_LIST = 1300

        self.ID_RESET = 1004
        self.ID_UPDATE = 1005
        self.ID_SAVE = 1006

        self.ID_IGNORE = 1300

        self.parent = parent

        self.theSizer = wx.FlexGridSizer(5, 4, 5, 10)
        self.listSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ignoreSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.shortcutsdirectory = parent.shortcutsdirectory

        self.ShortcutsArray = [[], [], []]

        #Shortcuts

        self.ShortcutsIgnoreString = parent.ShortcutsIgnoreString

        self.ShortcutsArray[0] = list(self.parent.Shortcuts)

        #Text Control

        self.ShortcutsArray[1] = list(self.parent.STCShortcuts)

        #DrScript

        self.ShortcutsArray[2] = list(self.parent.DrScriptShortcuts)

        self.ShortcutsArrayPos = 0

        #Plugins

        self.LoadPluginShortcutList()

        self.ShortcutList = ["Standard", "Text Control", "DrScript"]
        self.ShortcutList.extend(self.PluginList)

        self.cboList = wx.ComboBox(self, self.ID_LIST, "Standard", wx.DefaultPosition, (200, -1), self.ShortcutList, wx.CB_DROPDOWN|wx.CB_READONLY)

        self.boxShortcuts = wx.ListBox(self, self.ID_SHORTCUTS, wx.DefaultPosition, wx.Size(200, 200), self.parent.ShortcutNames)

        self.pnlShortcut = drShortcutPanel(self, -1, wx.Size(250, -1))

        self.btnGetIgnoreKeys = wx.Button(self, self.ID_IGNORE, "Ignore Key(s)...")

        self.txtIgnore = wx.TextCtrl(self, -1, self.ShortcutsIgnoreString, size=wx.Size(100, -1), style=wx.TE_READONLY)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.listSizer.Add(wx.StaticText(self, -1, "List: "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.listSizer.Add(self.cboList, 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.ignoreSizer.Add(wx.StaticText(self, -1, "Ignore: "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.ignoreSizer.Add(self.txtIgnore, 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.ignoreSizer.Add(self.btnGetIgnoreKeys, 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.listSizer, 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.ignoreSizer, 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Shortcuts List:"), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Shortcut:"), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.boxShortcuts, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.pnlShortcut, 1,  wx.EXPAND | wx.ALIGN_CENTER)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.btnReset = wx.Button(self, self.ID_RESET, "&Reset")
        self.btnUpdate = wx.Button(self, self.ID_UPDATE, "&Update")
        self.btnSave = wx.Button(self, self.ID_SAVE, "&Save")

        self.btnClose = wx.Button(self, 101, "&Close")

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.btnReset, 0,  wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnUpdate, 0,  wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnSave, 0,  wx.SHAPED | wx.ALIGN_CENTER)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.btnClose, 0,  wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.btnClose.SetDefault()

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnbtnReset, id=self.ID_RESET)
        self.Bind(wx.EVT_BUTTON, self.OnbtnUpdate, id=self.ID_UPDATE)
        self.Bind(wx.EVT_BUTTON, self.OnbtnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.OnbtnClose, id=101)

        self.Bind(wx.EVT_BUTTON, self.OnbtnGetIgnoreKeys, id=self.ID_IGNORE)

        self.Bind(wx.EVT_COMBOBOX, self.OnList, id=self.ID_LIST)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=self.ID_SHORTCUTS)

        self.parent.LoadDialogSizeAndPosition(self, 'shortcutsdialog.sizeandposition.dat')

    def LoadPluginShortcutList(self):
        plist = os.listdir(self.parent.pluginsdirectory)

        self.PluginShortcutNameList = []

        self.PluginList = []
        for p in plist:
            i = p.find(".py")
            l = len(p)
            if i > -1 and (i + 3 == l):
                self.PluginList.append("<Plugin>:" + p[:i])

        poplist = []
        #Load shortcuts from plugins.
        for plugin in self.PluginList:
            list = []
            if plugin.find("<Plugin>") > -1:
                pluginfile = os.path.join(self.parent.pluginsdirectory, plugin[plugin.find(':')+1:] + ".py")
                shortcutfile = os.path.join(self.parent.pluginsshortcutsdirectory, plugin[plugin.find(':')+1:] + ".shortcuts.dat")
                list = GetShortcuts(pluginfile, self)
                plist = self.parent.GetPluginLabels(pluginfile, True)
                for p in plist:
                    if not (p in list):
                        list.append(p)
                shortcuts = []
                if list:
                    needtomakefile = 0
                    #If the file does not exist, or is out of date, create it.
                    if not os.path.exists(shortcutfile):
                        needtomakefile = 1
                    else:
                        shortcuts, names, ignorestring = drShortcutsFile.ReadShortcuts(shortcutfile, 0)
                        if len(shortcuts) != len(list):
                            needtomakefile = 2

                    if needtomakefile:
                        try:
                            if list:
                                f = file(shortcutfile, 'w')
                                if needtomakefile == 2:
                                    for s in list:
                                        if s in names:
                                            ix = names.index(s)
                                            f.write("<" + s + "><mod>")
                                            if MatchControl(shortcuts[ix]):
                                                f.write("Control,")
                                            if MatchShift(shortcuts[ix]):
                                                f.write("Shift,")
                                            if MatchAlt(shortcuts[ix]):
                                                f.write("Alt,")
                                            if MatchMeta(shortcuts[ix]):
                                                f.write("Meta")
                                            f.write("</mod><keycode>" + drShortcuts.GetKeycodeStringFromShortcut(shortcuts[ix]) +
                                            "</keycode></" + s + ">\n")
                                        else:
                                            f.write("<" + s + "><mod></mod><keycode></keycode></" + s + ">\n")
                                else:
                                    for s in list:
                                        f.write("<" + s + "><mod></mod><keycode></keycode></" + s + ">\n")
                                f.close()
                                shortcuts, names, ignorestring = drShortcutsFile.ReadShortcuts(shortcutfile, 0)
                            else:
                                shortcuts, names, ignorestring = [], [], ""

                            if plugin.find(':') > -1:
                                plugin = plugin[plugin.find(':')+1:]

                            x = 0
                            for shortcut in shortcuts:
                                try:
                                    i = self.parent.PluginShortcutFunctionNames.index(plugin + ":" + names[x])
                                    self.parent.PluginAction.append(self.parent.PluginShortcutFunctions[i])
                                    self.parent.PluginShortcuts.append(shortcut)
                                except:
                                    pass
                                x += 1
                            if os.path.exists(shortcutfile):
                                shortcuts, names, ignorestring = drShortcutsFile.ReadShortcuts(shortcutfile, 0)
                        except:
                            drScrolledMessageDialog.ShowMessage(self, ("Error Creating Shortcuts For Plugin"), "Plugin Shortcuts Error")
                            return

                if shortcuts:
                    self.ShortcutsArray.append(shortcuts)
                    self.PluginShortcutNameList.append(names)
                else:
                    poplist.append(plugin)

        for popl in poplist:
            try:
                i = self.PluginList.index(popl)
                self.PluginList.pop(i)
            except:
                pass

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, 'shortcutsdialog.sizeandposition.dat')
        if event is not None:
            event.Skip()

    def OnbtnClose(self, event):
        self.Close(1)

    def OnbtnGetIgnoreKeys(self, event):
        addstring = '\n\n'
        if self.parent.PLATFORM_IS_WIN:
            addstring = '\n\n\n\n\n\n'
        d = wx.lib.dialogs.MultipleChoiceDialog(self, "Select the Modifier Keys you wish to ignore:" + addstring,
            "Ignore Modifier Keys", ["Control", "Meta", "Shift", "Alt"])
        answer = d.ShowModal()
        if answer == wx.ID_OK:
            tuply = d.GetValueString()
            leString = ""
            for selection in tuply:
                leString = leString + selection + ","
            self.txtIgnore.SetValue(leString)
        d.Destroy()

    def OnbtnReset(self, event):
        answer = wx.MessageBox("This will reset all standard shortcuts to the program default.\n(You still need to click update and/or save)\nAre you sure you want to do this?",
            "Reset Shortcuts", wx.YES_NO | wx.ICON_QUESTION)
        if answer == wx.YES:
            self.ShortcutsArray[0], self.ShortcutsIgnoreString = drShortcutsFile.GetDefaultShortcuts()
            self.ShortcutsArray[0], saa, sarg = drShortcuts.SetShortcuts(self.parent, self.ShortcutsArray[0], self.parent.ShortcutNames, 1)
            sel = self.boxShortcuts.GetSelection()
            self.ShortcutsArray[1] = drShortcuts.SetSTCShortcuts(self.parent.txtDocument, self.ShortcutsArray[1], True)
            drShortcuts.SetSTCShortcuts(self.parent.txtPrompt, self.ShortcutsArray[1], True)
            self.pnlShortcut.SetShortcut(self.ShortcutsArray[self.ShortcutsArrayPos][sel], sel, self.ShortcutsArrayPos)

    def OnbtnSave(self, event):
        #STC
        shortcutsfile = self.shortcutsdirectory + "/stcshortcuts.dat"
        try:
            drShortcutsFile.WriteShortcuts(shortcutsfile, self.ShortcutsArray[1], self.parent.STCShortcutNames, "", False)
        except:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + shortcutsfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return

        #STCDefault
        if self.parent.STCUseDefault:
            self.parent.STCUseDefault = 0

        #Main
        shortcutsfile = self.shortcutsdirectory + "/shortcuts.dat"
        try:
            drShortcutsFile.WriteShortcuts(shortcutsfile, self.ShortcutsArray[0], self.parent.ShortcutNames, self.txtIgnore.GetValue())
        except:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + shortcutsfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return

        #DrScripts
        shortcutsfile = self.shortcutsdirectory + "/drscript.shortcuts.dat"
        try:
            drShortcutsFile.WriteShortcuts(shortcutsfile, self.ShortcutsArray[2], self.parent.DrScriptShortcutNames, "", False)
        except:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + shortcutsfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return

        #Plugins
        x = 3
        l = len(self.ShortcutsArray)
        while x < l:
            plugin = self.ShortcutList[x]
            if plugin.find("<Plugin>") > -1:
                shortcutsfile = os.path.join(self.parent.pluginsshortcutsdirectory, plugin[plugin.find(':')+1:] + ".shortcuts.dat")
                try:
                    drShortcutsFile.WriteShortcuts(shortcutsfile, self.ShortcutsArray[x], self.PluginShortcutNameList[x-3], "", False)
                except:
                    drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + shortcutsfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
                    return

            x = x + 1

        self.update()

        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully saved shortcuts\nand updated the current instance of DrPython."), "Saved Shortcuts")

    def OnbtnUpdate(self, event):

        self.update()

        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully updated the current instance of DrPython.\nClick Save to make it permanent."), "Updated Shortcuts")

    def OnList(self, event):
        sel = self.cboList.GetSelection()
        self.ShortcutsArrayPos = sel

        self.pnlShortcut.Reset()

        if sel == 0:
            names = self.parent.ShortcutNames

        elif sel == 1:
            names = self.parent.STCShortcutNames

        elif sel == 2:
            names = self.parent.DrScriptShortcutNames

        else:
            names = self.PluginShortcutNameList[sel-3]

        self.boxShortcuts.Set(names)

    def OnSelect(self, event):
        sel = self.boxShortcuts.GetSelection()
        self.pnlShortcut.SetShortcut(self.ShortcutsArray[self.ShortcutsArrayPos][sel], sel, self.ShortcutsArrayPos)

    def update(self):
        self.parent.ShortcutsIgnoreString = self.txtIgnore.GetValue()

        self.parent.Shortcuts = self.ShortcutsArray[0]
        self.parent.STCShortcuts = self.ShortcutsArray[1]
        self.parent.DrScriptShortcuts = self.ShortcutsArray[2]

        self.parent.ShortcutsActionArray = []
        self.parent.ShortcutsArgumentsArray = []

        drShortcuts.SetSTCShortcuts(self.parent.txtPrompt, self.parent.STCShortcuts)
        self.parent.STCShortcuts = drShortcuts.SetSTCShortcuts(self.parent.txtDocument, self.parent.STCShortcuts)
        self.parent.Shortcuts, self.parent.ShortcutsActionArray, self.parent.ShortcutsArgumentsArray = drShortcuts.SetShortcuts(self.parent, self.ShortcutsArray[0], self.parent.ShortcutNames)

        #Plugins:

        l = len(self.ShortcutsArray)
        if l > 3:
            x = 3
            while x < l:
                sArray = self.ShortcutsArray[x]
                a = x - 3
                ly = len(sArray)
                y = 0
                while y < ly:
                    yName = self.ShortcutList[x] + ":" + self.PluginShortcutNameList[a][y]
                    yName = yName[yName.find(':')+1:]
                    if yName in self.parent.PluginShortcutFunctionNames:
                        i = self.parent.PluginShortcutFunctionNames.index(yName)
                        try:
                            self.parent.PluginShortcuts[i] = sArray[y]
                        except:
                            pass
                    y = y + 1
                x = x + 1