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

#Bookmarks Dialog

import wx
import drScrolledMessageDialog
import drFileDialog
from drProperty import *
from drTreeDialog import *

def BuildTreeFromString(dialog, branch, thestring):
    line = " "
    roots = [branch]
    rootindex = 0
    lastCount = 1
    i = 0
    lastI = 0
    #Skip the First Line
    i = thestring.find('\n')
    if i > -1:
        line = thestring[0:(i + 1)]
        lastI = i + 1
    thestring = thestring[lastI:]
    #Get On With It!
    while line:
        i = thestring.find('\n')
        if (i > -1):
            line = thestring[0:(i + 1)]
            lastI = i + 1
            thestring = thestring[lastI:]
            c = line.count('\t')
            line = line[c:].rstrip()
            while lastCount > c:
                roots.pop()
                rootindex = rootindex - 1
                lastCount = lastCount - 1
            currentItem = dialog.datatree.AppendItem(roots[rootindex], line)
            if line[0] == '>':
                dialog.datatree.SetItemImage(currentItem, 0, wx.TreeItemIcon_Normal)
                dialog.datatree.SetItemImage(currentItem, 1, wx.TreeItemIcon_Expanded)
                roots.append(currentItem)
                rootindex = rootindex + 1
                lastCount = c + 1
            else:
                dialog.datatree.SetItemImage(currentItem, 2, wx.TreeItemIcon_Normal)
                dialog.datatree.SetItemImage(currentItem, 2, wx.TreeItemIcon_Selected)
        else:
            line = ""

def WriteBranch(tree, branch, filehandle, tablevel):
    t = tree.GetItemText(branch)
    isfolder = (t[0] == '>')
    x = 0
    y = ""
    while x < tablevel:
        y = y + '\t'
        x = x + 1
    y = y + t + "\n"
    filehandle.write(y)
    if isfolder:
        ccount = tree.GetChildrenCount(branch, 0)
        if ccount > 0:
            if (wx.MAJOR_VERSION >= 2) and (wx.MINOR_VERSION >= 5):
                b, cookie = tree.GetFirstChild(branch)
            else:
                b, cookie = tree.GetFirstChild(branch, 1)
            WriteBranch(tree, b, filehandle, (tablevel + 1))
            x = 1
            while x < ccount:
                b, cookie = tree.GetNextChild(branch, cookie)
                WriteBranch(tree, b, filehandle, (tablevel + 1))
                x = x + 1

class drBookmarksDialog(drTreeDialog):

    def __init__(self, parent, bookmarksfile):

        drTreeDialog.__init__(self, parent, 'Edit Bookmarks', 'Bookmarks', bookmarksfile, parent.prefs.bookmarksstyle, \
        'bookmarksdialog.sizeandposition.dat', parent.bitmapdirectory + "/16/bookmark.png", BuildTreeFromString, WriteBranch)

        self.ID_ADD = 1001

        self.btnAdd = wx.Button(self, self.ID_ADD, "&Add")

        self.cmdSizer.Prepend(self.btnAdd, 0, wx.SHAPED)

        self.SetupSizer()

        self.Bind(wx.EVT_BUTTON,  self.OnbtnAdd, id=self.ID_ADD)

    def OnbtnAdd(self, event):
        sel = self.datatree.GetSelection()
        if not sel.IsOk():
            if self.datatree.GetCount() < 2:
                sel = self.datatree.GetRootItem()
            else:
                return
        if self.datatree.GetItemText(sel)[0] == '>':
            d = wx.SingleChoiceDialog(self, "Add Bookmark:", "Add Bookmark", ["Select Directory", "Select File", "Type It In"], wx.OK|wx.CANCEL)
            d.SetSize(wx.Size(250, 200))
            answer = d.ShowModal()
            d.Destroy()
            if answer == wx.ID_OK:
                s = d.GetStringSelection()
                currentItem = None
                if s == "Type It In":
                    d = wx.TextEntryDialog(self, 'Enter Bookmark:', 'Add Bookmark', '')
                    if d.ShowModal() == wx.ID_OK:
                        v = d.GetValue()
                        currentItem = self.datatree.AppendItem(sel, v.replace('\\', '/'))
                    d.Destroy()
                elif s == "Select Directory":
                    d = wx.DirDialog(self, "Select Directory:", style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON|wx.MAXIMIZE_BOX|wx.THICK_FRAME)
                    if self.parent.ddirectory:
                        try:
                            d.SetPath(self.parent.ddirectory)
                        except:
                            drScrolledMessageDialog.ShowMessage(self.parent, ("Error Setting Default Directory To: " + self.parent.ddirectory), "DrPython Error")
                    if d.ShowModal() == wx.ID_OK:
                        currentItem = self.datatree.AppendItem(sel, d.GetPath().replace('\\', '/'))
                    d.Destroy()
                else:
                    dlg = drFileDialog.FileDialog(self.parent, "Select File", self.wildcard)
                    if self.parent.ddirectory:
                        try:
                            dlg.SetDirectory(self.parent.ddirectory)
                        except:
                            drScrolledMessageDialog.ShowMessage(self.parent, ("Error Setting Default Directory To: " + self.parent.ddirectory), "DrPython Error")
                    if dlg.ShowModal() == wx.ID_OK:
                        currentItem = self.datatree.AppendItem(sel, dlg.GetPath().replace("\\", "/"))
                    dlg.Destroy()

                if currentItem is not None:
                    self.datatree.SetItemImage(currentItem, 2, wx.TreeItemIcon_Normal)
                    self.datatree.SetItemImage(currentItem, 2, wx.TreeItemIcon_Selected)
                self.datatree.SetModified()
        else:
            drScrolledMessageDialog.ShowMessage(self, "You can only add a bookmark to a folder.\nSelect either \"Bookmarks\", or a folder.", "Bad Bookmark Folder")
