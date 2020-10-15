#!/usr/bin/env python

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
#
#   Requirements(Dependencies):  Install Python, and wxPython.
#
#   Tested On Windows, Linux, Mac OS X
#
#   Icons taken from "Klassic New Crisp Icons" by Asif Ali Rizwaan (therizwaan) from the KDE-LOOK site (some edited a bit).
#   A humble and excellent artist.
#   Oh, the python icon is taken from wxPython.
#   The basic design of the program is meant to roughly (ROUGHLY) mimick DrScheme.
#   The purpose is the same, to provide a simple IDE(integrated development environment) ideal for teaching.
#   The DrPython icon itself was based on the DrScheme icon, with a slightly edited wxpython icon inserted(note yellow tongue, googly eyes).
#
#   This program could not have been written without the wonderful work of the people behind
#   python and wxPython, in particular the Styled Text Control.  Thank you.  Hopefully this tool will be of use.

#This is a module for a gui for importing / exporting preferences.

import wx
import drZip
import drFileDialog

class drSetupPreferencesDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'Setup Preferences', style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.parent = parent

        self.drframe = parent.drframe

        self.ID_EXPORT_ALL = 501
        self.ID_IMPORT_ALL = 502

        self.ID_EXPORT_PREFS = 503
        self.ID_IMPORT_PREFS = 504

        self.ID_EXPORT_PLUGINS = 505
        self.ID_IMPORT_PLUGINS = 506

        self.ID_EXPORT_DRSCRIPTS = 507
        self.ID_IMPORT_DRSCRIPTS = 518

        self.btnExportAll = wx.Button(self, self.ID_EXPORT_ALL, 'Export Preferences, Plugins, DrScripts To Zip')
        self.btnImportAll = wx.Button(self, self.ID_IMPORT_ALL, 'Import Preferences, Plugins, DrScripts From Zip')
        self.btnExportPrefs = wx.Button(self, self.ID_EXPORT_PREFS, 'Export Preferences To Zip')
        self.btnImportPrefs = wx.Button(self, self.ID_IMPORT_PREFS, 'Import Preferences From Zip')
        self.btnExportPlugins = wx.Button(self, self.ID_EXPORT_PLUGINS, 'Export Plugins To Zip')
        self.btnImportPlugins = wx.Button(self, self.ID_IMPORT_PLUGINS, 'Import Plugins From Zip')
        self.btnExportDrScripts = wx.Button(self, self.ID_EXPORT_DRSCRIPTS, 'Export DrScripts To Zip')
        self.btnImportDrScripts = wx.Button(self, self.ID_IMPORT_DRSCRIPTS, 'Import DrScripts From Zip')

        self.btnExit = wx.Button(self, wx.ID_CANCEL, 'Exit')

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)
        self.theSizer.Add(self.btnExportAll, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnImportAll, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)
        self.theSizer.Add(self.btnExportPrefs, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnImportPrefs, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)
        self.theSizer.Add(self.btnExportPlugins, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnImportPlugins, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)
        self.theSizer.Add(self.btnExportDrScripts, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(self.btnImportDrScripts, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)
        self.theSizer.Add(self.btnExit, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnExportAll, id=self.ID_EXPORT_ALL)
        self.Bind(wx.EVT_BUTTON, self.OnImportAll, id=self.ID_IMPORT_ALL)
        self.Bind(wx.EVT_BUTTON, self.OnExportPrefs, id=self.ID_EXPORT_PREFS)
        self.Bind(wx.EVT_BUTTON, self.OnImportPrefs, id=self.ID_IMPORT_PREFS)
        self.Bind(wx.EVT_BUTTON, self.OnExportPlugins, id=self.ID_EXPORT_PLUGINS)
        self.Bind(wx.EVT_BUTTON, self.OnImportPlugins, id=self.ID_IMPORT_PLUGINS)
        self.Bind(wx.EVT_BUTTON, self.OnExportDrScripts, id=self.ID_EXPORT_DRSCRIPTS)
        self.Bind(wx.EVT_BUTTON, self.OnImportDrScripts, id=self.ID_IMPORT_DRSCRIPTS)

    def OnExportAll(self, event):
        dlg = drFileDialog.FileDialog(self.drframe, "Export Preferences, Plugins, and DrScripts To", 'Zip File (*.zip)|*.zip', IsASaveDialog=True)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath().replace("\\", "/")
            drZip.ExportPreferencesTo(self.drframe.pluginsdirectory, self.drframe.preferencesdirectory,
                                      self.drframe.datdirectory, filename)

        dlg.Destroy()

    def OnExportDrScripts(self, event):
        dlg = drFileDialog.FileDialog(self.drframe, "Export DrScripts To", 'Zip File (*.zip)|*.zip', IsASaveDialog=True)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath().replace("\\", "/")
            drZip.ExportDrScriptsTo(self.drframe.preferencesdirectory, filename)

        dlg.Destroy()

    def OnExportPlugins(self, event):
        dlg = drFileDialog.FileDialog(self.drframe, "Export Plugins To", 'Zip File (*.zip)|*.zip', IsASaveDialog=True)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath().replace("\\", "/")
            drZip.ExportDirectoryTo(self.drframe.pluginsdirectory, filename, 'plugins')

        dlg.Destroy()

    def OnExportPrefs(self, event):
        dlg = drFileDialog.FileDialog(self.drframe, "Export Preferences To", 'Zip File (*.zip)|*.zip', IsASaveDialog=True)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath().replace("\\", "/")
            drZip.ExportPreferencesTo(self.drframe.pluginsdirectory, self.drframe.preferencesdirectory,
                                      self.drframe.datdirectory, filename, plugins=False, drscripts=False)

        dlg.Destroy()

    def OnImportAll(self, event):
        if self.drframe.Ask('This will permanently overwrite all of your preferences, plugins, and drscript file.\n\nProceed?', 'Warning'):
            dlg = drFileDialog.FileDialog(self.drframe, "Import Preferences, Plugins, and DrScripts From", 'Zip File (*.zip)|*.zip')

            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath().replace("\\", "/")
                drZip.ImportPreferencesFrom(self.drframe.preferencesdirectory, filename)
                self.drframe.ShowMessage('Successfully imported preferences, plugins, and drscripts.', 'Import Success')

            dlg.Destroy()

    def OnImportDrScripts(self, event):
        if self.drframe.Ask('This will permanently overwrite all of your drscript file.\n\nProceed?', 'Warning'):
            dlg = drFileDialog.FileDialog(self.drframe, "Import DrScripts From", 'Zip File (*.zip)|*.zip')

            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath().replace("\\", "/")
                drZip.ImportDrScriptsFrom(self.drframe.preferencesdirectory, filename)
                self.drframe.ShowMessage('Successfully imported drscripts.', 'Import Success')

            dlg.Destroy()

    def OnImportPlugins(self, event):
        if self.drframe.Ask('This will permanently overwrite all of your plugins.\n\nProceed?', 'Warning'):
            dlg = drFileDialog.FileDialog(self.drframe, "Import Plugins From", 'Zip File (*.zip)|*.zip')

            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath().replace("\\", "/")
                drZip.ImportPluginsFrom(self.drframe.preferencesdirectory, filename)
                self.drframe.ShowMessage('Successfully imported plugins.', 'Import Success')

            dlg.Destroy()

    def OnImportPrefs(self, event):
        if self.drframe.Ask('This will permanently overwrite all of your preferences.\n\nProceed?', 'Warning'):
            dlg = drFileDialog.FileDialog(self.drframe, "Import Preferences From", 'Zip File (*.zip)|*.zip')

            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath().replace("\\", "/")
                drZip.ImportJustPreferencesFrom(self.drframe.preferencesdirectory, filename)
                self.drframe.ShowMessage('Successfully imported preferences.', 'Import Success')

            dlg.Destroy()