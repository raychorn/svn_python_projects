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

#Bookmarks Menu

import os.path
import wx
from drProperty import *
import drScrolledMessageDialog

class drBookmarksMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)

        self.ID_BOOKMARK_BASE = 5500

        self.ID_BOOKMARK_MENU = 5199

        self.bookmarks = []

        self.parent = parent
        self.datdirectory = parent.datdirectory

        self.loadBookmarks()

    def loadBookmarks(self):
        bookfile = self.datdirectory + "/bookmarks.dat"
        if os.path.exists(bookfile):
            try:
                #Read from the file
                f = open(bookfile, 'r')
                folders = [self]
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
                        self.parent.Bind(wx.EVT_MENU, self.OnBookmark, id=(self.ID_BOOKMARK_BASE + bookmarkcount))
                        folders[folderindex].Append((self.ID_BOOKMARK_BASE + bookmarkcount), line, line)
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
                drScrolledMessageDialog.ShowMessage(self.parent, ("Your bookmarks file is a tad messed up.\n"), "Error")

    def OnBookmark(self, event):
        bookmarkindex = event.GetId() - self.ID_BOOKMARK_BASE
        if not os.path.exists(self.bookmarks[bookmarkindex]):
            drScrolledMessageDialog.ShowMessage(self.parent, ("Error with: " + self.bookmarks[bookmarkindex] + "\nBookmark does not actually exist.\n"), "Error")
        elif os.path.isdir(self.bookmarks[bookmarkindex]):
            self.parent.ddirectory = self.bookmarks[bookmarkindex].replace("\\", "/")
            self.parent.OnOpen(event)
        else:
            filename = self.bookmarks[bookmarkindex].replace("\\", "/")
            self.parent.OpenOrSwitchToFile(filename)
        
    def reloadBookmarks(self):
        mnuitems = self.GetMenuItems()
        num = len(mnuitems)
        x = 0
        while x < num:
            self.Remove(mnuitems[x].GetId())
            #mnuitems[x].Destroy()
            x = x + 1
        self.bookmarks = []
        self.loadBookmarks()
