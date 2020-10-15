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

#Plugins Dialog

import os, shutil, zipfile, tempfile, urllib, thread, sys
import wx, wx.wizard, wx.lib.dialogs, wx.html, wx.lib.newevent
import drScrolledMessageDialog
import drFileDialog
from drPrefsFile import ExtractPreferenceFromText

#*******************************************************************************
#Update Plugin List Dialog

(UpdatePluginDialog, EVT_UPDATE_PLUGINDIALOG) = wx.lib.newevent.NewEvent()

class drUpdatePluginListDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Updating Plugin List", wx.DefaultPosition, (300, 200), wx.DEFAULT_DIALOG_STYLE)

        self.parent = parent.parent

        self.stxtDownload = wx.StaticText(self, -1, "Downloading...")

        self.txtStatus = wx.TextCtrl(self, -1, '', size=(250, -1), style=wx.TE_READONLY)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(self.stxtDownload, 0, wx.EXPAND)
        self.theSizer.Add(self.txtStatus, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(EVT_UPDATE_PLUGINDIALOG, self.UpdateUI)

        self.error = False

        thread.start_new_thread(self.RunInThread, ())

    def RunInThread(self):
        self.error = False
        wx.PostEvent(self, UpdatePluginDialog(status = 'Plugin List: Connecting...'))
        targetfile = self.parent.ancestor.pluginsdirectory + "/drpython.plugin.list.dat"
        try:
            u = urllib.urlopen('http://drpython.sourceforge.net/cgi-bin/GetPluginList.py')

            result = 'Philosophia'
            data = ''
            x = 0
            while len(result) > 0:
                result = u.read(1)

                if (x % 1024) == 0:
                    wx.PostEvent(self, UpdatePluginDialog(status = 'Plugin List: ' + str(x / 1024) + 'kb Read'))

                x += 1

                if result:
                    data += result

            u.close()
        except:
            self.error = True
            wx.PostEvent(self, UpdatePluginDialog(status = 'Plugin List: Error'))
            return

        if data.find('<Plugins>') != 0:
            self.error = True
            wx.PostEvent(self, UpdatePluginDialog(status = 'Plugin List: Error'))
            return

        try:
            f = open(targetfile, 'wb')
            f.write(data)
            f.close()
        except:
            self.error = True
            wx.PostEvent(self, UpdatePluginDialog(status = 'Plugin List: Error'))
            return

        wx.PostEvent(self, UpdatePluginDialog(status = 'Plugin List: Done.'))

        self.EndModal(0)

    def UpdateUI(self, event):
        self.txtStatus.SetValue(event.status)
        if self.error:
            errormessage = '''Error Downloading Plugin List From Selected Mirror.
If you proceed, DrPython will use the copy
which came with this version of the core program.
This copy may be out of date.

Please try a different mirror.'''
            drScrolledMessageDialog.ShowMessage(self, errormessage, 'Plugin List Error')
            self.EndModal(0)




#*******************************************************************************
#Select Plugins Dialog
class drSelectPluginsDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Select DrPython Plugin", wx.DefaultPosition, (600, 400), wx.DEFAULT_DIALOG_STYLE)

        self.Plugins = []

        self.parent = parent

        #Local For Test
        self.pluginlistfile = parent.pluginsdirectory + "/drpython.plugin.list.dat"
        if not os.path.exists(self.pluginlistfile):
            self.pluginlistfile = parent.programdirectory + "/drpython.plugin.list.dat"

        self.txtSearch = wx.TextCtrl(self, -1, '', size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.choType = wx.Choice(self, -1, choices=['Keyword', 'Title', 'Author', 'Description'])
        self.chkCaseSensitive = wx.CheckBox(self, -1, 'Case Sensitive')
        self.btnSearch = wx.Button(self, wx.ID_FIND, 'Search')
        self.btnClear = wx.Button(self, wx.ID_CLEAR)

        self.choType.SetSelection(0)

        self.lstPlugins = wx.CheckListBox(self, wx.ID_ANY, size=(300, 300))
        self.htmlData = wx.html.HtmlWindow(self, size=(300, 300))

        self.btnCancel = wx.Button(self, wx.ID_CANCEL)
        self.btnOk = wx.Button(self, wx.ID_OK)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer = wx.FlexGridSizer(0, 2, 10, 10)
        self.searchSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.searchSizer.Add(self.txtSearch, 1, wx.EXPAND)
        self.searchSizer.Add(self.choType, 0, wx.SHAPED)
        self.searchSizer.Add(self.chkCaseSensitive, 0, wx.SHAPED)
        self.searchSizer.Add(self.btnSearch, 0, wx.SHAPED)
        self.searchSizer.Add(self.btnClear, 0, wx.SHAPED)

        self.mainSizer.Add(self.lstPlugins, 0, wx.SHAPED)
        self.mainSizer.Add(self.htmlData, 0, wx.SHAPED)
        self.mainSizer.Add(self.btnCancel, 0, wx.SHAPED)
        self.mainSizer.Add(self.btnOk, 0, wx.SHAPED | wx.ALIGN_RIGHT)

        self.theSizer.Add(self.searchSizer, 0, wx.EXPAND)
        self.theSizer.Add(self.mainSizer, 0, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.ReadPluginList()

        self.Bind(wx.EVT_LISTBOX, self.OnSelectPlugin, self.lstPlugins)
        self.Bind(wx.EVT_BUTTON, self.OnbtnSearch, self.btnSearch)
        self.Bind(wx.EVT_BUTTON, self.OnbtnClear, self.btnClear)
        self.txtSearch.Bind(wx.EVT_CHAR, self.OnChar)

    def GetPluginFileText(self, text):
        #Protects against invalid values in the plugin list file.
        data = ''
        for character in text:
            c = ord(character)
            if (c < 128) and (c >= 0):
                data += character

        return data


    def GetPluginData(self, pluginindex, dataindex, casesensitive):
        data = self.PluginDataArray[pluginindex][dataindex]

        if casesensitive:
            return data.lower()
        return data

    def GetSelectedPlugins(self):
        selections = []
        l = self.lstPlugins.GetCount()
        x = 0

        while x < l:
            if self.lstPlugins.IsChecked(x):
                selections.append(x)
            x += 1

        pluginfilenames = []

        for selection in selections:
            pluginfilenames.append(self.lstPlugins.GetString(selection) + '-' + self.PluginDataArray[selection][0] + '.zip')

        return pluginfilenames

    def OnbtnClear(self, event):
        self.txtSearch.SetValue('')
        self.OnbtnSearch(event)

    def OnbtnSearch(self, event):
        stext = self.txtSearch.GetValue()
        if not stext:
            self.PluginDataArrayForLST = list(self.PluginDataArray)
            self.lstPlugins.Set(self.Plugins)
            return

        t = self.choType.GetSelection() - 1

        self.PluginDataArrayForLST = []
        pluginlist = []
        x = 0
        casesensitive = self.chkCaseSensitive.GetValue()
        for plugin in self.Plugins:
            if self.SearchPlugin(stext, t, plugin, casesensitive):
                pluginlist.append(plugin)
                self.PluginDataArrayForLST.append(self.PluginDataArray[x])
            x += 1
        self.lstPlugins.Set(pluginlist)

    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.OnbtnSearch(None)
        event.Skip()

    def OnSelectPlugin(self, event):
        sel = self.lstPlugins.GetSelection()
        if sel == -1:
            return
        txt = self.lstPlugins.GetStringSelection()

        htmltxt = '''<html><body><b>Name:</b> %s<br>
<br>
<b>Version:</b> %s<br>
<br>
<b>Author(s):</b> %s<br>
<br>
<b>Description:</b><br>
<br> %s<br>
<br></html></body>''' % (txt, self.PluginDataArrayForLST[sel][0], self.PluginDataArrayForLST[sel][1], self.PluginDataArrayForLST[sel][2])

        self.htmlData.SetPage(htmltxt)

    def ReadPluginList(self):
        try:
            f = open(self.pluginlistfile, 'r')
            text = self.GetPluginFileText(f.read())
            f.close()

            self.Plugins = ExtractPreferenceFromText(text, 'Plugins').strip().split('\n')

            if not self.Plugins:
                drScrolledMessageDialog.ShowMessage(self, 'Corrupt Plugin List, Trying Default', 'Error')
                self.pluginlistfile = self.parent.programdirectory + "/drpython.plugin.list.dat"
                f = open(self.pluginlistfile, 'r')
                text = f.read()
                f.close()

                self.Plugins = ExtractPreferenceFromText(text, 'Plugins').strip().split('\n')

            self.PluginDataArray = []

            for plugin in self.Plugins:
                plugintext = ExtractPreferenceFromText(text, plugin).strip()
                version = ExtractPreferenceFromText(plugintext, 'Version').strip()
                author = ExtractPreferenceFromText(plugintext, 'Author').strip()
                description = ExtractPreferenceFromText(plugintext, 'Description').strip()
                self.PluginDataArray.append([version, author, description])

            self.PluginDataArrayForLST = list(self.PluginDataArray)

            self.lstPlugins.Set(self.Plugins)

        except:
            drScrolledMessageDialog.ShowMessage(self, 'Error Reading "' + self.pluginlistfile + '".', 'Error Reading Plugin List')

    def SearchPlugin(self, searchtext, type, pluginname, casesensitive):
        if casesensitive:
            if type == 0:
                return pluginname.find(searchtext) > -1
            elif (type < 3) and (type > -1):
                if pluginname in self.Plugins:
                    i = self.Plugins.index(pluginname)
                    return self.GetPluginData(i, type, 0).find(searchtext) > -1
                return False
            else:
                if pluginname.find(searchtext) > -1:
                    return True
                elif pluginname in self.Plugins:
                    i = self.Plugins.index(pluginname)
                    if self.GetPluginData(i, 0, 0).find(searchtext) > -1:
                        return True
                    elif self.GetPluginData(i, 1, 0).find(searchtext) > -1:
                        return True
                    elif self.GetPluginData(i, 2, 0).find(searchtext) > -1:
                        return True
        else:
            searchtext = searchtext.lower()
            if type == 0:
                return pluginname.lower().find(searchtext) > -1
            elif (type < 3) and (type > -1):
                if pluginname in self.Plugins:
                    i = self.Plugins.index(pluginname)
                    return self.GetPluginData(i, type, 1).find(searchtext) > -1
                return False
            else:
                if pluginname.lower().find(searchtext) > -1:
                    return True
                elif pluginname in self.Plugins:
                    i = self.Plugins.index(pluginname)
                    if self.GetPluginData(i, 0, 1).find(searchtext) > -1:
                        return True
                    elif self.GetPluginData(i, 1, 1).find(searchtext) > -1:
                        return True
                    elif self.GetPluginData(i, 2, 1).find(searchtext) > -1:
                        return True
        return False

#*******************************************************************************
#Install Wizard

class drPluginInstallLocationPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.parent = parent

        title = wx.StaticText(self, -1, "Select Location:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.radLocation = wx.RadioBox(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, ["Local", "SourceForge Mirror"], 1, wx.RA_SPECIFY_COLS | wx.NO_BORDER)

        mirrors = ['Bern, Switzerland (Europe)', 'Brussels, Belgium (Europe)', 'Chapel Hill, NC (North America)', 'Duesseldorf, Germany (Europe)', \
        'Dublin, Ireland (Europe)', 'Minneapolis, MN (North America)', 'New York, New York (North America)', 'Paris, France (Europe)', \
        'Phoenix, AZ (North America)', 'Reston, VA (North America)', 'SourceForge (OSDN)', 'Sydney, Australia (Australia)', 'Zurich, Switzerland  (Europe)']

        self.mirrorAddresses = ['http://puzzle.dl.sourceforge.net/', 'http://belnet.dl.sourceforge.net/', 'http://unc.dl.sourceforge.net/', 'http://mesh.dl.sourceforge.net/', \
        'http://heanet.dl.sourceforge.net/', 'http://umn.dl.sourceforge.net/', 'http://voxel.dl.sourceforge.net/', 'http://ovh.dl.sourceforge.net/', \
        'http://easynews.dl.sourceforge.net/sourceforge/', 'http://aleron.dl.sourceforge.net/', 'http://osdn.dl.sourceforge.net/', 'http://optusnet.dl.sourceforge.net/', 'http://switch.dl.sourceforge.net/']

        self.lstMirrors = wx.ListBox(self, wx.ID_ANY, size=(300, 300), choices=mirrors)
        self.lstMirrors.SetSelection(0)
        self.lstMirrors.Enable(False)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(self.radLocation, 0, wx.SHAPED)
        self.theSizer.Add(self.lstMirrors, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_RADIOBOX, self.OnLocationChanged, self.radLocation)
        self.Bind(wx.EVT_LISTBOX, self.OnMirrorChanged, self.lstMirrors)

    def OnLocationChanged(self, event):
        isSF = self.radLocation.GetSelection()
        self.lstMirrors.Enable(isSF)
        self.parent.Location = isSF
        if isSF:
            self.OnMirrorChanged(None)

    def OnMirrorChanged(self, event):
        i = self.lstMirrors.GetSelection()
        if i < 0:
            i = 0
        self.parent.Mirror = self.mirrorAddresses[i]

class drPluginInstallSelectPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.parent = parent

        title = wx.StaticText(self, -1, "Select Plugins to Install:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.btnAdd = wx.Button(self, wx.ID_ADD)
        self.btnRemove = wx.Button(self, wx.ID_REMOVE)

        self.lstPlugins = wx.ListBox(self, wx.ID_ANY, size=(300, 300))

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.bSizer.Add(self.btnAdd, 0, wx.SHAPED | wx.ALIGN_LEFT)
        self.bSizer.Add(self.btnRemove, 0, wx.SHAPED | wx.ALIGN_RIGHT)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.bSizer, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.lstPlugins, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.btnAdd)
        self.Bind(wx.EVT_BUTTON, self.OnRemove, self.btnRemove)

    def OnAdd(self, event):
        if self.parent.Location:
            #SourceForge
            d = drSelectPluginsDialog(self.parent.ancestor)
            answer = d.ShowModal()
            self.Raise()
            self.SetFocus()
            if answer == wx.ID_OK:
                selectedplugins = d.GetSelectedPlugins()
                for plugin in selectedplugins:
                    self.parent.pluginstodownload.append(self.parent.Mirror + 'sourceforge/drpython/' + plugin)
                labels = map(lambda x: os.path.splitext(x)[0], selectedplugins)
                self.parent.pluginlabels.extend(labels)
                self.parent.pluginsinstallmethod.extend(map(lambda x: 0, labels))
                self.lstPlugins.Set(self.parent.pluginlabels)
            d.Destroy()
        else:
            #Local
            dlg = drFileDialog.FileDialog(self.parent.ancestor, "Select DrPython Plugin(s)", self.parent.wildcard, MultipleSelection=True)
            if self.parent.ancestor.pluginsdirectory:
                dlg.SetDirectory(self.parent.ancestor.pluginsdirectory)
            if dlg.ShowModal() == wx.ID_OK:
                filenames = dlg.GetPaths()
                filenames = map(lambda x: x.replace("\\", '/'), filenames)
                self.parent.pluginstoinstall.extend(filenames)
                labels = map(lambda x: os.path.splitext(os.path.split(x)[1])[0], filenames)
                self.parent.pluginlabels.extend(labels)
                self.parent.pluginsinstallmethod.extend(map(lambda x: 0, labels))
                self.lstPlugins.Set(self.parent.pluginlabels)
            dlg.Destroy()

    def OnRemove(self, event):
        i = self.lstPlugins.GetSelection()
        if i < 0:
            return
        answer = wx.MessageBox('Remove "%s"?' % self.parent.pluginlabels[i], "Remove Plugin From List", wx.YES_NO | wx.ICON_QUESTION)
        if answer == wx.YES:
            self.parent.pluginlabels.pop(i)
            if self.parent.Location:
                self.parent.pluginstodownload.pop(i)
            else:
                self.parent.pluginstoinstall.pop(i)
            self.lstPlugins.Set(self.parent.pluginlabels)

    def Run(self):
        if self.parent.Location:
            answer = wx.MessageBox('Update Plugin List?', "Update Plugin List", wx.YES_NO | wx.ICON_QUESTION)
            if answer == wx.YES:
                e = drUpdatePluginListDialog(self)
                e.ShowModal()
                e.Destroy()

            #Make sure plugion labels are synced with list:
            self.lstPlugins.Set(self.parent.pluginlabels)

(UpdateDownloadPage, EVT_UPDATE_DOWNLOADPAGE) = wx.lib.newevent.NewEvent()

class drPluginInstallDownloadPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.parent = parent

        self.errors = []

        title = wx.StaticText(self, -1, "Getting Selected Plugins:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.stxtDownload = wx.StaticText(self, -1, "Downloading...")
        self.stxtUnPacking = wx.StaticText(self, -1, "UnPacking...")
        self.stxtDone = wx.StaticText(self, -1, "Done")

        self.stxtDownload.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtUnPacking.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtDone.SetForegroundColour(self.GetBackgroundColour())

        self.gDownload = wx.Gauge(self, -1, 0, size=(250, -1))
        self.gUnPack = wx.Gauge(self, -1, 0, size=(250, -1))

        self.txtStatus = wx.TextCtrl(self, -1, '', size=(250, -1), style=wx.TE_READONLY)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtDownload, 0, wx.SHAPED)
        self.theSizer.Add(self.gDownload, 0, wx.SHAPED)
        self.theSizer.Add(self.txtStatus, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtUnPacking, 0, wx.SHAPED)
        self.theSizer.Add(self.gUnPack, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtDone, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(EVT_UPDATE_DOWNLOADPAGE, self.UpdateUI)

    def CreateDirectories(self, targetdir, zippedfilename):
        zippedfilename = zippedfilename.replace('\\', '/')
        d = zippedfilename.find('/')
        while d > -1:
            dir = zippedfilename[:d]
            targetdir = targetdir + '/' + dir
            if not os.path.exists(targetdir):
                os.mkdir(targetdir)
            zippedfilename = zippedfilename[d+1:]
            d = zippedfilename.find('/')

    def Download(self, remotefile, label):
        try:
            targetfile = self.parent.tempdir + label + '.zip'
            wx.PostEvent(self, UpdateDownloadPage(step = 0, range = -1, value = -1, done = False, status = label + '.zip: Connecting...'))
            u = urllib.urlopen(remotefile)
            mimetype = u.info().gettype()
            if mimetype != 'application/zip':
                u.close()
                self.errors.append([remotefile, 'MimeType Info: "' + mimetype + '"'])
                return ''

            result = 'Philosophia'
            data = ''
            x = 0
            while len(result) > 0:
                result = u.read(1)

                if (x % 1024) == 0:
                    wx.PostEvent(self, UpdateDownloadPage(step = 0, range = -1, value = -1, done = False, status = label + '.zip: ' + str(x / 1024) + 'kb Read'))

                x += 1

                if result:
                    data += result

            u.close()

            f = open(targetfile, 'wb')
            f.write(data)
            f.close()

            return targetfile
        except:
            self.errors.append([remotefile, str(sys.exc_info()[0]).lstrip("exceptions.") + ": " + str(sys.exc_info()[1])])
        return ''

    def Run(self):
        thread.start_new_thread(self.RunInThread, ())

    def RunInThread(self):
        #Download
        if self.parent.Location:
            l = len(self.parent.pluginstodownload)
            x = 0
            wx.PostEvent(self, UpdateDownloadPage(step = 0, range = l, value = x, done = False, status=''))
            self.parent.pluginstoinstall = []
            while x < l:
                result = self.Download(self.parent.pluginstodownload[x], self.parent.pluginlabels[x])
                if result:
                    self.parent.pluginstoinstall.append(result)
                x = x + 1
                wx.PostEvent(self, UpdateDownloadPage(step = 0, range = l, value = x, done = False, status= ''))

            #Update arrays based on what was downloaded
            self.parent.pluginlabels = map(lambda x: os.path.splitext(os.path.split(x)[1])[0], self.parent.pluginstoinstall)
            self.parent.pluginsinstallmethod = (map(lambda x: 0, self.parent.pluginlabels))

            wx.PostEvent(self, UpdateDownloadPage(step = 0, range = l, value = x, done = True, status= ''))

        #UnPack
        l = len(self.parent.pluginstoinstall)

        wx.PostEvent(self, UpdateDownloadPage(step = 1, range = l, value = 0, done = False, status= ''))

        x = 0
        while x < l:
            self.UnPack(self.parent.pluginstoinstall[x], self.parent.pluginlabels[x])
            x = x + 1
            wx.PostEvent(self, UpdateDownloadPage(step = 1, range = l, value = x, done = False, status= ''))

        wx.PostEvent(self, UpdateDownloadPage(step = 1, range = l, value = x, done = True, status= ''))

    def UnPack(self, filename, label):
        zf = zipfile.ZipFile(filename, 'r')

        dir = self.parent.tempdir + label

        if not os.path.exists(dir):
            os.mkdir(dir)

        zippedfiles = zf.namelist()

        self.parent.UnZippedFilesArray.append(zippedfiles)

        for zippedfile in zippedfiles:
            l = len(zippedfile)
            if (zippedfile[l-1] == '/') or (zippedfile[l-1] == '\\'):
                self.CreateDirectories(dir, zippedfile)
            else:
                self.CreateDirectories(dir, zippedfile)
                data = zf.read(zippedfile)
                f = open(dir + '/' + zippedfile, 'wb')
                f.write(data)
                f.close()

        zf.close()

    def UpdateUI(self, event):
        if event.step == 0:
            if event.status:
                self.txtStatus.SetValue(event.status)
            else:
                if not event.done:
                    self.stxtDownload.SetForegroundColour(self.GetForegroundColour())
                else:
                    self.stxtDownload.SetForegroundColour(wx.Colour(175, 175, 175))
                if event.range != self.gDownload.GetRange():
                    self.gDownload.SetRange(event.range)
                self.gDownload.SetValue(event.value)
        elif event.step == 1:
            if not event.done:
                self.stxtUnPacking.SetForegroundColour(self.GetForegroundColour())
            else:
                self.stxtUnPacking.SetForegroundColour(wx.Colour(175, 175, 175))
                self.stxtDone.SetForegroundColour(self.GetForegroundColour())
            if event.range != self.gUnPack.GetRange():
                self.gUnPack.SetRange(event.range)
            self.gUnPack.SetValue(event.value)

        self.Refresh()

        if self.errors:
            error = self.errors.pop(0)
            drScrolledMessageDialog.ShowMessage(self.parent, 'Error Downloading File "' + error[0] + '".\n\n' + error[1], "Error", wx.DefaultPosition, (550,300))

class drPluginInstallIndexPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.parent = parent

        title = wx.StaticText(self, -1, "Set Loading Method:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.chklLoadByDefault = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, (200, 100), self.parent.pluginlabels)

        self.chklLoadFromIndex = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, (200, 100), self.parent.pluginlabels)

        self.theSizer = wx.FlexGridSizer(0, 1, 5, 5)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, "Load By Default:"), 0, wx.EXPAND)
        self.theSizer.Add(self.chklLoadByDefault, 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, "Load From Index:"), 0, wx.EXPAND)
        self.theSizer.Add(self.chklLoadFromIndex, 0, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_CHECKLISTBOX, self.OnLoadByDefault, self.chklLoadByDefault)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnLoadFromIndex, self.chklLoadFromIndex)

    def GetDefSel(self, IndexSel):
        txt = self.chklLoadFromIndex.GetString(IndexSel)
        return self.chklLoadByDefault.FindString(txt)

    def GetIdxSel(self, DefaultSel):
        txt = self.chklLoadByDefault.GetString(DefaultSel)
        return self.chklLoadFromIndex.FindString(txt)

    def OnLoadByDefault(self, event):
        sel = event.GetSelection()
        i = self.GetIdxSel(sel)
        if sel > -1:
            if self.chklLoadByDefault.IsChecked(sel) and (i > -1):
                self.parent.pluginsinstallmethod[sel] = 0
                self.chklLoadFromIndex.Check(i, False)
            elif i > -1:
                if not self.chklLoadFromIndex.IsChecked(i):
                    self.parent.pluginsinstallmethod[sel] = -1

    def OnLoadFromIndex(self, event):
        sel = event.GetSelection()
        i = self.GetDefSel(sel)
        if sel > -1:
            if self.chklLoadFromIndex.IsChecked(sel) and (i > -1):
                self.parent.pluginsinstallmethod[i] = 1
                self.chklLoadByDefault.Check(i, False)
            elif not self.chklLoadByDefault.IsChecked(sel) and (i > -1):
                self.parent.pluginsinstallmethod[i] = -1

    def Run(self):
        if not self.parent.pluginstoinstall:
            return
        self.chklLoadByDefault.Set(self.parent.pluginlabels)
        indexlabels = []
        x = 0
        for label in self.parent.pluginlabels:
            pluginname = label
            if pluginname.find('-') > -1:
                pluginname = pluginname[:pluginname.find('-')]
            if pluginname.find('.') > -1:
                pluginname = pluginname[:pluginname.find('.')]
            for fn in self.parent.UnZippedFilesArray[x]:
                if fn.find(pluginname + '.idx') > -1:
                    indexlabels.append(label)
                    break
            x += 1
        self.chklLoadFromIndex.Set(indexlabels)

        x = 0
        l = len(self.parent.pluginlabels)
        while x < l:
            self.chklLoadByDefault.Check(x, True)
            x = x + 1

class drPluginInstallInstallPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.parent = parent

        title = wx.StaticText(self, -1, "Installing Selected Plugins:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.stxtInstalling = wx.StaticText(self, -1, "Installing...")
        self.stxtIndexing = wx.StaticText(self, -1, "Indexing...")
        self.stxtDone = wx.StaticText(self, -1, "Done")

        self.stxtInstalling.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtIndexing.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtDone.SetForegroundColour(self.GetBackgroundColour())

        self.gInstall = wx.Gauge(self, -1, 0, size=(200, -1))
        self.gIndex = wx.Gauge(self, -1, 0, size=(200, -1))

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtInstalling, 0, wx.SHAPED)
        self.theSizer.Add(self.gInstall, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtIndexing, 0, wx.SHAPED)
        self.theSizer.Add(self.gIndex, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtDone, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

    def RemoveTempDir(self, tempdir):
        entries = os.listdir(tempdir)

        for entry in entries:
            fname = tempdir + '/' + entry
            if os.path.isdir(fname):
                self.RemoveTempDir(fname)
            else:
                os.remove(fname)

        os.rmdir(tempdir)

    def Index(self, label, unzippedfiles, installmethod):
        dir = self.parent.tempdir + label

        pluginname = label
        if pluginname.find('-') > -1:
            pluginname = pluginname[:pluginname.find('-')]
        if pluginname.find('.') > -1:
            pluginname = pluginname[:pluginname.find('.')]

        if installmethod == 0:
            #indexfile = self.parent.preferencesdirectory + "/default.idx"
            #AB:
            #print self.parent.preferencesdirectory
            #print self.parent.pluginsbasepreferencesdir
            indexfile = self.parent.GetParent().preferencesdirectory + "/default.idx"
            if not os.path.exists(indexfile):
                f = open(indexfile, 'wb')
                #f.write('\n')
                f.close()
            try:
                f = open(indexfile, 'rU')
                plugins = [x.strip() for x in f]
                f.close()

                f = open(indexfile, 'w')
                for p in plugins:
                    if p != pluginname:
                        f.write(p + '\n')
                f.write(pluginname + '\n')
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self.parent, 'Error Adding Plugin "' + pluginname +
                    '" to default.idx"', "Error",  wx.DefaultPosition, (550,300))
                return

        elif installmethod == 1:
            target = pluginname + '.idx'

            indexfile = ''

            for fname in unzippedfiles:
                if os.path.split(fname)[1] == target:
                    indexfile = dir + '/' + fname

            if not indexfile:
                drScrolledMessageDialog.ShowMessage(self.parent, 'Error Installing "' + label + '"', 'Install Index Error')
                return

            shutil.copyfile(indexfile, os.path.join(self.parent.pluginsdirectory , target))

    def Install(self, filename, label, unzippedfiles):
        pluginname = label
        if pluginname.find('-') > -1:
            pluginname = pluginname[:pluginname.find('-')]
        if pluginname.find('.') > -1:
            pluginname = pluginname[:pluginname.find('.')]

        dir = self.parent.tempdir + label

        target = pluginname + '.py'

        pluginfile = ''

        for fname in unzippedfiles:
            if os.path.split(fname)[1] == target:
                pluginfile = dir + '/' + fname

        if not pluginfile:
            drScrolledMessageDialog.ShowMessage(self.parent, 'Error Installing "' + label + '"', 'Install Error')
        else:
            #Do the Install
            pluginrfile = os.path.join(self.parent.pluginsdirectory, target)

            #Install Script
            plugininstallfile = pluginfile + ".install"
            continueinstallation = True
            if os.path.exists(plugininstallfile):
                f = open(plugininstallfile, 'r')
                scripttext = f.read()
                f.close()

                try:
                    code = compile((scripttext + '\n'), plugininstallfile, 'exec')
                except:
                    drScrolledMessageDialog.ShowMessage(self.parent, ("Error compiling install script."), "Error", wx.DefaultPosition, (550,300))
                    return
                try:
                    cwd = os.getcwd()
                    os.chdir(dir + '/' + os.path.commonprefix(unzippedfiles))
                    exec(code)
                    continueinstallation = Install(self.parent.ancestor)
                    os.chdir(cwd)
                except:
                    drScrolledMessageDialog.ShowMessage(self.parent, ("Error running install script."), "Error", wx.DefaultPosition, (550,300))
                    return
            #/Install Script
            if continueinstallation:
                try:
                    copyf = True
                    if os.path.exists(pluginrfile):
                        answer = wx.MessageBox('Overwrite"' + pluginrfile + '"?', "DrPython", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                        if answer == wx.NO:
                            copyf = False
                    if copyf:
                        shutil.copyfile(pluginfile, pluginrfile)
                        #there could be an error check: if idx file does not exist in source, simply create one.
                        shutil.copyfile(os.path.splitext(pluginfile)[0] + '.idx',
                                        os.path.splitext(pluginrfile)[0] + '.idx')
                        
                except:
                    drScrolledMessageDialog.ShowMessage(self.parent, ("Error with: " + pluginfile), "Install Error")
                    return

    def Run(self):
        l = len(self.parent.pluginstoinstall)
        if l < 1:
            self.stxtDone.SetForegroundColour(self.GetForegroundColour())
            return

        #Install
        self.stxtInstalling.SetForegroundColour(self.GetForegroundColour())

        self.gInstall.SetRange(l)

        x = 0
        while x < l:
            self.Install(self.parent.pluginstoinstall[x], self.parent.pluginlabels[x], self.parent.UnZippedFilesArray[x])
            x = x + 1
            self.gInstall.SetValue(x)

        self.stxtInstalling.SetForegroundColour(wx.Colour(175, 175, 175))

        #Index
        self.stxtIndexing.SetForegroundColour(self.GetForegroundColour())

        self.gIndex.SetRange(l)

        x = 0
        while x < l:
            self.Index(self.parent.pluginlabels[x], self.parent.UnZippedFilesArray[x], self.parent.pluginsinstallmethod[x])
            x = x + 1
            self.gIndex.SetValue(x)

        self.stxtIndexing.SetForegroundColour(wx.Colour(175, 175, 175))

        #Remove All Temporary Files.
        for label in self.parent.pluginlabels:
            dir = self.parent.tempdir + label
            try:
                self.RemoveTempDir(dir)
                if self.parent.Location:
                    #Remove the Downloaded File, if it exists.
                    downloadedfile = self.parent.tempdir + label + '.zip'
                    if os.path.exists(downloadedfile):
                        os.remove(downloadedfile)
            except:
                drScrolledMessageDialog.ShowMessage(self.parent, ("Error removing temporary directory for: " + label), "Post Install Error")
                return

        self.stxtDone.SetForegroundColour(self.GetForegroundColour())

class drPluginInstallWizard(wx.wizard.Wizard):
    def __init__(self, parent, title, bitmap):
        wx.wizard.Wizard.__init__(self, parent, wx.ID_ANY, title, bitmap)

        self.ancestor = parent

        self.pluginsdirectory = parent.pluginsdirectory

        self.wildcard = "DrPython Plugin Archive (*.zip)|*.zip"

        self.pluginstodownload = []

        self.pluginstoinstall = []

        self.pluginsinstallmethod = []

        self.pluginlabels = []

        self.UnZippedFilesArray = []

        self.Location = 0

        self.Mirror = ''

        try:
            #TempDir
            self.tempdir = os.path.split(tempfile.mktemp())[0].replace('\\', '/') + '/'
        except:
            drScrolledMessageDialog.ShowMessage(parent, "Error Getting Temporary Directory.", "Install Error")
            return

        self.LocationPage = drPluginInstallLocationPage(self)
        self.SelectPage = drPluginInstallSelectPage(self)
        self.DownloadPage = drPluginInstallDownloadPage(self)
        self.IndexPage = drPluginInstallIndexPage(self)
        self.InstallPage = drPluginInstallInstallPage(self)

        wx.wizard.WizardPageSimple_Chain(self.LocationPage, self.SelectPage)
        wx.wizard.WizardPageSimple_Chain(self.SelectPage, self.DownloadPage)
        wx.wizard.WizardPageSimple_Chain(self.DownloadPage, self.IndexPage)
        wx.wizard.WizardPageSimple_Chain(self.IndexPage, self.InstallPage)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged, self)

    def OnPageChanged(self, event):
        cp = self.GetCurrentPage()
        if cp == self.SelectPage:
            self.SelectPage.Run()
        elif cp == self.DownloadPage:
            self.DownloadPage.Run()
        elif cp == self.IndexPage:
            self.IndexPage.Run()
        elif cp == self.InstallPage:
            self.InstallPage.Run()

    def Run(self):
        self.RunWizard(self.LocationPage)

#*******************************************************************************
#UnInstall Wizard

class drPluginUnInstallSelectPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.parent = parent

        title = wx.StaticText(self, -1, "Select Plugins to UnInstall:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.btnAdd = wx.Button(self, wx.ID_ADD)
        self.btnRemove = wx.Button(self, wx.ID_REMOVE)

        self.lstPlugins = wx.ListBox(self, wx.ID_ANY, size=(300, 300))

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.bSizer.Add(self.btnAdd, 0, wx.SHAPED | wx.ALIGN_LEFT)
        self.bSizer.Add(self.btnRemove, 0, wx.SHAPED | wx.ALIGN_RIGHT)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.bSizer, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.lstPlugins, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.btnAdd)
        self.Bind(wx.EVT_BUTTON, self.OnRemove, self.btnRemove)

    def OnAdd(self, event):
        plist = os.listdir(self.parent.pluginsdirectory)

        PluginList = []

        for p in plist:
            i = p.find(".py")
            l = len(p)
            if i > -1 and (i + 3 == l):
                PluginList.append(p[:i])

        PluginList.sort()

        d = wx.lib.dialogs.MultipleChoiceDialog(self, "Select Plugins to Remove:", "Add Plugin(s) to List", PluginList)
        if d.ShowModal() == wx.ID_OK:
            selections = d.GetValueString()
            self.parent.pluginstoremove.extend(selections)
            self.lstPlugins.Set(self.parent.pluginstoremove)
        d.Destroy()

    def OnRemove(self, event):
        i = self.lstPlugins.GetSelection()
        if i < 0:
            return
        answer = wx.MessageBox('Remove "%s"?' % self.parent.pluginstoremove[i], "Remove Plugin From List", wx.YES_NO | wx.ICON_QUESTION)
        if answer == wx.YES:
            self.parent.pluginstoremove.pop(i)
            self.lstPlugins.Set(self.parent.pluginstoremove)

class drPluginUnInstallDataPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.parent = parent

        title = wx.StaticText(self, -1, "Remove Preferences and Shortcuts?:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.chklData = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, (200, 200), self.parent.pluginstoremove)

        self.theSizer = wx.FlexGridSizer(0, 1, 5, 5)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.EXPAND)
        self.theSizer.Add(self.chklData, 0, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_CHECKLISTBOX, self.OnData, self.chklData)

    def OnData(self, event):
        sel = event.GetSelection()
        if sel > -1:
            self.parent.removealldataforpluginArray[sel] = self.chklData.IsChecked(sel)

    def Run(self):
        if not self.parent.pluginstoremove:
            return
        self.chklData.Set(self.parent.pluginstoremove)

        self.parent.removealldataforpluginArray = map(lambda x: True, self.parent.pluginstoremove)

        x = 0
        l = len(self.parent.pluginstoremove)
        while x < l:
            self.chklData.Check(x, True)
            x = x + 1

class drPluginUnInstallUnInstallPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.parent = parent

        title = wx.StaticText(self, -1, "UnInstalling Selected Plugins:")
        title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.stxtUnInstalling = wx.StaticText(self, -1, "UnInstalling...")
        self.stxtUnIndexing = wx.StaticText(self, -1, "Removing From Index Files...")
        self.stxtDone = wx.StaticText(self, -1, "Done")

        self.stxtUnInstalling.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtUnIndexing.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtDone.SetForegroundColour(self.GetBackgroundColour())

        self.gUnInstall = wx.Gauge(self, -1, 0, size=(200, -1))
        self.gUnIndex = wx.Gauge(self, -1, 0, size=(200, -1))

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(title, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtUnInstalling, 0, wx.SHAPED)
        self.theSizer.Add(self.gUnInstall, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtUnIndexing, 0, wx.SHAPED)
        self.theSizer.Add(self.gUnIndex, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.theSizer.Add(self.stxtDone, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

    def RemoveDatFiles(self, plugin):
        pluginpreferencesfilebase = os.path.join(self.parent.pluginsdirectory , plugin)
        pluginshortcutsfilebase = os.path.join(self.parent.pluginsshortcutsdirectory, plugin)
        try:
            if os.path.exists(pluginpreferencesfilebase + '.preferences.dat'):
                os.remove(pluginpreferencesfilebase + '.preferences.dat')
            if os.path.exists(pluginshortcutsfilebase + '.shortcuts.dat'):
                os.remove(pluginshortcutsfilebase + '.shortcuts.dat')
        except:
            drScrolledMessageDialog.ShowMessage(self.parent, "Error Removing Plugin Preference Files", "Uninstall Error")

    def RemoveFromIndex(self, idx):
        idxfile = os.path.join(self.parent.pluginsdirectory , idx)

        f = open(idxfile, 'r')
        plugins = f.read().strip().split('\n')
        f.close()

        pluginstowrite = []
        for plugin in plugins:
            if not (plugin in self.parent.pluginstoremove):
                pluginstowrite.append(plugin)

        if not pluginstowrite:
            f = open(idxfile, 'w')
            for plugin in pluginstowrite:
                f.write(plugin + '\n')
            f.close()
        else:
            if idx != 'default.idx':
                os.remove(idxfile)

    def Run(self):
        #UnInstall Plugins
        self.stxtUnInstalling.SetForegroundColour(self.GetForegroundColour())

        self.gUnInstall.SetRange(len(self.parent.pluginstoremove))
        self.gUnInstall.SetValue(0)
        x = 0
        for plugin in self.parent.pluginstoremove:
            self.UnInstall(plugin)
            if self.parent.removealldataforpluginArray[x]:
                self.RemoveDatFiles(plugin)
            x = x + 1
            self.gUnInstall.SetValue(x)

        self.stxtUnInstalling.SetForegroundColour(self.GetForegroundColour())

        #Remove Plugins from any index files.
        self.stxtUnIndexing.SetForegroundColour(self.GetForegroundColour())

        plist = os.listdir(self.parent.pluginsdirectory)

        IndexList = []

        for p in plist:
            i = p.find(".idx")
            if i > -1:
                IndexList.append(p)

        self.gUnIndex.SetRange(len(IndexList))
        self.gUnIndex.SetValue(0)
        x = 0
        for idx in IndexList:
            try:
                self.RemoveFromIndex(idx)
            except:
                drScrolledMessageDialog.ShowMessage(self.parent, ('Error Removing Plugins From Index: "' + idx + '".'), "Uninstall Error")
            x = x + 1
            self.gUnIndex.SetValue(x)

        self.stxtUnIndexing.SetForegroundColour(wx.Colour(175, 175, 175))
        self.stxtDone.SetForegroundColour(self.GetForegroundColour())

    def UnInstall(self, plugin):
        pluginfile = os.path.join(self.parent.pluginsdirectory, plugin) + ".py"
        try:
            continueuninstall = True
            try:
                exec(compile("import " + plugin, plugin, 'exec'))
                exec(compile("continueuninstall = " + plugin + ".UnInstall(self.parent.ancestor)", plugin, 'exec'))
            except:
                pass
            if continueuninstall:
                os.remove(pluginfile)
                if os.path.exists(pluginfile + "c"):
                    os.remove(pluginfile + "c")
                if os.path.exists(pluginfile + ".bak"):
                    os.remove(pluginfile + ".bak")
        except:
            drScrolledMessageDialog.ShowMessage(self.parent, ("Error Removing Plugin File: " + pluginfile), "Uninstall Error")

class drPluginUnInstallWizard(wx.wizard.Wizard):
    def __init__(self, parent, title, bitmap):
        wx.wizard.Wizard.__init__(self, parent, wx.ID_ANY, title, bitmap)

        self.ancestor = parent

        self.pluginstoremove = []
        self.removealldataforpluginArray = []

        self.SelectPage = drPluginUnInstallSelectPage(self)
        self.DataPage = drPluginUnInstallDataPage(self)
        self.UnInstallPage = drPluginUnInstallUnInstallPage(self)

        wx.wizard.WizardPageSimple_Chain(self.SelectPage, self.DataPage)
        wx.wizard.WizardPageSimple_Chain(self.DataPage, self.UnInstallPage)

        self.Location = 0
        self.Mirror = ''

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged, self)

    def OnPageChanged(self, event):
        cp = self.GetCurrentPage()
        if cp == self.DataPage:
            self.DataPage.Run()
        elif cp == self.UnInstallPage:
            self.UnInstallPage.Run()

    def Run(self):
        self.RunWizard(self.SelectPage)

#*******************************************************************************
#Edit Indexes Dialog

class drEditIndexDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Edit Indexes", wx.DefaultPosition, (-1, -1), wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)

        wx.Yield()  # TODO: Why!?

        plist = os.listdir(parent.pluginsdirectory)

        self.PluginList = []

        self.IndexList = []

        self.indexname = ""
        self.indexplugins = []

        for p in plist:
            i = p.find(".py")
            l = len(p)
            if i > -1 and (i + 3 == l):
                self.PluginList.append(p[:i])

        pidxlist = os.listdir(parent.pluginsdirectory)
        for p in pidxlist:
            i = p.find(".idx")
            if i > -1:
                self.IndexList.append(p)
        ##AB:
        #if len(self.IndexList)==0:
            #self.IndexList.append('default.idx')

        ##FS: 25.03.2007: added again
        self.IndexList.append('default.idx')
            
        self.PluginList.sort()
        self.IndexList.sort()

        self.boxNotInIndex = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, (200, 200), self.PluginList)

        self.boxInIndex = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, (200, 200))

        self.btnAdd = wx.Button(self, wx.ID_ADD)
        self.btnRemove = wx.Button(self, wx.ID_REMOVE)

        self.btnUp = wx.Button(self, wx.ID_UP)
        self.btnDown = wx.Button(self, wx.ID_DOWN)

        self.cboIndex = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, (250, -1), self.IndexList)

        self.cboIndex.SetStringSelection('default.idx')

        self.btnClose = wx.Button(self, wx.ID_CANCEL, "&Close Dialog")
        self.btnDelete = wx.Button(self, wx.ID_DELETE)
        self.btnNew = wx.Button(self, wx.ID_NEW)
        self.btnSave = wx.Button(self, wx.ID_SAVE)
        self.btnSaveAs = wx.Button(self, wx.ID_SAVEAS)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)
        self.indexSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topmenuSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer = wx.FlexGridSizer(0, 4, 5, 10)
        self.menubuttonSizer = wx.BoxSizer(wx.VERTICAL)

        self.indexSizer.Add(wx.StaticText(self, -1, "   Current Index:   "), 0, wx.SHAPED)
        self.indexSizer.Add(self.cboIndex, 0, wx.SHAPED)
        self.indexSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.indexSizer.Add(self.btnClose, 0, wx.SHAPED)

        self.topmenuSizer.Add(self.btnDelete, 1, wx.SHAPED)
        self.topmenuSizer.Add(self.btnNew, 1, wx.SHAPED)
        self.topmenuSizer.Add(self.btnSave, 1, wx.SHAPED)
        self.topmenuSizer.Add(self.btnSaveAs, 1, wx.SHAPED)

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

        self.mainSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, "Not In Index:"), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, "Plugins In Index:"), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.mainSizer.Add(self.boxNotInIndex, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.mainSizer.Add(self.menubuttonSizer, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.mainSizer.Add(self.boxInIndex, 0,  wx.SHAPED | wx.ALIGN_CENTER)

        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.SHAPED)
        self.theSizer.Add(self.indexSizer, 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.topmenuSizer, 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.mainSizer, 9, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 1, wx.SHAPED)

        self.parent = parent

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnbtnUp, self.btnUp)
        self.Bind(wx.EVT_BUTTON, self.OnbtnDown, self.btnDown)

        self.Bind(wx.EVT_BUTTON, self.OnbtnAdd, self.btnAdd)
        self.Bind(wx.EVT_BUTTON, self.OnbtnRemove, self.btnRemove)
        self.Bind(wx.EVT_BUTTON, self.OnbtnSave, self.btnSave)
        self.Bind(wx.EVT_BUTTON, self.OnbtnDelete, self.btnDelete)
        self.Bind(wx.EVT_BUTTON, self.OnbtnSaveAs, self.btnSaveAs)
        self.Bind(wx.EVT_BUTTON, self.OnbtnNew, self.btnNew)

        self.Bind(wx.EVT_CHOICE, self.OnOpen, self.cboIndex)

        self.parent.LoadDialogSizeAndPosition(self, 'editindexdialog.sizeandposition.dat')

        self.OnOpen(None)

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, 'plugindialog.sizeandposition.dat')
        if event is not None:
            event.Skip()

    def OnbtnAdd(self, event):
        tselection = self.boxNotInIndex.GetStringSelection()
        try:
            self.indexplugins.index(tselection)
            drScrolledMessageDialog.ShowMessage(self, 'Plugin "' + tselection + '" has already been added.', "Already Added")
        except:
            tsel = self.boxNotInIndex.GetSelection()
            if tsel == -1:
                drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Add", "Mistake")
                return
            sel = self.boxInIndex.GetSelection()
            if sel == -1:
                sel = 0
            self.boxInIndex.Append(tselection)
            self.boxInIndex.SetSelection(sel)
            self.indexplugins.append(tselection)
            self.SetNotInIndex()

    def OnbtnDelete(self, event):
        indexname = self.cboIndex.GetStringSelection()
        if indexname == 'default.idx':
            drScrolledMessageDialog.ShowMessage(self, 'You Cannot Delete the Default Index', 'Error')
            return
        answer = wx.MessageBox('Delete "%s"?' % (indexname), "DrPython", wx.YES_NO | wx.ICON_QUESTION)
        if answer == wx.YES:
            indexfile = os.path.join(self.parent.pluginsbasepreferencesdir, indexname)
            if not os.path.exists(indexfile):
                drScrolledMessageDialog.ShowMessage(self, '"%s" does not exist.' % (indexfile), 'Error')
                return
            try:
                os.remove(indexfile)
            except:
                drScrolledMessageDialog.ShowMessage(self, 'Error Removing "%s".' % (indexfile), 'Error')
            if indexname in self.IndexList:
                i = self.IndexList.index(indexname)
                self.IndexList.pop(i)
                self.cboIndex.Delete(i)
            self.cboIndex.SetStringSelection('default.idx')
            self.OnOpen(None)
            if self.parent.prefs.enablefeedback:
                drScrolledMessageDialog.ShowMessage(self, 'Successfully Removed "%s".' % (indexfile), 'Deleted Index')

    def OnbtnDown(self, event):
        sel = self.boxInIndex.GetSelection()
        if sel < self.boxInIndex.GetCount() - 1 and sel > -1:
            txt = self.boxInIndex.GetString(sel)
            self.boxInIndex.Delete(sel)
            self.boxInIndex.InsertItems([txt], sel+1)
            self.boxInIndex.SetSelection(sel+1)
            #franz:swap elements
            self.indexplugins.insert(sel+1, self.indexplugins.pop(sel))

    def OnbtnNew(self, event):
        d = wx.TextEntryDialog(self, "Enter New Index Name (No .idx):", "New Index", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            indexname = v + '.idx'
            indexfile = os.path.join(self.parent.pluginsbasepreferencesdir , indexname)
            self.IndexList.append(indexname)
            self.cboIndex.Append(indexname)
            self.cboIndex.SetStringSelection(indexname)
            try:
                f = open(indexfile, 'wb')
                f.write('\n')
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(self, 'Error Creating "%s".' % (indexfile), 'Error')
                return

            self.OnOpen(None)

    def OnbtnRemove(self, event):
        sel = self.boxInIndex.GetSelection()
        if sel == -1:
            drScrolledMessageDialog.ShowMessage(self, "Nothing Selected to Remove", "Mistake")
            return

        self.indexplugins.pop(sel)
        self.boxInIndex.Delete(sel)
        self.boxInIndex.SetSelection(sel-1)
        self.SetNotInIndex()

    def OnbtnSave(self, event):
        f = open(self.indexname, 'w')
        for plugin in self.indexplugins:
            f.write(plugin + "\n")
        f.close()
        if self.parent.prefs.enablefeedback:
            drScrolledMessageDialog.ShowMessage(self, ("Succesfully wrote to:\n"  + self.indexname), "Saved Changes to Index File")

    def OnbtnSaveAs(self, event):
        idx = self.cboIndex.GetStringSelection()
        d = wx.TextEntryDialog(self, 'Save "%s" As(No .idx):' % (idx), "Save Index As", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            indexname = v + '.idx'
            indexfile = os.path.join(self.parent.pluginsbasepreferencesdir , indexname)
            self.IndexList.append(indexname)
            self.cboIndex.Append(indexname)
            self.cboIndex.SetStringSelection(indexname)
            try:
                f = open(indexfile, 'wb')
                for plugin in self.indexplugins:
                    f.write(plugin + "\n")
                f.close()
                if self.parent.prefs.enablefeedback:
                    drScrolledMessageDialog.ShowMessage(self, ("Succesfully wrote to:\n"  + indexfile), "Saved Changes to Index File")
            except:
                drScrolledMessageDialog.ShowMessage(self, 'Error Saving "%s" As "%s".' % (idx, indexname), 'Error')
                return

    def OnbtnUp(self, event):
        sel = self.boxInIndex.GetSelection()
        if sel > 0:
            txt = self.boxInIndex.GetString(sel)
            self.boxInIndex.Delete(sel)
            self.boxInIndex.InsertItems([txt], sel-1)
            self.boxInIndex.SetSelection(sel-1)
            #franz:swap elements
            self.indexplugins.insert(sel-1, self.indexplugins.pop(sel))

    def OnOpen(self, event):
        fname = self.cboIndex.GetStringSelection()
        self.indexname = os.path.join(self.parent.preferencesdirectory, fname)
        if not os.path.exists(self.indexname):
            return
        try:
            f = open(self.indexname, 'r')
            self.indexplugins = f.read().rstrip().split('\n')
            f.close()

            x = 0
            l = len(self.indexplugins)
            while x < l:
                if not self.indexplugins[x]:
                    self.indexplugins.pop(x)
                    x = x - 1
                    l = l - 1
                x = x + 1

            self.boxInIndex.Set(self.indexplugins)
            self.SetNotInIndex()
        except:
            drScrolledMessageDialog.ShowMessage(self.parent, ("Error Reading Index File: " + self.indexname), "Open Error")

    def SetNotInIndex (self):
        #Written By Franz
        #AB: Modified to keep old selection
        sel = self.boxNotInIndex.GetSelection()
        nlist = []
        for i in self.PluginList:
            if i not in self.indexplugins:
                nlist.append (i)
        self.boxNotInIndex.Set (nlist)
        if sel<0:
            sel=0
        if sel>=len(nlist):
            sel=len(nlist)-1
        self.boxNotInIndex.SetSelection(sel)
