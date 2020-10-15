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

#drScript Dialog

import os.path
import wx
import drScrolledMessageDialog
from drProperty import *
from drPrefsFile import ExtractPreferenceFromText
import drShortcutsFile
from drTreeDialog import *

class drTreeItemData(wx.TreeItemData):
    def __init__(self, Line, Shortcut):
        wx.TreeItemData.__init__(self)
        self.Line = Line
        self.Shortcut = Shortcut

def BuildTreeFromString(dialog, branch, thestring):
    line = " "
    roots = [branch]
    rootindex = 0
    #Shortcuts
    Shortcuts = []
    ShortcutIndex = 0
    map(Shortcuts.append, dialog.parent.DrScriptShortcuts[dialog.parent.drscriptmenu.ExampleScriptCount:])
    lastCount = 0
    i = 0
    lastI = 0
    while line:
        i = thestring.find('\n')
        if i > -1:
            line = thestring[0:(i + 1)]
            lastI = i + 1
            thestring = thestring[lastI:]
            c = line.count('\t')
            line = line[c:].rstrip()
            while lastCount > c:
                roots.pop()
                rootindex = rootindex - 1
                lastCount = lastCount - 1
            if line.find("title") > -1:
                line_title = ExtractPreferenceFromText(line, "title")
                currentItem = dialog.datatree.AppendItem(roots[rootindex], line_title)
                dialog.datatree.SetPyData(currentItem, drTreeItemData(line, Shortcuts[ShortcutIndex]))
                ShortcutIndex = ShortcutIndex + 1
                dialog.datatree.SetItemImage(currentItem, 2, wx.TreeItemIcon_Normal)
                dialog.datatree.SetItemImage(currentItem, 2, wx.TreeItemIcon_Selected)
            elif line[0] == '>':
                currentItem = dialog.datatree.AppendItem(roots[rootindex], line)
                dialog.datatree.SetPyData(currentItem, drTreeItemData(line, None))
                dialog.datatree.SetItemImage(currentItem, 0, wx.TreeItemIcon_Normal)
                dialog.datatree.SetItemImage(currentItem, 1, wx.TreeItemIcon_Expanded)
                roots.append(currentItem)
                rootindex = rootindex + 1
                lastCount = c + 1
        else:
            line = ""

class drScriptDialog(drTreeDialog):
    def __init__(self, parent):
        drTreeDialog.__init__(self, parent, 'Edit DrScript Menu', 'DrScript Menu', parent.preferencesdirectory + "/drscript.dat", parent.prefs.drscriptstyle, \
        'drscriptdialog.sizeandposition.dat', parent.bitmapdirectory + '/16/drscript.png', BuildTreeFromString, self.WriteBranch)

        self.SetupSizer()

    def GetShortcutArrays(self, tree, branch):
        Shortcuts = []
        t = tree.GetItemText(branch)
        if not (t[0] == '>'):
            data = tree.GetPyData(branch)
            if data.Shortcut is not None:
                Shortcuts.append(data.Shortcut)
        else:
            ccount = tree.GetChildrenCount(branch, 0)
            if ccount > 0:
                if (wx.MAJOR_VERSION >= 2) and (wx.MINOR_VERSION >= 5):
                    b, cookie = tree.GetFirstChild(branch)
                else:
                    b, cookie = tree.GetFirstChild(branch, 1)
                s = self.GetShortcutArrays(tree, b)
                Shortcuts.extend(s)
                x = 1
                while x < ccount:
                    b, cookie = tree.GetNextChild(branch, cookie)
                    s = self.GetShortcutArrays(tree, b)
                    Shortcuts.extend(s)
                    x = x + 1

        return Shortcuts
    
    def WriteBranch(self, tree, branch, filehandle, tablevel):
        t = tree.GetItemText(branch)
        if tablevel > -1:
            data = tree.GetPyData(branch)
            if data is not None:
                x = 0
                y = ""
                while x < tablevel:
                    y = y + '\t'
                    x = x + 1
                title = ExtractPreferenceFromText(data.Line, "title")
                if title:
                    self.parent.drscriptmenu.titles.append(title)
                if title:
                    if not (title == t):
                        data.Line = data.Line[:data.Line.find("<title>")] + "<title>" + t  + "</title>"
                y = y + data.Line + '\n'
                filehandle.write(y)
        if t[0] == '>':
            ccount = tree.GetChildrenCount(branch, 0)
            if ccount > 0:
                if (wx.MAJOR_VERSION >= 2) and (wx.MINOR_VERSION >= 5):
                    b, cookie = tree.GetFirstChild(branch)
                else:
                    b, cookie = tree.GetFirstChild(branch, 1)
                self.WriteBranch(tree, b, filehandle, (tablevel + 1))
                x = 1
                while x < ccount:
                    b, cookie = tree.GetNextChild(branch, cookie)
                    self.WriteBranch(tree, b, filehandle, (tablevel + 1))
                    x = x + 1



    def OnbtnAddFolder(self, event):
        sel = self.datatree.GetSelection()
        if not sel.IsOk():
            if self.datatree.GetCount() < 2:
                sel = self.datatree.GetRootItem()
            else:
                return
        if self.datatree.GetItemText(sel)[0] == '>':
            d = wx.TextEntryDialog(self, 'Enter Tree Folder:', 'Add Folder', '')
            if d.ShowModal() == wx.ID_OK:
                v = d.GetValue()
                sel = self.datatree.GetSelection()
                if sel.IsOk():
                    item = self.datatree.AppendItem(self.datatree.GetSelection(), ">" + v)
                    self.datatree.SetPyData(item, drTreeItemData(">" + v, None))
                    self.datatree.SetItemImage(item, 0, wx.TreeItemIcon_Normal)
                    self.datatree.SetItemImage(item, 1, wx.TreeItemIcon_Expanded)
                    self.datatree.SetModified()
            d.Destroy()
        else:
            drScrolledMessageDialog.ShowMessage(self, "You can only add a folder to another folder.", "Bad Folder Location")

    def OnbtnSave(self, event):
        try:
            root = self.datatree.GetRootItem()
            f = open(self.targetfile, 'w')
            self.parent.drscriptmenu.titles = self.parent.drscriptmenu.titles[:self.parent.drscriptmenu.ExampleScriptCount]
            self.WriteBranch(self.datatree, root, f, -1)
            f.close()
        except IOError:
            drScrolledMessageDialog.ShowMessage(self, "There were some problems writing to:\n" + self.targetfile, "Write Error")
            return
        self.datatree.SetModified(False)
        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully wrote to:\n"  + self.targetfile), "Success")


        root = self.datatree.GetRootItem()

        #Sync Shortcuts:
        s = self.GetShortcutArrays(self.datatree, root)
        self.parent.DrScriptShortcuts = self.parent.DrScriptShortcuts[:self.parent.drscriptmenu.ExampleScriptCount]
        map(lambda x: self.parent.DrScriptShortcuts.append(x), s)

        #Sync the Shortcuts File:

        shortcutsfile = self.parent.shortcutsdirectory + "/drscript.shortcuts.dat"
        try:
            drShortcutsFile.WriteShortcuts(shortcutsfile, self.parent.DrScriptShortcuts, self.parent.drscriptmenu.titles, "", False)
        except IOError:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + shortcutsfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return
