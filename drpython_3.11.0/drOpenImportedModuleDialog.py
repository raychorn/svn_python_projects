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

#Open Imported Module Dialog

import os, sys, keyword
import wx
from drSingleChoiceDialog import drSingleChoiceDialog

#*******************************************************************************************************
#Utility Functions for parsing import strings,
#and getting the path for each module.

def GetModulePath(filepath, selmodule, platformiswin):
    moduletext = selmodule
    #Special Cases:
    if selmodule == 'os.path':
        if platformiswin:
            selmodule = 'ntpath'
        elif os.name == 'mac':
            selmodule = 'macpath'
        else:
            selmodule = 'posixpath'

    selectedmodule = '/' + selmodule.replace('.', '/') + '.py'
    #Handle cases like 'import wx' == import 'wx.__init__'
    selectedinitmodule = '/' + selmodule.replace('.', '/') + '/__init__.py'

    if os.path.exists(filepath + selectedmodule):
        return moduletext, (filepath + selectedmodule)
    if os.path.exists(filepath + selectedinitmodule):
        return moduletext, (filepath + selectedinitmodule)

    #Search for the file:
    for somepath in sys.path:
        modulefile = somepath.replace('\\', '/') + selectedmodule
        initfile = somepath.replace('\\', '/') + selectedinitmodule
        if os.path.exists(modulefile):
            return moduletext, modulefile
        elif os.path.exists(initfile):
            return moduletext, initfile

    return moduletext, None

def ParseImportStatement(matches):
    targetarray = map(lambda x: x.strip().split(), matches)
    results = []
    for item in targetarray:
        x = 0
        isfrom = (item[0] == 'from')
        l = len(item)
        while x < l:
            if item[x].find(',') > -1:
                y = item.pop(x)
                ya = y.split(',')
                ly = len(ya)
                counter = 0
                while counter < ly:
                    if not ya[counter]:
                        ya.pop(counter)
                        ly -= 1
                    else:
                        counter += 1
                item.extend(ya)
                l = l + len(ya) - 1
            elif item[x] == 'as':
                item.pop(x)
                try:
                    item.pop(x)
                    l -= 2
                except:
                    l -= 1
            elif item[x] == '*':
                item.pop(x)
                l -= 1
            elif item[x] in keyword.kwlist:
                item.pop(x)
                l -= 1
            else:
                if (x > 0) and isfrom:
                    a = item.pop(x)
                    item.insert(x, item[0] + '.' + a)
                x += 1
        results.append(item)
    return results


#*******************************************************************************************************

class drOpenImportedModuleDialog(drSingleChoiceDialog):
    def __init__(self, parent, modulelist, point=wx.DefaultPosition, size=(250, 300)):
        drSingleChoiceDialog.__init__(self, parent, "Open Imported Module", modulelist, point, size)

        #Why is this needed?  Who knows.  But it is.
        self.Move(point)

        self.Bind(wx.EVT_CLOSE, self.OnCloseW)

        self.parent.LoadDialogSizeAndPosition(self, 'openimportedmoduledialog.sizeandposition.dat')

    def GetSelectedModule(self):
        return self.GetStringSelection()

    def OnbtnCancel(self, event):
        self.OnCloseW(None)
        drSingleChoiceDialog.OnbtnCancel(self, event)

    def OnbtnOk(self, event):
        self.OnCloseW(None)
        drSingleChoiceDialog.OnbtnOk(self, event)

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, 'openimportedmoduledialog.sizeandposition.dat')
        if event is not None:
            event.Skip()
