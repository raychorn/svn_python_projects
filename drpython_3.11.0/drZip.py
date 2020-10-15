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

#This is a module to make adding
#to / from zip files really easy.

#Targets are prefs directory,
#creating a directory structure from the drscript menu
#an all plugins.

import os, zipfile, string, tempfile
from drPrefsFile import ExtractPreferenceFromText

def AddDirectoryToZipFile(directory, dirname, zip):
    dlist = os.listdir(directory)

    for item in dlist:
        absitem = os.path.join(directory, item)
        zipitem = os.path.join(dirname, item)
        if os.path.isdir(absitem):
            AddDirectoryToZipFile(absitem, zipitem, zip)
        else:
            zip.write(absitem, zipitem)

def AddDrScriptsToZipFile(prefdir, zip):
    scriptfile = prefdir + "/drscript.dat"

    if os.path.exists(scriptfile):
        newlines = []

        dirstrings = ['drscripts']
        lastCount = 0
        #Read from the file
        f = open(scriptfile, 'rb')
        #Initialize
        line = f.readline()
        while line:
            c = line.count('\t')
            indentationstring = line[:c]
            line = line[c:].rstrip()
            while lastCount > c:
                dirstrings.pop()
                lastCount = lastCount - 1

            if line[0] == '>':
                dirstrings.append(line[1:])
                newlines.append(indentationstring + line)
                c = c + 1
            else:
                line_path = ExtractPreferenceFromText(line, "path")
                line_title = ExtractPreferenceFromText(line, "title")

                line_filename = os.path.basename(line_path)

                if os.path.exists(line_path):
                    zippath = string.join(dirstrings, '/')
                    zipname = os.path.join(zippath, line_filename)
                    zip.write(line_path, zipname)
                    newlines.append(indentationstring + '<path>' + zipname + '</path><title>' + line_title + '</title>')

            lastCount = c
            line = f.readline()
        f.close()


        #Add the edited Script File:
        newtext = string.join(newlines, '\n')

        tdrscript = tempfile.mktemp()

        f = file(tdrscript, 'wb')
        f.write(newtext)
        f.close()

        zip.write(tdrscript, 'drscript.dat')

        #Remove the temporary file:
        os.remove(tdrscript)

        #Add Shortcuts
        zip.write(prefdir + "/drscript.shortcuts.dat", 'drscript.shortcuts.dat')


def CreateDirectories(targetdir, zippedfilename):
    zippedfilename = zippedfilename.replace('\\', '/')
    d = zippedfilename.find('/')
    while d > -1:
        dir = zippedfilename[:d]
        targetdir = targetdir + '/' + dir
        if not os.path.exists(targetdir):
            os.mkdir(targetdir)
        zippedfilename = zippedfilename[d+1:]
        d = zippedfilename.find('/')

def ExportDirectoryTo(targetdirectory, filename, ziproot = ''):
    zf = zipfile.ZipFile(filename, 'w')

    AddDirectoryToZipFile(targetdirectory, ziproot, zf)

    zf.close()

def ExportDrScriptsTo(prefdir, filename):
    zf = zipfile.ZipFile(filename, 'w')

    AddDrScriptsToZipFile(prefdir, zf)

    zf.close()

def ExportPreferencesTo(pluginsdirectory, prefdir, shortcutsdir, datdirectory, filename,
                        shortcuts = True, popupmenu = True, toolbar = True, plugins = True, drscripts = True):
    zf = zipfile.ZipFile(filename, 'w')

    #Add Plugins
    if plugins:
        AddDirectoryToZipFile(pluginsdirectory, '', zf)

    if drscripts:
        AddDrScriptsToZipFile(prefdir, zf)

    #Add Preferences
    zf.write(prefdir + "/preferences.dat", 'preferences.dat')

    #Add Shortcuts
    if shortcuts:
        zf.write(shortcutsdir + "/shortcuts.dat", 'shortcuts.dat')
        zf.write(shortcutsdir + "/stcshortcuts.dat", 'stcshortcuts.dat')

    #Add Pop Up Menu
    if popupmenu:
        zf.write(datdirectory +  "/popupmenu.dat", 'popupmenu.dat')

    #Add ToolBar
    if toolbar:
        zf.write(datdirectory + "/toolbar.dat", 'toolbar.dat')

    zf.close()



