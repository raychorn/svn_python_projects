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

#Pop Up Menu Dialog

import os.path, re
import wx
import drScrolledMessageDialog
import drShortcutsFile

def GetPopUpMenuLabels(filename, frame):
    try:
        f = file(filename, 'r')
        text = f.read()
        f.close()
    except:
        drScrolledMessageDialog.ShowMessage(frame, 'File error with: "' + filename + '".', "ERROR")
        return []

    rePopUpMenu = re.compile(r'^\s*?DrFrame\.AddPluginPopUpMenuFunction\(.*\)', re.MULTILINE)

    allPopUps = rePopUpMenu.findall(text)

    PopUpArray = []

    for s in allPopUps:
        #From the Left most '('
        start = s.find('(')
        #To the Right most ')'
        end = s.rfind(')')

        if (start > -1) and (end > -1):
            s = s[start+1:end]
            i = s.find(',')
            e = i + 1 + s[i+1:].find(',')
            arglabel = s[i+1:e].strip().strip('"')

            PopUpArray.append("<Plugin>:"+arglabel)

    return PopUpArray

class drPopUpMenuDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, ("Customize Pop Up Menu"), wx.DefaultPosition, wx.Size(-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)

        wx.Yield()

        self.ID_PROGRAM = 1001
        self.ID_POPUP = 1002

        self.ID_LIST = 1300

        self.ID_ADD = 1003
        self.ID_REMOVE = 1004
        self.ID_UPDATE = 1005
        self.ID_SAVE = 1006

        self.ID_UP = 1111
        self.ID_DOWN = 2222

        self.parent = parent

        self.theSizer = wx.FlexGridSizer(5, 4, 5, 10)
        self.menubuttonSizer = wx.BoxSizer(wx.VERTICAL)
        self.listSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.datdirectory = parent.datdirectory

        popupmenulist = []

        map(popupmenulist.append, parent.popupmenulist)

        if not popupmenulist:
                popupmenulist = ["<ROOT>", "Undo", "Redo", "<Separator>", "Cut", "Copy", "Paste", "Delete", "<Separator>", "Select All"]
        else:
            popupmenulist.insert(0, "<ROOT>")

        programmenulist = drShortcutsFile.GetShortcutList()

        programmenulist.sort()

        programmenulist.insert(0, "<Insert Separator>")

        self.ListArray = []
        self.ListArray.append(programmenulist)

        #STC

        stclist = []
        map(stclist.append, drShortcutsFile.GetSTCShortcutList())
        stclist.insert(0, "<Insert Separator>")
        self.ListArray.append(stclist)

        #DrScript

        drscriptlist = []
        map(drscriptlist.append, parent.drscriptmenu.titles)
        x = 0
        l = len(drscriptlist)
        while x < l:
            drscriptlist[x] = "<DrScript>:" + drscriptlist[x]
            x = x + 1
        drscriptlist.insert(0, "<Insert Separator>")

        self.ListArray.append(drscriptlist)

        #Plugins
        plist = os.listdir(parent.pluginsdirectory)

        self.PluginList = []
        plugins = []
        for p in plist:
            i = p.find(".py")
            l = len(p)
            if i > -1 and (i + 3 == l):
                self.PluginList.append("<Plugin>:" + p[:i])
                plugins.append(p[:i])

        poplist = []
        for plugin in plugins:
            pluginfile = os.path.join(self.parent.pluginsdirectory, plugin + ".py")
            pluginlist = GetPopUpMenuLabels(pluginfile, self)
            plist = self.parent.GetPluginLabels(pluginfile)
            for p in plist:
                if not (p in pluginlist):
                    pluginlist.append(p)
            if pluginlist:
                pluginlist.insert(0, "<Insert Separator>")
                self.ListArray.append(pluginlist)
            else:
                poplist.append("<Plugin>:" + plugin)

        for popl in poplist:
            i = self.PluginList.index(popl)
            self.PluginList.pop(i)

        list = ["Standard", "Text Control", "DrScript"]
        list.extend(self.PluginList)

        self.cboList = wx.ComboBox(self, self.ID_LIST, "Standard", wx.DefaultPosition, (200, -1), list, wx.CB_DROPDOWN|wx.CB_READONLY)

        self.programmenu = wx.ListBox(self, self.ID_PROGRAM, wx.DefaultPosition, wx.Size(250, 300), programmenulist)

        self.popupmenu = wx.ListBox(self, self.ID_POPUP, wx.DefaultPosition, wx.Size(250, 300), popupmenulist)

        self.btnUp = wx.Button(self, self.ID_UP, " Up ")
        self.btnAdd = wx.Button(self, self.ID_ADD, " ---> ")
        self.btnRemove = wx.Button(self, self.ID_REMOVE, " Remove ")
        self.btnDown = wx.Button(self, self.ID_DOWN, " Down ")

        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnAdd, 0, wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnUp, 0, wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnDown, 0, wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.menubuttonSizer.Add(self.btnRemove, 0, wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.listSizer.Add(wx.StaticText(self, -1, "List: "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.listSizer.Add(self.cboList, 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.listSizer, 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Current List:"), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Pop Up Menu:"), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.programmenu, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.menubuttonSizer, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.popupmenu, 0,  wx.SHAPED | wx.ALIGN_CENTER)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.btnUpdate = wx.Button(self, self.ID_UPDATE, "&Update")
        self.btnSave = wx.Button(self, self.ID_SAVE, "&Save")

        self.btnClose = wx.Button(self, 101, "&Close")
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.btnClose, 0,  wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnUpdate, 0,  wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnSave, 0,  wx.SHAPED | wx.ALIGN_CENTER)
        self.btnClose.SetDefault()

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnbtnUp, id=self.ID_UP)
        self.Bind(wx.EVT_BUTTON, self.OnbtnAdd, id=self.ID_ADD)
        self.Bind(wx.EVT_BUTTON, self.OnbtnRemove, id=self.ID_REMOVE)
        self.Bind(wx.EVT_BUTTON, self.OnbtnDown, id=self.ID_DOWN)
        self.Bind(wx.EVT_BUTTON, self.OnbtnUpdate, id=self.ID_UPDATE)
        self.Bind(wx.EVT_BUTTON, self.OnbtnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.OnbtnClose, id=101)

        self.Bind(wx.EVT_COMBOBOX, self.OnList, id=self.ID_LIST)

        self.parent.LoadDialogSizeAndPosition(self, 'popupmenudialog.sizeandposition.dat')

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, 'popupmenudialog.sizeandposition.dat')
        if event is not None:
            event.Skip()

    def OnbtnAdd(self, event):
        tselection = self.programmenu.GetStringSelection()
        tsel = self.programmenu.GetSelection()
        if tsel == -1:
            drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Add", "Mistake")
            return

        sel = self.popupmenu.GetSelection()
        if sel == -1:
            sel = 0

        separator = (tselection == "<Insert Separator>")
        if separator:
            tselection = "<Separator>"

        self.popupmenu.InsertItems([tselection], sel+1)
        self.popupmenu.SetSelection(sel+1)

    def OnbtnClose(self, event):
        self.Close(1)

    def OnbtnDown(self, event):
        sel = self.popupmenu.GetSelection()
        if sel < self.popupmenu.GetCount()-1 and sel > 0:
            txt = self.popupmenu.GetString(sel)
            self.popupmenu.Delete(sel)
            self.popupmenu.InsertItems([txt], sel+1)
            self.popupmenu.SetSelection(sel+1)

    def OnbtnRemove(self, event):
        sel = self.popupmenu.GetSelection()
        if not sel:
            drScrolledMessageDialog.ShowMessage(self, "You cannot remove the root item.", "Mistake")
            return
        if sel == -1:
            drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Remove", "Mistake")
            return

        self.popupmenu.Delete(sel)
        self.popupmenu.SetSelection(sel-1)

    def OnbtnUp(self, event):
        sel = self.popupmenu.GetSelection()
        if sel > 1:
            txt = self.popupmenu.GetString(sel)
            self.popupmenu.Delete(sel)
            self.popupmenu.InsertItems([txt], sel-1)
            self.popupmenu.SetSelection(sel-1)

    def OnbtnUpdate(self, event):
        y = 0
        c = self.popupmenu.GetCount()

        popupmenulist = []


        while y < c:
            pop = self.popupmenu.GetString(y)
            if not pop == "<ROOT>":
                popupmenulist.append(pop)
            y = y + 1

        self.parent.popupmenulist = popupmenulist

        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully updated the current instance of DrPython.\nClick Save to make it permanent."), "Updated Pop Up Menu")

    def OnbtnSave(self, event):
        y = 0
        c = self.popupmenu.GetCount()

        popupmenustring = ""
        popupmenulist = []

        while y < c:
            pop = self.popupmenu.GetString(y)
            if not pop == "<ROOT>":
                popupmenustring = popupmenustring + pop + "\n"
                popupmenulist.append(pop)
            y = y + 1

        self.parent.popupmenulist = popupmenulist

        popupfile = self.datdirectory + "/popupmenu.dat"
        try:
            f = file(popupfile, 'w')
            f.write(popupmenustring)
            f.close()
        except IOError:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + popupfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return
        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully wrote to:\n"  + popupfile + "\nand updated the current instance of DrPython."), "Saved Pop Up Menu")

    def OnList(self, event):
        sel = self.cboList.GetSelection()

        self.programmenu.Set(self.ListArray[sel])


