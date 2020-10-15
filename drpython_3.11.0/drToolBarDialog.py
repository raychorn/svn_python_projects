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

#ToolBar Menu Dialog

import os.path, re
import wx
import wx.stc
import drScrolledMessageDialog
import drShortcutsFile
import drToolBarFile
import drFileDialog

def GetToolBarLabels(filename, frame):
    try:
        f = file(filename, 'r')
        text = f.read()
        f.close()
    except:
        drScrolledMessageDialog.ShowMessage(frame, 'File error with: "' + filename + '".', "ERROR")
        return []

        # modified 22/10/2006 Jean-Pierre MANDON
        # line: rePopUpMenu = re.compile(r'^\s*?DrFrame\.AddToolBarFunction\(.*\)', re.MULTILINE)
        # replaced with
    rePopUpMenu = re.compile(r'^\s*?DrFrame\.AddPluginToolBarFunction\(.*\)', re.MULTILINE)

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
            # modified 22/10/2006 Jean-Pierre MANDON
            """
            e = i + 1 + s[i+1:].find(',')
            arglabel = s[i+1:e].strip().strip('"')
            """
            # replaced with
            arglabel=s[1:i-1]
            arglabel=arglabel.strip().strip('"')
            # end of modification
            PopUpArray.append("<Plugin>:"+arglabel)

    return PopUpArray

class drToolBarDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Customize ToolBar", wx.DefaultPosition, wx.Size(-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)
        wx.Yield()

        self.parent = parent

        self.ID_PROGRAM = 1001
        self.ID_POPUP = 1002

        self.ID_ADD = 1003
        self.ID_REMOVE = 1004
        self.ID_UPDATE = 1005
        self.ID_SAVE = 1006

        self.ID_LIST = 1300

        self.ID_UP = 1111
        self.ID_DOWN = 2222

        self.ID_16 = 3016
        self.ID_24 = 3024

        self.theSizer = wx.FlexGridSizer(5, 4, 5, 10)
        self.menubuttonSizer = wx.BoxSizer(wx.VERTICAL)
        self.listSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.preferencesdirectory = parent.preferencesdirectory

        ToolBarList = []

        map(ToolBarList.append, parent.ToolBarList)

        #Icons:

        self.customNames, self.customFiles16, self.customFiles24 = drToolBarFile.getCustomBitmaps(self.parent.datdirectory)

        #End Icons

        ToolBarList.insert(0, "<ROOT>")

        programmenulist = drShortcutsFile.GetShortcutList()
        try:
            i = programmenulist.index("Toggle Maximize")
            programmenulist.pop(i)
        except:
            pass

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
            pluginlist = GetToolBarLabels(pluginfile, self)
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

        self.programmenu = wx.ListBox(self, self.ID_PROGRAM, wx.DefaultPosition, wx.Size(250, 250), programmenulist)

        self.toolbaritems = wx.ListBox(self, self.ID_POPUP, wx.DefaultPosition, wx.Size(250, 250), ToolBarList)

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

        self.listSizer.Add(wx.StaticText(self, -1, "List: "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.listSizer.Add(self.cboList, 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.listSizer, 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Current List:"), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "ToolBar:"), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.programmenu, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.menubuttonSizer, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.toolbaritems, 0,  wx.SHAPED | wx.ALIGN_CENTER)

        self.txt16 = wx.TextCtrl(self, -1, "<Default>", wx.DefaultPosition, wx.Size(200, -1), wx.TE_READONLY)
        self.btn16 = wx.Button(self, self.ID_16, "Change")

        self.txt24 = wx.TextCtrl(self, -1, "<Default>", wx.DefaultPosition, wx.Size(200, -1), wx.TE_READONLY)
        self.btn24 = wx.Button(self, self.ID_24, "Change")

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Icon 16x16:"), 0, wx.ALIGN_LEFT)  #AB:with wx.SHAPED only shows 1st word
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "Icon 24x24:"), 0, wx.ALIGN_LEFT)  #AB:with wx.SHAPED only shows 1st word

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.txt16, 0, wx.ALIGN_LEFT | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.txt24, 0, wx.ALIGN_LEFT | wx.SHAPED)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.btn16, 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.theSizer.Add(self.btn24, 0, wx.ALIGN_CENTER | wx.SHAPED)

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

        self.Bind(wx.EVT_BUTTON,  self.OnbtnUp, id=self.ID_UP)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnAdd, id=self.ID_ADD)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnRemove, id=self.ID_REMOVE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnDown, id=self.ID_DOWN)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnUpdate, id=self.ID_UPDATE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnChange16, id=self.ID_16)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnChange24, id=self.ID_24)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnClose, id=101)

        self.Bind(wx.EVT_COMBOBOX, self.OnList, id=self.ID_LIST)
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=self.ID_PROGRAM)

        self.parent.LoadDialogSizeAndPosition(self, 'toolbardialog.sizeandposition.dat')

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, 'toolbardialog.sizeandposition.dat')
        if event is not None:
            event.Skip()

    def OnbtnAdd(self, event):
        tselection = self.programmenu.GetStringSelection()
        tsel = self.programmenu.GetSelection()
        if tsel == -1:
            drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Add", "Mistake")
            return
        separator = (tselection == "<Insert Separator>")
        if separator:
            tselection = "<Separator>"
        sel = self.toolbaritems.GetSelection()
        if sel == -1:
            sel = 0
        self.toolbaritems.InsertItems([tselection], sel+1)
        self.toolbaritems.SetSelection(sel+1)

    def OnbtnChange16(self, event):
        d = wx.SingleChoiceDialog(self.parent, 'Change Icon For 16x16:', "Change Icon", ["Default", "Select File"], wx.CHOICEDLG_STYLE)
        d.SetSize(wx.Size(250, 250))
        answer = d.ShowModal()
        d.Destroy()
        if answer == wx.ID_OK:
            sname = self.programmenu.GetStringSelection()
            i = d.GetSelection()
            newname = "<Default>"
            if i == 1:
                dlg = drFileDialog.FileDialog(self.parent, "Open", "PNG (*.png)|*.png")
                if dlg.ShowModal() == wx.ID_OK:
                    newname = dlg.GetPath()
            self.txt16.SetValue(newname)

            if newname == "<Default>":
                newname = ""

            if sname in self.customNames:
                ci = self.customNames.index(sname)
                self.customFiles16.pop(ci)
                self.customFiles16.insert(ci, newname)
            else:
                self.customNames.append(sname)
                self.customFiles16.append(newname)
                self.customFiles24.append("")

    def OnbtnChange24(self, event):
        d = wx.SingleChoiceDialog(self.parent, 'Change Icon For 24x24:', "Change Icon", ["Default", "Select File"], wx.CHOICEDLG_STYLE)
        d.SetSize(wx.Size(250, 250))
        answer = d.ShowModal()
        d.Destroy()
        if answer == wx.ID_OK:
            sname = self.programmenu.GetStringSelection()
            i = d.GetSelection()
            newname = "<Default>"
            if i == 1:
                dlg = drFileDialog.FileDialog(self.parent, "Open", "PNG (*.png)|*.png")
                if dlg.ShowModal() == wx.ID_OK:
                    newname = dlg.GetPath()
            self.txt24.SetValue(newname)

            if newname == "<Default>":
                newname = ""

            if sname in self.customNames:
                ci = self.customNames.index(sname)
                self.customFiles24.pop(ci)
                self.customFiles24.insert(ci, newname)
            else:
                self.customNames.append(sname)
                self.customFiles16.append("")
                self.customFiles24.append(newname)

    def OnbtnClose(self, event):
        self.Close(1)

    def OnbtnDown(self, event):
        sel = self.toolbaritems.GetSelection()
        if sel < self.toolbaritems.GetCount()-1 and sel > 0:
            txt = self.toolbaritems.GetString(sel)
            self.toolbaritems.Delete(sel)
            self.toolbaritems.InsertItems([txt], sel+1)
            self.toolbaritems.SetSelection(sel+1)

    def OnbtnRemove(self, event):
        sel = self.toolbaritems.GetSelection()
        if not sel:
            drScrolledMessageDialog.ShowMessage(self, "You cannot remove the root item.", "Mistake")
            return
        if sel == -1:
            drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Remove", "Mistake")
            return

        self.toolbaritems.Delete(sel)
        self.toolbaritems.SetSelection(sel-1)

    def OnbtnUp(self, event):
        sel = self.toolbaritems.GetSelection()
        if sel > 1:
            txt = self.toolbaritems.GetString(sel)
            self.toolbaritems.Delete(sel)
            self.toolbaritems.InsertItems([txt], sel-1)
            self.toolbaritems.SetSelection(sel-1)

    def OnbtnUpdate(self, event):
        y = 0
        c = self.toolbaritems.GetCount()

        ToolBarList = []

        while y < c:
            pop = self.toolbaritems.GetString(y)
            if not pop == "<ROOT>":
                ToolBarList.append(pop)
            y = y + 1

        self.parent.ToolBarList = ToolBarList

        if self.parent.hasToolBar:
            self.parent.DestroyToolBar()
            self.parent.SetToolBar(None)
            self.parent.toolbar = wx.ToolBar(self.parent, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
            self.parent.ToolBarIdList = self.parent.SetupToolBar()

            if self.parent.prefs.iconsize > 0:
                self.parent.SetToolBar(self.parent.toolbar)

            thereisafile = (len(self.parent.txtDocument.filename) > 0)
            self.parent.toolbar.EnableTool(self.parent.ID_RELOAD, thereisafile)

            if self.parent.txtPrompt.pid == -1:
                self.parent.toolbar.EnableTool(self.parent.ID_PYTHON, True)
                self.parent.toolbar.EnableTool(self.parent.ID_END, False)
                self.parent.toolbar.EnableTool(self.parent.ID_RUN, thereisafile)
                self.parent.toolbar.EnableTool(self.parent.ID_SET_ARGS, thereisafile)
            else:
                self.parent.toolbar.EnableTool(self.parent.ID_PYTHON, False)
                self.parent.toolbar.EnableTool(self.parent.ID_END, True)
                if thereisafile:
                    self.parent.toolbar.EnableTool(self.parent.ID_RUN, False)
                    self.parent.toolbar.EnableTool(self.parent.ID_SET_ARGS, False)

        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully updated the current instance of DrPython.\nClick Save to make it permanent."), "Updated ToolBar")

    def OnbtnSave(self, event):
        toolbarfile = self.parent.datdirectory + "/toolbar.dat"

        msg = "Succesfully wrote to:\n"  + toolbarfile + "\nand updated the current instance of DrPython."

        #Custom Bitmaps.
        if self.customNames:
            toolbarcustomfile = self.parent.datdirectory + "/toolbar.custom.icons.dat"
            f = file(toolbarcustomfile, 'w')
            x = 0
            l = len(self.customNames)
            while x < l:
                if (len(self.customFiles16[x]) > 0) or (len(self.customFiles24[x]) > 0):
                    f.write("<Name>"+self.customNames[x]+"</Name><16>"+self.customFiles16[x]+"</16><24>"+self.customFiles24[x]+"</24>\n")
                x = x + 1
            f.close()
            msg = msg + "\n\nSuccesfully Saved Custom ToolBar Icons."

        y = 0
        c = self.toolbaritems.GetCount()

        toolbaritemsstring = ""
        ToolBarList = []

        while y < c:
            pop = self.toolbaritems.GetString(y)
            if not pop == "<ROOT>":
                toolbaritemsstring = toolbaritemsstring + pop + "\n"
                ToolBarList.append(pop)
            y = y + 1

        self.parent.ToolBarList = ToolBarList

        if self.parent.hasToolBar:
            if self.parent.toolbar is not None:
                self.parent.SetToolBar(None)

            self.parent.DestroyToolBar()
            self.parent.toolbar = wx.ToolBar(self.parent, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
            self.parent.ToolBarIdList = self.parent.SetupToolBar()

            if self.parent.prefs.iconsize > 0:
                self.parent.SetToolBar(self.parent.toolbar)

            thereisafile = (len(self.parent.txtDocument.filename) > 0)
            self.parent.toolbar.EnableTool(self.parent.ID_RELOAD, thereisafile)

            if self.parent.txtPrompt.pid == -1:
                self.parent.toolbar.EnableTool(self.parent.ID_PYTHON, True)
                self.parent.toolbar.EnableTool(self.parent.ID_END, False)
                self.parent.toolbar.EnableTool(self.parent.ID_RUN, thereisafile)
                self.parent.toolbar.EnableTool(self.parent.ID_SET_ARGS, thereisafile)
            else:
                self.parent.toolbar.EnableTool(self.parent.ID_PYTHON, False)
                self.parent.toolbar.EnableTool(self.parent.ID_END, True)
                if thereisafile:
                    self.parent.toolbar.EnableTool(self.parent.ID_RUN, False)
                    self.parent.toolbar.EnableTool(self.parent.ID_SET_ARGS, False)

        try:
            f = file(toolbarfile, 'w')
            f.write(toolbaritemsstring)
            f.close()
        except IOError:
            drScrolledMessageDialog.ShowMessage(self, ("There were some problems writing to:\n"  + toolbarfile + "\nEither the file is having metaphysical issues, or you do not have permission to write.\nFor metaphysical issues, consult the documentation.\nFor permission issues, change the permissions on the directory to allow yourself write access.\nDrPython will now politely ignore your request to save.\nTry again when you have fixed the problem."), "Write Error")
            return
        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, msg, "Saved ToolBar")

    def OnList(self, event):
        sel = self.cboList.GetSelection()

        self.programmenu.Set(self.ListArray[sel])

    def OnSelect(self, event):
        #Take one away for "Insert Separator"
        seltext = self.programmenu.GetStringSelection()

        if seltext in self.customNames:
            i = self.customNames.index(seltext)
            if self.customFiles16[i]:
                self.txt16.SetValue(self.customFiles16[i])
            else:
                self.txt16.SetValue("<Default>")
            if self.customFiles24[i]:
                self.txt24.SetValue(self.customFiles24[i])
            else:
                self.txt24.SetValue("<Default>")
        else:
            self.txt16.SetValue("<Default>")
            self.txt24.SetValue("<Default>")