def ImportDrScriptsFrom(prefdir, filename):
    UnPackIf(prefdir, filename, 'drscript')
    SetupImportedDrScripts(prefdir)

def ImportPluginsFrom(prefdir, filename):
    UnPackIf(prefdir, filename, 'plugins')

def ImportPreferencesFrom(prefdir, filename):
    UnPack(prefdir, filename)
    SetupImportedDrScripts(prefdir)

def ImportJustPreferencesFrom(prefdir, filename):
    UnPackJustPreferences(prefdir, filename)
    SetupImportedDrScripts(prefdir)

def SetupImportedDrScripts(prefdir):
    scriptfile = prefdir + "/drscript.dat"

    if os.path.exists(scriptfile):

        #Read from the file
        f = open(scriptfile, 'rb')
        lines = f.readlines()
        f.close()

        newlines = []

        for line in lines:
            c = line.count('\t')
            identationstring =  line[:c]

            if line[0] != '>':

                line_path = ExtractPreferenceFromText(line, "path")
                line_title = ExtractPreferenceFromText(line, "title")

                new_path = os.path.join(prefdir, line_path)

                if os.path.exists(new_path):
                    newlines.append(identationstring + '<path>' + new_path + '</path><title>' + line_title + '</title>\n')
            else:
                newlines.append(identationstring + line)

        f = open(scriptfile, 'wb')
        f.writelines(newlines)
        f.close()

def UnPack(targetdirectory, filename, label=''):
    zf = zipfile.ZipFile(filename, 'r')

    dir = targetdirectory + label

    if not os.path.exists(dir):
        os.mkdir(dir)

    zippedfiles = zf.namelist()

    for zippedfile in zippedfiles:
        l = len(zippedfile)
        if (zippedfile[l-1] == '/') or (zippedfile[l-1] == '\\'):
            CreateDirectories(dir, zippedfile)
        else:
            CreateDirectories(dir, zippedfile)
            data = zf.read(zippedfile)
            f = file(dir + '/' + zippedfile, 'wb')
            f.write(data)
            f.close()

    zf.close()

def UnPackIf(targetdirectory, filename, prefix, label=''):
    zf = zipfile.ZipFile(filename, 'r')

    dir = targetdirectory + label

    if not os.path.exists(dir):
        os.mkdir(dir)

    zippedfiles = zf.namelist()

    for zippedfile in zippedfiles:
        if zippedfile.find(prefix) == 0:
            l = len(zippedfile)
            if (zippedfile[l-1] == '/') or (zippedfile[l-1] == '\\'):
                CreateDirectories(dir, zippedfile)
            else:
                CreateDirectories(dir, zippedfile)
                data = zf.read(zippedfile)
                f = file(dir + '/' + zippedfile, 'wb')
                f.write(data)
                f.close()

    zf.close()

def UnPackJustPreferences(targetdirectory, filename, label=''):
    zf = zipfile.ZipFile(filename, 'r')

    dir = targetdirectory + label

    if not os.path.exists(dir):
        os.mkdir(dir)

    rawzippedfiles = zf.namelist()

    zippedfiles = []

    targets = ['preferences.dat', 'popupmenu.dat', 'shortcuts.dat', 'stcshortcuts.dat', 'toolbar.dat']

    for rz in rawzippedfiles:
        if rz in targets:
            zippedfiles.append(rz)

    for zippedfile in zippedfiles:
        l = len(zippedfile)
        if (zippedfile[l-1] == '/') or (zippedfile[l-1] == '\\'):
            CreateDirectories(dir, zippedfile)
        else:
            CreateDirectories(dir, zippedfile)
            data = zf.read(zippedfile)
            f = file(dir + '/' + zippedfile, 'wb')
            f.write(data)
            f.close()

    zf.close()
