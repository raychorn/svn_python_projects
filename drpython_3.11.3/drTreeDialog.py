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

#Tree Dialog Base Class

import os.path
import wx
import drScrolledMessageDialog
from drProperty import *

def SortBranch(dialog, branch):
    x = 0
    ccount = dialog.datatree.GetChildrenCount(branch, 0)
    twigs = []
    if ccount > 0:
        b, cookie = dialog.datatree.GetFirstChild(branch)
        twigs.append([dialog.datatree.GetItemText(b), b])
        x = 1
        while x < ccount:
            b, cookie = dialog.datatree.GetNextChild(branch, cookie)
            twigs.append([dialog.datatree.GetItemText(b), b])
            x = x + 1

    twigs.sort()

    x = len(twigs) - 1
    while x > -1:
        dialog.datatree.MoveXToY(twigs[x][1], branch)
        x -= 1

class drTree(wx.TreeCtrl):
    def __init__(self, parent, id, targetbitmap, stylestring, point, size, style):
        wx.TreeCtrl.__init__(self, parent, id, point, size, style)

        self.parent = parent

        self.modified = False

        self.grandparent = self.GetGrandParent()

        yarrr = convertStyleStringToWXFontArray(stylestring)

        imagesize = (16,16)

        self.imagelist = wx.ImageList(imagesize[0], imagesize[1])

        self.images = [wx.BitmapFromImage(wx.Image(self.grandparent.bitmapdirectory + "/16/folder.png", wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(self.grandparent.bitmapdirectory + "/16/folder open.png", wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(targetbitmap, wx.BITMAP_TYPE_PNG))]

        map(self.imagelist.Add, self.images)

        self.AssignImageList(self.imagelist)

        w = wx.Font(yarrr[1], wx.NORMAL, wx.NORMAL, wx.NORMAL, yarrr[2])

        w.SetFaceName(yarrr[0])

        if yarrr[3]:
            w.SetWeight(wx.BOLD)
        else:
            w.SetWeight(wx.NORMAL)
        if yarrr[4]:
            w.SetStyle(wx.ITALIC)
        else:
            w.SetStyle(wx.NORMAL)

        self.SetFont(w)

        f = convertColorPropertyToColorArray(getStyleProperty("fore", stylestring))
        b = convertColorPropertyToColorArray(getStyleProperty("back", stylestring))

        self.TextColor = wx.Colour(f[0], f[1], f[2])

        self.SetForegroundColour(self.TextColor)

        self.badbranch = 0
        self.dragging = 0
        self.draggingId = self.GetRootItem()

        self.SetBackgroundColour(wx.Colour(b[0], b[1], b[2]))

        self.edittext = ""

        self.Bind(wx.EVT_TREE_BEGIN_DRAG,  self.OnBeginDrag, id=id)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,  self.OnItemActivated, id=id)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnLabelEdited)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLabelEdited)

    def GetBadBranch(self):
        return self.badbranch

    def GetModified(self):
        return self.modified

    def MoveChildren(self, fromitem, toitem):
        ccount = self.GetChildrenCount(fromitem, 0)
        if ccount > 0:
            b, cookie = self.GetFirstChild(fromitem)
            newchild = self.InsertItemBefore(toitem, 0, self.GetItemText(b))
            self.SetPyData(newchild, self.GetPyData(b))

            if self.GetChildrenCount(b, 0) > 0:
                self.MoveChildren(b, newchild)

            self.SetIcons(newchild)

            x = 1
            while x < ccount:
                b, cookie = self.GetNextChild(fromitem, cookie)
                newchild = self.InsertItemBefore(toitem, x, self.GetItemText(b))
                self.SetPyData(newchild, self.GetPyData(b))
                if self.GetChildrenCount(b, 0) > 0:
                    self.MoveChildren(b, newchild)
                self.SetIcons(newchild)
                x = x + 1

    def MoveXToY(self, frombranch, tobranch):
        tobranchtext = self.GetItemText(tobranch)
        tobranchparent = self.GetItemParent(tobranch)
        if tobranchtext[0] == '>':
            newbranch = self.InsertItemBefore(tobranch, 0, self.GetItemText(frombranch))
        else:
            newbranch = self.InsertItem(tobranchparent, tobranch, self.GetItemText(frombranch))

        self.SetPyData(newbranch, self.GetPyData(frombranch))
        self.SetIcons(newbranch)

        self.MoveChildren(frombranch, newbranch)

        self.Delete(frombranch)

        return newbranch

    def OnBeginDrag(self, event):
        self.draggingId = self.GetSelection()
        if (self.draggingId == self.GetRootItem()) or (not self.draggingId.IsOk()):
            return

        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.dragging = 1

    def OnItemActivated(self, event):
        sel = self.GetSelection()
        if not sel.IsOk():
            return
        self.edittext = self.GetItemText(sel)
        self.EditLabel(sel)

    def OnLabelEdited(self, event):
        if self.edittext:
            self.SetModified()
            if self.edittext[0] == '>':
                sel = self.GetSelection()
                text = self.GetItemText(sel)
                if not text[0] == '>':
                    self.SetItemText(sel, '>' + text)
        event.Skip()

    def OnLeftUp(self, event):
        self.SetCursor(wx.STANDARD_CURSOR)
        if self.dragging:
            self.dragging = 0
            item, flags = self.HitTest(event.GetPosition())
            if item.IsOk():
                if item == self.draggingId:
                    return

                newbranch = self.MoveXToY(self.draggingId, item)

                self.SelectItem(newbranch)

    def OnMotion(self, event):
        if self.dragging:
            sel, flags = self.HitTest(event.GetPosition())
            if sel.IsOk():
                self.SelectItem(sel)
        event.Skip()

    def SetBadBranch(self, branch):
        self.badbranch = branch

    def SetIcons(self, item):
        text = self.GetItemText(item)
        if text[0] == '>':
            self.SetItemImage(item, 0, wx.TreeItemIcon_Normal)
            self.SetItemImage(item, 1, wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(item, 2, wx.TreeItemIcon_Normal)
            self.SetItemImage(item, 2, wx.TreeItemIcon_Selected)

    def SetModified(self, mod=True):
        self.modified = mod
        if self.modified:
            self.parent.SetTitle(self.parent.title + ' [Modified]')
        else:
            self.parent.SetTitle(self.parent.title)

class drTreeDialog(wx.Dialog):

    def __init__(self, parent, title, rootstring, targetfile, targetstyle, dialogsizefile, bitmapfile, BuildTreeFromString, WriteBranch):
        wx.Dialog.__init__(self, parent, -1, title, wx.Point(50, 50), (-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.title = title

        self.ID_ADD_FOLDER = 1002
        self.ID_REMOVE = 1003
        self.ID_SORT = 1004
        self.ID_SAVE = 1005

        self.parent = parent

        self.BuildTreeFromString = BuildTreeFromString
        self.WriteBranch = WriteBranch

        self.preferencesdirectory = parent.preferencesdirectory
        self.wildcard = parent.prefs.wildcard
        self.targetfile = targetfile
        self.dialogsizefile = dialogsizefile

        self.btnAddFolder = wx.Button(self, self.ID_ADD_FOLDER, "Add &Folder")
        self.btnRemove = wx.Button(self, self.ID_REMOVE, "&Remove")
        self.btnSort = wx.Button(self, self.ID_SORT, "Sort Folder")
        self.btnSave = wx.Button(self, self.ID_SAVE, "&Save")
        self.btnClose = wx.Button(self, 101, "&Close")
        self.btnClose.SetDefault()

        self.datatree = drTree(self, -1, bitmapfile, targetstyle, wx.Point(0, 0), (500, 350), wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS)

        root = self.datatree.AddRoot(">"+rootstring)

        self.datatree.SetItemImage(root, 0, wx.TreeItemIcon_Normal)
        self.datatree.SetItemImage(root, 1, wx.TreeItemIcon_Expanded)

        self.initialize()

        self.datatree.Expand(root)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.cmdSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cmdSizer.Add(self.btnAddFolder, 0, wx.SHAPED)
        self.cmdSizer.Add(self.btnRemove, 0, wx.SHAPED)
        self.cmdSizer.Add(self.btnSort, 0, wx.SHAPED)
        self.cmdSizer.Add(self.btnSave, 0, wx.SHAPED)

        self.theSizer.Add(self.cmdSizer, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.datatree, 9, wx.EXPAND)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.btnClose, 0, wx.SHAPED | wx.ALIGN_CENTER)

        self.Bind(wx.EVT_BUTTON,  self.OnbtnAddFolder, id=self.ID_ADD_FOLDER)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnRemove, id=self.ID_REMOVE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnSort, id=self.ID_SORT)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnClose, id=101)

        self.parent.LoadDialogSizeAndPosition(self, dialogsizefile)

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, self.dialogsizefile)
        if event is not None:
            event.Skip()

    def initialize(self):
        if os.path.exists(self.targetfile):
            try:
                f = open(self.targetfile, 'r')
                self.BuildTreeFromString(self, self.datatree.GetRootItem(), f.read())
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self.parent, ('File Error.\n"'+self.targetfile+'"\n'), "Error")

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
                item = self.datatree.AppendItem(self.datatree.GetSelection(), ">" + v)
                self.datatree.SetItemImage(item, 0, wx.TreeItemIcon_Normal)
                self.datatree.SetItemImage(item, 1, wx.TreeItemIcon_Expanded)
                self.datatree.SetModified()
            d.Destroy()
        else:
            drScrolledMessageDialog.ShowMessage(self, "You can only add a folder to another folder.", "Bad Folder Location")

    def OnbtnClose(self, event):
        if self.datatree.GetModified():
            answer = wx.MessageBox('Save Changes?', self.title, wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            if answer == wx.YES:
                self.OnbtnSave(event)
            elif answer == wx.CANCEL:
                return
        self.Close(1)

    def OnbtnRemove(self, event):
        sel = self.datatree.GetSelection()
        if not sel.IsOk():
            return
        if sel == self.datatree.GetRootItem():
            drScrolledMessageDialog.ShowMessage(self, "You can't remove the Root Item.\n", "Mistake")
            return
        t = self.datatree.GetItemText(sel)
        message = "This will remove the item: " + t
        if self.datatree.GetItemText(sel)[0] == '>':
            message = "This will remove all items in folder: " + t + "!"
        answer = wx.MessageBox((message + "\nAre you sure you want to do this?"), "DrPython", wx.YES_NO | wx.ICON_QUESTION)
        if answer == wx.NO:
            return
        try:
            self.datatree.Delete(sel)
            self.datatree.SetModified()
        except:
            drScrolledMessageDialog.ShowMessage(self, ("Something went wrong trying to remove that item....\nWhat's it called....\nOh yes: " + t + "\n"), "Error")
            return

    def OnbtnSave(self, event):
        try:
            root = self.datatree.GetRootItem()
            f = open(self.targetfile, 'w')
            self.WriteBranch(self.datatree, root, f, 0)
            f.close()
        except IOError:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + self.targetfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return
        self.datatree.SetModified(False)
        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully wrote to:\n"  + self.targetfile), "Success")

    def OnbtnSort(self, event):
        sel = self.datatree.GetSelection()
        if not sel.IsOk():
            return

        #self.datatree.SortChildren(sel)
        SortBranch(self, sel)

        self.datatree.SetModified()

    def SetupSizer(self):
        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

    def GetTreeCtrlItems(self, tree, branch, tablevel, skipfolders = True):

        t = tree.GetItemText(branch)
        isfolder = (t[0] == '>')
        if not isfolder:
            self.curentries.append(t)
        if isfolder:
            ccount = tree.GetChildrenCount(branch, 0)
            if ccount > 0:
                if (wx.MAJOR_VERSION >= 2) and (wx.MINOR_VERSION >= 5):
                    b, cookie = tree.GetFirstChild(branch)
                else:
                    b, cookie = tree.GetFirstChild(branch, 1)
                self.GetTreeCtrlItems(tree, b, tablevel + 1, skipfolders)
                x = 1
                while x < ccount:
                    b, cookie = tree.GetNextChild(branch, cookie)
                    self.GetTreeCtrlItems(tree, b, tablevel + 1, skipfolders)
                    x = x + 1

    def GetCurrentItems(self, skipfolders = True):
        self.curentries = list()
        root = self.datatree.GetRootItem()
        self.GetTreeCtrlItems(self.datatree, root, 0, skipfolders)

