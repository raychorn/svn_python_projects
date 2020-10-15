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

#File Dialog

import os, re, stat, time, sys, locale
import wx
import drScrolledMessageDialog
import lnkDecoderRing
import drEncoding

class FileListCtrl(wx.ListView):
    def __init__(self, parent, id, fsize, fstyle):
        wx.ListView.__init__(self, parent, id, size=fsize, style=fstyle)

        bDir = parent.parent.bitmapdirectory + '/16/'

        self.parent = parent

        self.grandparent = parent.parent

        self.IsDetailed = False

        self.pywfilter = re.compile('.*\.pyw$')
        self.pyfilter = re.compile('.*\.py$')

        self.imagelist = wx.ImageList(16, 16)
        self.images = [wx.BitmapFromImage(wx.Image(bDir+'folder.png', wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(bDir+'py.png', wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(bDir+'pyw.png', wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(bDir+'unknown.png', wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(bDir+'up.png', wx.BITMAP_TYPE_PNG)), \
        wx.BitmapFromImage(wx.Image(bDir+'down.png', wx.BITMAP_TYPE_PNG))]

        map(self.imagelist.Add, self.images)

        self.AssignImageList(self.imagelist, wx.IMAGE_LIST_SMALL)

        self.directories = ['']
        self.dirposition = -1

        self.ShowHiddenFiles = False

        self.DataArray = []
        self.currentcolumn = 0
        self.direction = [0, -1, -1, -1, -1]

        self.timeformat = '%m/%d/%Y %H:%M:%S'

        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumnClick)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def GetDirectory(self):
        try:
            return self.directories[self.dirposition]
        except:
            return self.directories[0]

    def GoBack(self, filter):
        self.dirposition = self.dirposition - 1
        if self.dirposition < 0:
            self.dirposition = 0
        self.SetDirectoryTo(self.directories[self.dirposition], filter, False)

    def GoForward(self, filter):
        self.dirposition = self.dirposition + 1
        if self.dirposition >= len(self.directories):
            self.dirposition = len(self.directories) - 1
        self.SetDirectoryTo(self.directories[self.dirposition], filter, False)

    def IsDirectory(self, index):
        return self.DataArray[index][2] == '<Dir>'

    def OnColumnClick(self, event):
        oldcol = self.currentcolumn
        self.currentcolumn = event.GetColumn()
        self.ClearColumnImage(oldcol)
        if oldcol != self.currentcolumn:
            self.direction[oldcol] = -1
        if self.direction[self.currentcolumn] == -1:
            self.direction[self.currentcolumn] = 1
            self.SetColumnImage(self.currentcolumn, 5)
        else:
            self.direction[self.currentcolumn] = not self.direction[self.currentcolumn]
            if self.direction[self.currentcolumn]:
                self.SetColumnImage(self.currentcolumn, 5)
            else:
                self.SetColumnImage(self.currentcolumn, 4)
        self.SortItems(self.SortData)

    def OnSize(self, event):
        if self.IsDetailed:
            width = self.GetSizeTuple()[0]
            self.SetColumnWidth(0, int(width * .4))
            self.SetColumnWidth(1, int(width * .15))
            self.SetColumnWidth(2, int(width * .15))
            self.SetColumnWidth(3, int(width * .15))
            self.SetColumnWidth(4, int(width * .15))
        if event is not None:
            event.Skip()

    def SetDirectoryTo(self, directory, filter="*", updatedirectories=True):
        self.parent.cboFile.SetValue('')
        self.parent.cboFile.Clear()
        directory = os.path.normpath(directory).replace('\\', '/').replace('//', '/')
        if not os.path.exists(directory):
            return
        self.parent.txtDirectory.SetValue(directory)

        try:
            if wx.USE_UNICODE:
                uthelist = os.listdir(directory)
                thelist = []
                if self.grandparent.prefs.defaultencoding:
                    for u in uthelist:
                        try:
                            thelist.append(u)
                        except:
                            wx.MessageBox ("Cannot show files:\nPlease check in Options=>Preferences=>General=>Default Encoding!", "Error Decoding Directory Entry:  Not Ascii.", wx.ICON_INFORMATION, self)
                            return
                else:
                    for u in uthelist:
                        if not drEncoding.CheckAscii(u):
                            wx.MessageBox ("Cannot show files:\nNo Encoding is set up.\nPlease check in Options=>Preferences=>General=>Default Encoding!", "Error Decoding Directory Entry:  Not Ascii.", wx.ICON_INFORMATION, self)
                            return
                        else:
                            thelist.append(u)
            else:
                thelist = os.listdir(directory)

            if updatedirectories:
                self.directories = self.directories[:self.dirposition+1]
                self.directories.append(directory)
                self.dirposition = self.dirposition + 1
            dirs = []
            l = len(thelist)
            x = 0
            while x < l:
                if os.path.isdir(directory + '/' + thelist[x]):
                    dirs.append(thelist.pop(x))
                    x = x - 1
                    l = l - 1
                x = x + 1

            self.DeleteAllItems()
            #franz, 15.03.2005:
            thelist.sort(lambda x,y: cmp(x.lower(), y.lower()))
            dirs.sort(lambda x,y: cmp(x.lower(), y.lower()))

            filter = filter + ";" + self.parent.parent.prefs.constantwildcard

            filter = filter.replace('.', '\.').replace('*', '.*').replace(';', '$|') + '$'
            refilter = re.compile(filter)

            dirs.insert(0, '..')

            for item in dirs:
                additem = True
                if not self.ShowHiddenFiles:
                    if item[0] == '.':
                        if item != '..':
                            additem = False
                if additem:
                    i = self.GetItemCount()
                    self.InsertStringItem(i, item)
                    self.SetItemImage(i, 0, 0)
                    if self.IsDetailed:
                        self.SetItemData(i, i)
                        st = os.stat(directory + '/' + item)

                        mtime = time.strftime(self.timeformat ,time.localtime(st.st_mtime))
                        mmode = str(oct(stat.S_IMODE(st.st_mode)))

                        self.DataArray.append((item, '', '<Dir>', mtime, mmode))

                        self.SetStringItem(i, 1, '')
                        self.SetStringItem(i, 2, '<Dir>')
                        self.SetStringItem(i, 3, mtime)
                        self.SetStringItem(i, 4, mmode)
            for item in thelist:
                additem = True
                if not self.ShowHiddenFiles:
                    if item[0] == '.':
                        additem = False
                if additem:
                    if refilter.match(item):
                        self.parent.cboFile.Append(item)
                        i = self.GetItemCount()
                        self.InsertStringItem(i, item)
                        if self.pywfilter.match(item):
                            self.SetItemImage(i, 2, 2)
                        elif self.pyfilter.match(item):
                            self.SetItemImage(i, 1, 1)
                        else:
                            self.SetItemImage(i, 3, 3)
                        if self.IsDetailed:
                            self.SetItemData(i, i)
                            st = os.stat(directory + '/' + item)
                            size = str(st.st_size)
                            mtime = time.strftime(self.timeformat ,time.localtime(st.st_mtime))
                            mmode = str(oct(stat.S_IMODE(st.st_mode)))
                            type_ = item.rfind('.')
                            if type > -1:
                                type_ = item[type_+1:]
                            else:
                                type_ = ''

                            self.DataArray.append((item, size, type_, mtime, mmode))

                            self.SetStringItem(i, 1, str(size))
                            self.SetStringItem(i, 2, type_)
                            self.SetStringItem(i, 3, mtime)
                            self.SetStringItem(i, 4, mmode)
        except:
            self.grandparent.ShowMessage('Error Setting Directory To:' + directory, 'File Dialog Error')

    def SetShowHiddenFiles(self, showhidden):
        self.ShowHiddenFiles = showhidden

    def SetViewDetailed(self, fstyle = 0):
        self.DeleteAllItems()
        self.SetWindowStyleFlag(fstyle|wx.LC_REPORT)
        self.IsDetailed = True
        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Size')
        self.InsertColumn(2, 'Type')
        self.InsertColumn(3, 'Modified')
        self.InsertColumn(4, 'Permissions')

        self.SetColumnImage(0, 5)

        self.OnSize(None)

    def SetViewList(self, fstyle = 0):
        self.DeleteAllItems()
        self.SetWindowStyleFlag(fstyle|wx.LC_LIST)
        self.IsDetailed = False

    def SortData(self, item1, item2):
        i1 = self.DataArray[item1][self.currentcolumn]
        i2 = self.DataArray[item2][self.currentcolumn]
        i1isdir = self.IsDirectory(item1)
        i2isdir = self.IsDirectory(item2)
        if i1isdir and not i2isdir:
            if self.direction[self.currentcolumn]:
                return 1
            else:
                return -1
        elif not i1isdir and i2isdir:
            if self.direction[self.currentcolumn]:
                return -1
            else:
                return 1
        elif i1isdir and i2isdir:
            if self.currentcolumn == 1:
                i1 = self.DataArray[item1][0]
                i2 = self.DataArray[item2][0]
            elif self.currentcolumn == 3:
                it1 = time.strptime(i1, self.timeformat)
                it2 = time.strptime(i2, self.timeformat)

                i2 = it1[0]
                i1 = it2[0]
                x = 1
                while (i1 == i2) and (x < 6):
                    i2 = it1[x]
                    i1 = it2[x]
                    x = x + 1
            if self.direction[self.currentcolumn]:
                if i1 < i2:
                    return 1
                if i1 > i2:
                    return -1
            else:
                if i1 < i2:
                    return -1
                if i1 > i2:
                    return 1
        if self.currentcolumn == 1:
            try:
                i1 = int(i1)
            except:
                i1 = 0
            try:
                i2 = int(i2)
            except:
                i1 = 0
        elif self.currentcolumn == 3:
            it1 = time.strptime(i1, self.timeformat)
            it2 = time.strptime(i2, self.timeformat)

            i1 = it1[0]
            i2 = it2[0]
            x = 1
            while (i1 == i2) and (x < 6):
                i1 = it1[x]
                i2 = it2[x]
                x = x + 1

        if self.direction[self.currentcolumn]:
            if i1 < i2:
                return -1
            if i1 > i2:
                return 1
        else:
            if i1 < i2:
                return 1
            if i1 > i2:
                return -1
        return 0

class DirPanel(wx.Dialog):
    def __init__(self, parent, id, pos, size):
        wx.Dialog.__init__(self, parent, id, 'Look In:', pos, size)

        self.parent = parent

        self.ID_CLOSE = 3031

        self.dirControl = wx.GenericDirCtrl(self, -1, size=size, style=wx.DIRCTRL_DIR_ONLY)

        self.btnClose = wx.Button(self, self.ID_CLOSE, 'Close')

        self.theSizer = wx.BoxSizer(wx.VERTICAL)
        self.theSizer.Add(self.dirControl, 1, wx.EXPAND)
        self.theSizer.Add(self.btnClose, 0, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=self.ID_CLOSE)

    def GetPath(self):
        return self.dirControl.GetPath()

    def OnClose(self, event):
        self.EndModal(0)

class drFileDialog(wx.Dialog):
    def __init__(self, parent, title, wildcard, point=wx.DefaultPosition, size=wx.DefaultSize, IsASaveDialog=0, MultipleSelection=0, ShowRecentFiles=0):
        wx.Dialog.__init__(self, parent, -1, title, point, size, wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.parent = parent

        self.IsASaveDialog = IsASaveDialog
        self.MultipleSelection = MultipleSelection
        if IsASaveDialog:
            self.MultipleSelection = False

        #Constants:

        self.ID_BOOKMARKS = 3001
        self.ID_DISPLAY_LIST = 3002
        self.ID_DISPLAY_DETAILED = 3003
        self.ID_BACK = 3004
        self.ID_FORWARD = 3005
        self.ID_UP = 3006
        self.ID_HOME = 3011
        self.ID_REFRESH = 3007
        self.ID_NEW_DIRECTORY = 3008
        self.ID_DELETE_FILE = 3009

        self.ID_BROWSE = 3010

        self.ID_SHOW_HIDDEN_FILES = 3011

        self.ID_LIST_FILES =  3015

        self.ID_DIR = 3020
        self.ID_FILE = 3030
        self.ID_EXTENSION = 3031
        self.ID_SHOW_READONLY = 3032
        self.ID_ENCODING = 3035

        self.ID_OK = 3040
        self.ID_CANCEL = 3041

        self.ID_BOOKMARK_MENU = 3100

        self.ID_BOOKMARK_ADD = 3101
        self.ID_BOOKMARK_FILE = 3102

        self.ID_EDIT_BOOKMARKS = 3103

        self.ID_BOOKMARK_BASE = 3150

        #/Constants

        #Components:

        #ShowRecentFiles is not used anymore.
        self.cboFile = wx.ComboBox(self, self.ID_FILE, size=(500, -1))

        self.btnOk = wx.Button(self, self.ID_OK, "  &Ok  ")

        self.cboExtension = wx.ComboBox(self, self.ID_EXTENSION, size=(250, -1))

        try:
            defaultlocale = locale.getdefaultlocale()[1]
        except:
            defaultlocale = None
        if defaultlocale is not None:
            encodings = ['<Default Encoding>', defaultlocale, 'ascii', 'latin-1', 'cp1252', 'utf-8', 'utf-16']
        else:
            encodings = ['<Default Encoding>', 'ascii', 'latin-1', 'cp1252', 'utf-8', 'utf-16']

        self.cboEncoding = wx.ComboBox(self, self.ID_ENCODING, size=(250, -1), choices=encodings)

        if 1: #not self.parent.PLATFORM_IS_WIN:
            self.chkShowHiddenFiles = wx.CheckBox(self, self.ID_SHOW_HIDDEN_FILES, '  Show Hidden Files  ')

        self.btnCancel = wx.Button(self, self.ID_CANCEL, "  &Cancel  ")

        bDir = self.parent.bitmapdirectory + '/24/'

        self.btnDisplayList = wx.BitmapButton(self, self.ID_DISPLAY_LIST, wx.BitmapFromImage(wx.Image(bDir+'list.png', wx.BITMAP_TYPE_PNG)))
        self.btnDisplayDetailed = wx.BitmapButton(self, self.ID_DISPLAY_DETAILED, wx.BitmapFromImage(wx.Image(bDir+'detailed.png', wx.BITMAP_TYPE_PNG)))
        self.btnBack = wx.BitmapButton(self, self.ID_BACK, wx.BitmapFromImage(wx.Image(bDir+'back.png', wx.BITMAP_TYPE_PNG)))
        self.btnForward = wx.BitmapButton(self, self.ID_FORWARD, wx.BitmapFromImage(wx.Image(bDir+'forward.png', wx.BITMAP_TYPE_PNG)))
        self.btnUp = wx.BitmapButton(self, self.ID_UP, wx.BitmapFromImage(wx.Image(bDir+'up.png', wx.BITMAP_TYPE_PNG)))
        self.btnHome = wx.BitmapButton(self, self.ID_HOME, wx.BitmapFromImage(wx.Image(bDir+'home.png', wx.BITMAP_TYPE_PNG)))
        self.btnRefresh = wx.BitmapButton(self, self.ID_REFRESH, wx.BitmapFromImage(wx.Image(bDir+'Reload File.png', wx.BITMAP_TYPE_PNG)))
        self.btnBookmarks = wx.BitmapButton(self, self.ID_BOOKMARKS, wx.BitmapFromImage(wx.Image(bDir+'bookmarks.png', wx.BITMAP_TYPE_PNG)))
        self.btnDir = wx.BitmapButton(self, self.ID_BROWSE, wx.BitmapFromImage(wx.Image(bDir+'folder.png', wx.BITMAP_TYPE_PNG)))
        self.btnNewDirectory = wx.BitmapButton(self, self.ID_NEW_DIRECTORY, wx.BitmapFromImage(wx.Image(bDir+'new directory.png', wx.BITMAP_TYPE_PNG)))
        self.btnDeleteFile = wx.BitmapButton(self, self.ID_DELETE_FILE, wx.BitmapFromImage(wx.Image(bDir+'Delete.png', wx.BITMAP_TYPE_PNG)))

        self.btnDisplayList.SetToolTipString('List View')
        self.btnDisplayDetailed.SetToolTipString('Detailed View')
        self.btnBookmarks.SetToolTipString('Bookmarks')
        self.btnBack.SetToolTipString('Back')
        self.btnForward.SetToolTipString('Forward')
        self.btnUp.SetToolTipString('Up')
        self.btnHome.SetToolTipString('Home')
        self.btnRefresh.SetToolTipString('Refresh')
        self.btnDir.SetToolTipString('Look In')
        self.btnNewDirectory.SetToolTipString('New Directory')
        self.btnDeleteFile.SetToolTipString('Delete')

        self.txtDirectory = wx.TextCtrl(self, self.ID_DIR, '', size=(350, -1), style=wx.TE_PROCESS_ENTER)

        if MultipleSelection:
            self.lstFiles = FileListCtrl(self, self.ID_LIST_FILES, (500, 230), wx.LC_LIST)
        else:
            self.lstFiles = FileListCtrl(self, self.ID_LIST_FILES, (500, 230), wx.LC_LIST | wx.LC_SINGLE_SEL)


        self.btnOk.SetDefault()
        self.cboFile.SetFocus()

        #/Components

        #Data

        swildcards = wildcard.split('|')
        self.wildcards = []
        x = 0
        l = len(swildcards) - 1
        while x < l:
            self.cboExtension.Append(swildcards[x])
            self.wildcards.append(swildcards[x+1])
            x = x + 2

        self.cboExtension.SetValue(swildcards[0])
        wx.CallAfter (self.cboExtension.SetMark, 0, 0)

        if self.parent.prefs.defaultencoding:
            if not self.parent.prefs.defaultencoding in encodings:
                self.cboEncoding.Append(self.parent.prefs.defaultencoding)
            self.cboEncoding.SetSelection(encodings.index(self.parent.prefs.defaultencoding))
        else:
            self.cboEncoding.SetSelection(0)

        self.currentextension = 0

        self.lstFiles.SetDirectoryTo(self.parent.ddirectory, self.wildcards[self.currentextension])

        self.bookmarks = []

        #lnk Replace Table:
        if not self.parent.PLATFORM_IS_WIN:
            self.lnkReplaceA = []
            self.lnkReplaceB = []
            replacestrings = self.parent.prefs.windowsshortcutreplacetable.split('#')
            for rstring in replacestrings:
                if rstring:
                    a, b = rstring.split(',')
                    self.lnkReplaceA.append(a)
                    self.lnkReplaceB.append(b)
        #/Data

        #Sizer:

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.commandSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.commandSizer.Add(self.btnDisplayList, 0, wx.SHAPED)
        self.commandSizer.Add(self.btnDisplayDetailed, 0, wx.SHAPED)
        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)

        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.commandSizer.Add(self.btnBack, 0, wx.SHAPED)
        self.commandSizer.Add(self.btnForward, 0, wx.SHAPED)
        self.commandSizer.Add(self.btnUp, 0, wx.SHAPED)
        self.commandSizer.Add(self.btnHome, 0, wx.SHAPED)
        self.commandSizer.Add(self.btnRefresh, 0, wx.SHAPED)
        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)

        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.commandSizer.Add(self.btnBookmarks, 0, wx.SHAPED)
        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.commandSizer.Add(self.btnDir, 0, wx.SHAPED)

        if 1: #not self.parent.PLATFORM_IS_WIN:
            self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED | wx.ALIGN_RIGHT)
            self.commandSizer.Add(self.chkShowHiddenFiles, 1, wx.SHAPED | wx.ALIGN_RIGHT)
        else:
            self.commandSizer.Add(wx.StaticText(self, -1, '   '), 1, wx.EXPAND)

        self.commandSizer.Add(self.btnNewDirectory, 0, wx.SHAPED)
        self.commandSizer.Add(self.btnDeleteFile, 0, wx.SHAPED)
        self.commandSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)

        self.dirSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dirSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.dirSizer.Add(self.txtDirectory, 9, wx.EXPAND)
        self.dirSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)

        self.listSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.listSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.listSizer.Add(self.lstFiles, 9, wx.EXPAND)
        self.listSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)

        self.OkSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.OkSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.OkSizer.Add(self.cboFile, 9, wx.EXPAND | wx.ALIGN_LEFT)
        self.OkSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.OkSizer.Add(self.btnOk, 0, wx.ALIGN_RIGHT)
        self.OkSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)

        self.CancelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CancelSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.CancelSizer.Add(self.cboExtension, 2, wx.EXPAND)
        self.CancelSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.CancelSizer.Add(self.cboEncoding, 2, wx.EXPAND)
        self.CancelSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.CancelSizer.Add(self.btnCancel, 0, wx.ALIGN_RIGHT)
        self.CancelSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)

        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.theSizer.Add(self.commandSizer, 0, wx.EXPAND | wx.ALIGN_CENTER)
        self.theSizer.Add(self.dirSizer, 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.theSizer.Add(self.listSizer, 9, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.theSizer.Add(self.OkSizer, 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)
        self.theSizer.Add(self.CancelSizer, 0, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        #/Sizer

        #Events:

        self.Bind(wx.EVT_BUTTON, self.OnbtnUp, id=self.ID_UP)
        self.Bind(wx.EVT_BUTTON, self.OnbtnBack, id=self.ID_BACK)
        self.Bind(wx.EVT_BUTTON, self.OnbtnForward, id=self.ID_FORWARD)
        self.Bind(wx.EVT_BUTTON, self.OnbtnHome, id=self.ID_HOME)
        self.Bind(wx.EVT_BUTTON, self.OnbtnRefresh, id=self.ID_REFRESH)
        self.Bind(wx.EVT_BUTTON, self.OnbtnBookmarks, id=self.ID_BOOKMARKS)

        self.Bind(wx.EVT_BUTTON, self.OnbtnNewDirectory, id=self.ID_NEW_DIRECTORY)
        self.Bind(wx.EVT_BUTTON, self.OnbtnDelete, id=self.ID_DELETE_FILE)

        self.Bind(wx.EVT_BUTTON, self.OnbtnDisplayList, id=self.ID_DISPLAY_LIST)
        self.Bind(wx.EVT_BUTTON, self.OnbtnDisplayDetailed, id=self.ID_DISPLAY_DETAILED)

        self.Bind(wx.EVT_BUTTON, self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnbtnOk, id=self.ID_OK)

        self.Bind(wx.EVT_COMBOBOX, self.OnExtension, id=self.ID_EXTENSION)

        if 1: #not self.parent.PLATFORM_IS_WIN:
            self.Bind(wx.EVT_CHECKBOX, self.OnShowHiddenFiles, id=self.ID_SHOW_HIDDEN_FILES)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnFileSelected, id=self.ID_LIST_FILES)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnFileActivated, id=self.ID_LIST_FILES)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDir, id=self.ID_DIR)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnbtnOk, id=self.ID_FILE)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.cboFile.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_BUTTON, self.OnBrowse, id=self.ID_BROWSE)

        #/Events

        self.parent.LoadDialogSizeAndPosition(self, 'filedialog.sizeandposition.dat')

    def OnCloseW(self, event):
        self.parent.SaveDialogSizeAndPosition(self, 'filedialog.sizeandposition.dat')
        if event is not None:
            event.Skip()

    def EndAndCheck(self, value):
        if self.IsASaveDialog:
            filename = self.GetPath()
            if os.path.exists(filename):
                msg = 'File "' + filename + '" already exists.  Overwrite?'
                if not self.parent.Ask(msg, "OverWrite File?"):
                    return
        self.OnCloseW(None)
        self.EndModal(value)

    def GetEncoding(self):
        return self.cboEncoding.GetValue()

    def getNormedPath(self, filename):
        if filename.find(".lnk") > -1:
            filename = self.HandleLnk(filename)
        else:
            filename = filename.replace('\\', '/')
        return filename

    def GetPath(self):
        path = self.getNormedPath(self.cboFile.GetValue())
        if self.IsASaveDialog and self.parent.prefs.defaultextension:
            if path.find('.') == -1:
                path += '.py'
        return path

    def GetPaths(self):
        i = self.lstFiles.GetFirstSelected()
        if i == -1:
            return [self.getNormedPath(self.cboFile.GetValue())]

        if (self.lstFiles.GetItemText(i) != self.cboFile.GetValue()) and (self.lstFiles.GetNextSelected(i) == -1):
            return [self.getNormedPath(self.cboFile.GetValue())]

        dir = self.lstFiles.GetDirectory()
        filelist = [self.getNormedPath(os.path.join(dir, self.lstFiles.GetItemText(i)).replace('\\', '/'))]

        y = i
        y = self.lstFiles.GetNextSelected(y)
        while y != -1:
            filelist.append(self.getNormedPath(os.path.join(dir, self.lstFiles.GetItemText(y)).replace('\\', '/')))
            y = self.lstFiles.GetNextSelected(y)
        currentfile = self.getNormedPath(self.cboFile.GetValue().replace('\\', '/'))
        if not (currentfile in filelist):
            filelist.insert(0, currentfile)
        return filelist

    def HandleLnk(self, filename):
        filename = lnkDecoderRing.ReadLink(filename)
        if self.parent.PLATFORM_IS_WIN:
            return filename
        else:
            x = 0
            for rA in self.lnkReplaceA:
                result = re.match(rA + '\:', filename)
                resultA = re.match(rA, filename)
                if result is not None:
                    if self.lnkReplaceB[x].find('@') > 0:
                        return filename.replace(result.group(), self.lnkReplaceB[x].replace('@', resultA.group().lower()))
                    elif self.lnkReplaceB[x].find('@') > 0:
                        return filename.replace(result.group(), self.lnkReplaceB[x].replace('@', resultA.group()))
                    else:
                        return filename.replace(result.group(), self.lnkReplaceB[x])
                x += 1
        self.parent.ShowMessage('Windows Shortcut Error:\n\nCould not Find: "%s".' % (filename), 'Error')
        return None

    def HandleDesktop(self, filename):
        f = open(filename, 'rb')
        lines = f.read().split()
        f.close()

        for line in lines:
            if line.find('URL=') > -1:
                return line[4:]

        return None

    def OnAddBookmark(self, event):
        try:
            bookfile = self.parent.datdirectory + "/bookmarks.dat"

            f = open(bookfile, 'rb')
            text = f.read()
            f.close()

            text = text.strip()

            cdir = self.lstFiles.GetDirectory()

            text = text + '\n\t' + cdir + '\n'

            f = open(bookfile, 'wb')
            f.write(text)
            f.close()

            self.parent.bookmarksmenu.reloadBookmarks()

            if self.parent.prefs.enablefeedback:
                self.parent.ShowMessage('Successfully Added ' + cdir, 'Success')
        except:
            self.parent.ShowMessage('Error Adding Bookmark', 'Error')

    def OnBookmark(self, event):
        bookmarkindex = event.GetId() - self.ID_BOOKMARK_BASE
        if not (os.path.exists(self.bookmarks[bookmarkindex])):
            drScrolledMessageDialog.ShowMessage(self.parent, ("Error with: " + self.bookmarks[bookmarkindex] + "\nBookmark does not actually exist.\n"), "Error")
            return
        if os.path.isdir(self.bookmarks[bookmarkindex]):
            self.lstFiles.SetDirectoryTo(self.bookmarks[bookmarkindex], self.wildcards[self.currentextension])
            return
        self.cboFile.SetValue(self.bookmarks[bookmarkindex])

    def OnbtnBack(self, event):
        self.lstFiles.GoBack(self.wildcards[self.currentextension])

    def OnbtnBookmarks(self, event):
        bookfile = self.parent.datdirectory + "/bookmarks.dat"
        bookmarksmenu = wx.Menu()

        bookmarksmenu.Append(self.ID_BOOKMARK_ADD, 'Bookmark Current Directory')
        bookmarksmenu.Append(self.ID_BOOKMARK_FILE, 'File Current Directory...')
        bookmarksmenu.Append(self.ID_EDIT_BOOKMARKS, 'Edit Bookmarks...')
        bookmarksmenu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.OnAddBookmark, id=self.ID_BOOKMARK_ADD)
        self.Bind(wx.EVT_MENU, self.OnFileBookmark, id=self.ID_BOOKMARK_FILE)
        self.Bind(wx.EVT_MENU, self.parent.OnEditBookmarks, id=self.ID_EDIT_BOOKMARKS)

        self.bookmarks = []
        if os.path.exists(bookfile):
            try:
                #Read from the file
                f = open(bookfile, 'r')
                folders = [bookmarksmenu]
                folderindex = 0
                menuTitles = []
                menuTitleindex = -1
                lastCount = 1
                bookmarkcount = 0
                #Skip the First Line
                line = f.readline()
                #Initialize
                line = f.readline()
                while line:
                    c = line.count('\t')
                    line = line[c:].rstrip()
                    while lastCount > c:
                        folders[(folderindex - 1)].AppendMenu(self.ID_BOOKMARK_MENU, menuTitles.pop(), folders.pop())
                        folderindex = folderindex - 1
                        menuTitleindex = menuTitleindex - 1
                        lastCount = lastCount - 1
                    if line[0] == '>':
                        folders.append(wx.Menu())
                        menuTitles.append(line[1:])
                        folderindex = folderindex + 1
                        menuTitleindex = menuTitleindex + 1
                        c = c + 1
                    else:
                        self.bookmarks.append(line)
                        self.Bind(wx.EVT_MENU, self.OnBookmark, id=(self.ID_BOOKMARK_BASE + bookmarkcount))
                        folders[folderindex].Append((self.ID_BOOKMARK_BASE + bookmarkcount), line)
                        bookmarkcount = bookmarkcount + 1
                    lastCount = c
                    line = f.readline()
                f.close()
                #Add any menus not yet added:
                c = 1
                while lastCount > c:
                    folders[(folderindex - 1)].AppendMenu(self.ID_BOOKMARK_MENU, menuTitles.pop(), folders.pop())
                    folderindex = folderindex - 1
                    menuTitleindex = menuTitleindex - 1
                    lastCount = lastCount - 1

            except:
                drScrolledMessageDialog.ShowMessage(self, ("Your bookmarks file is a tad messed up.\n"), "Error")
                return
        else:
            f = open(bookfile, 'wb')
            f.write('>Bookmarks\n')
            f.close()

        posX, posY = self.btnBookmarks.GetPosition()
        posY = posY + self.btnBookmarks.GetSize()[1]
        self.PopupMenu(bookmarksmenu, (posX, posY))
        bookmarksmenu.Destroy()

    def OnBrowse(self, event):
        posX, posY = self.btnDir.GetPosition()
        posY = posY + self.btnDir.GetSize()[1]
        d = DirPanel(self, -1, (posX, posY), (250, 300))
        d.ShowModal()
        self.lstFiles.SetDirectoryTo(d.GetPath(), self.wildcards[self.currentextension])
        d.Destroy()

    def OnbtnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnbtnDelete(self, event):
        filename = self.cboFile.GetValue()
        if os.path.exists(filename) and not os.path.isdir(filename):
            msg = 'Delete "' + filename + '"?'
            if self.parent.Ask(msg, "Delete File?"):
                try:
                    os.remove(filename)
                    self.cboFile.SetValue('')
                    self.OnbtnRefresh(None)
                except:
                    drScrolledMessageDialog.ShowMessage(self, 'Error Removing "' + filename + '".', "Error")

    def OnbtnDisplayDetailed(self, event):
        if self.MultipleSelection:
            self.lstFiles.SetViewDetailed()
        else:
            self.lstFiles.SetViewDetailed(wx.LC_SINGLE_SEL)
        self.lstFiles.SetDirectoryTo(self.lstFiles.GetDirectory(), self.wildcards[self.currentextension])

    def OnbtnDisplayList(self, event):
        if self.MultipleSelection:
            self.lstFiles.SetViewList()
        else:
            self.lstFiles.SetViewList(wx.LC_SINGLE_SEL)
        self.lstFiles.SetDirectoryTo(self.lstFiles.GetDirectory(), self.wildcards[self.currentextension])

    def OnbtnForward(self, event):
        self.lstFiles.GoForward(self.wildcards[self.currentextension])

    def OnbtnHome(self, event):
        try:
            self.lstFiles.SetDirectoryTo(os.path.expanduser('~'), self.wildcards[self.currentextension])
        except:
            drScrolledMessageDialog.ShowMessage(self, 'Error Setting Current Directory to Home', "DrPython Error")

    def OnbtnNewDirectory(self, event):
        d = wx.TextEntryDialog(self, "Enter New Directory:", "New Directory", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            if v:
                os.mkdir(self.lstFiles.GetDirectory() + '/' + v)
                self.OnbtnRefresh(None)

    def OnbtnOk(self, event):
        filename = self.cboFile.GetValue()
        if not os.path.isabs(filename):
            fname = self.txtDirectory.GetValue()
            if not fname.endswith ('/'):
                fname += '/'
            filename = fname + filename
        if filename.find(".lnk") > -1:
            filename = self.HandleLnk(filename)
            if filename is None:
                return
        elif filename.find('.desktop') > -1:
            filename = self.HandleDesktop(filename)
            if filename is None:
                return
        if not self.IsASaveDialog:
            if not os.path.exists(filename):
                if wx.MessageBox('"' + filename + '" does not exist.\Do you want to create it?',
                    "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                    f = open(filename, "w")
                    f.close()
                else:
                    return
        if os.path.isdir(filename):
            self.cboFile.SetValue('')
            self.lstFiles.SetDirectoryTo(filename, self.wildcards[self.currentextension])
        else:
            self.cboFile.SetValue(filename)
            self.EndAndCheck(wx.ID_OK)

    def OnbtnRefresh(self, event):
        self.lstFiles.SetDirectoryTo(self.lstFiles.GetDirectory(), self.wildcards[self.currentextension])

    def OnbtnUp(self, event):
        cdir = os.path.split(self.lstFiles.GetDirectory())[0]
        self.lstFiles.SetDirectoryTo(cdir, self.wildcards[self.currentextension])

    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.OnbtnCancel(None)
        elif event.GetKeyCode() == wx.WXK_RETURN:
            self.OnbtnOk(None)
        else:
            event.Skip()

    def OnDir(self, event):
        directory = self.txtDirectory.GetValue()
        if os.path.exists(directory):
            self.lstFiles.SetDirectoryTo(directory, self.wildcards[self.currentextension])
        else:
            self.parent.ShowMessage('"%s" does not exist.' % (directory), 'Error')

    def OnExtension(self, event):
        self.currentextension = self.cboExtension.GetSelection()
        self.lstFiles.SetDirectoryTo(self.lstFiles.GetDirectory(), self.wildcards[self.currentextension])

    def OnFileActivated(self, event):
        seltext = event.GetLabel()
        filename = self.lstFiles.GetDirectory() + '/' + seltext
        if filename.find(".lnk") > -1:
            filename = self.HandleLnk(filename)
            if filename is None:
                return
        elif filename.find('.desktop') > -1:
            filename = self.HandleDesktop(filename)
            if filename is None:
                return
        if not self.IsASaveDialog:
            if not os.path.exists(filename):
                self.parent.ShowMessage('"' + filename + '" does not exist.', 'Error')
                return
        if os.path.isdir(filename):
            self.lstFiles.SetDirectoryTo(filename, self.wildcards[self.currentextension])
        else:
            self.EndAndCheck(wx.ID_OK)

    def OnFileBookmark(self, event):
        try:
            bookfile = self.parent.datdirectory + "/bookmarks.dat"

            f = open(bookfile, 'rb')
            text = f.read()
            f.close()

            lines = text.strip().split('\n')

            x = 0
            folders = []
            linenumbers = []

            for line in lines:
                c = line.count('\t')
                pre = line[:c].replace('\t', '    ')
                line = line[c:].rstrip()
                if line[0] == '>':
                    folders.append(pre + line[1:])
                    linenumbers.append(x)
                x += 1

            cdir = self.lstFiles.GetDirectory()

            d = wx.SingleChoiceDialog(self.parent, 'Select Bookmark Folder:', "File Bookmark", folders, wx.CHOICEDLG_STYLE)
            answer = d.ShowModal()
            result = d.GetSelection()

            if answer == wx.ID_OK:
                target = linenumbers[result]

                f = open(bookfile, 'wb')

                x = 0
                for line in lines:
                    f.write(line + '\n')
                    if x == target:
                        c = line.count('\t')
                        istring = '\t'
                        for a in range(c):
                            istring += '\t'
                        f.write(istring + cdir + '\n')
                    x += 1
                f.close()

                self.parent.bookmarksmenu.reloadBookmarks()

                if self.parent.prefs.enablefeedback:
                    self.parent.ShowMessage('Successfully Added ' + cdir, 'Success')
        except:
            self.parent.ShowMessage('Error Filing Bookmark', 'Error')

    def OnFileSelected(self, event):
        seltext = event.GetLabel()
        filename = self.lstFiles.GetDirectory()
        if not filename.endswith ('/'):
            filename += '/'
        filename += seltext
        if not os.path.isdir(filename):
            self.cboFile.SetValue(filename)

    def OnShowHiddenFiles(self, event):
        showhidden = self.chkShowHiddenFiles.GetValue()
        self.lstFiles.SetShowHiddenFiles(showhidden)
        self.OnbtnRefresh(None)

    def SetDirectory(self, directory):
        if not os.path.exists(directory):
            directory = self.parent.userhomedirectory
        self.lstFiles.SetDirectoryTo(directory, self.wildcards[self.currentextension])

    def SetFilename(self, filename):
        self.cboFile.SetValue(filename)

class drWxFileDialog(wx.FileDialog):
    def __init__(self, parent, message, defaultDir, defaultFile, wildcard, style):
        wx.FileDialog.__init__(self, parent, message, defaultDir, defaultFile, wildcard, style)

    def GetEncoding(self):
        return '<Default Encoding>'

#Wrapper for drFileDialog
def FileDialog(parent, title, wildcard, point=(0, 0), size=wx.DefaultSize, IsASaveDialog=0, MultipleSelection=0, ShowRecentFiles=0):
        if parent.prefs.usewxfiledialog:
            if IsASaveDialog:
                return drWxFileDialog(parent, title, "", "", wildcard, wx.SAVE|wx.HIDE_READONLY|wx.OVERWRITE_PROMPT)
            else:
                return drWxFileDialog(parent, title, "", "", wildcard, wx.OPEN|wx.HIDE_READONLY|wx.MULTIPLE)
        else:
            return drFileDialog(parent, title, wildcard, point, size, IsASaveDialog, MultipleSelection, ShowRecentFiles)
