#   Programmer: user marrin
#
#   Copyright 2010-2007 user marrin
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

#DrFileHistory

import wx

class DrFileHistory(wx.FileHistory):
    """Subclass of `wx.FileHistory` acting more like a Python sequence.

    It has a length, index access and is iterable.  Additionally there are
    methods to load and save the list of paths.

    :bug: `LoadFromFile()` and `SaveToFile()` can't cope with filenames ending
        in whitespace or containing newline characters.
    """
    def __init__(self, maxFiles, idBase):
        wx.FileHistory.__init__(self, maxFiles, idBase)
        self.IdBase = idBase
        for i in xrange(self.MaxFiles):
            wx.RegisterId(self.IdBase + i)

    __len__ = wx.FileHistory.GetCount

    def __getitem__(self, index):
        if not (0 <= index < len(self)):
            raise IndexError
        return self.GetHistoryFile(index)

    def __delitem__(self, index):
        if not (0 <= index < len(self)):
            raise IndexError
        self.RemoveFileFromHistory(index)

    def Clear(self):
        """Clears all paths in the history."""
        for dummy in xrange(len(self)):
            del self[0]

    def LoadFromFile(self, filename):
        """Loads the history of paths.

        The current items are replaced by the file content.
        """
        self.Clear()
        with open(filename, 'r') as lines:
            for line in lines:
                self.AddFileToHistory(line.rstrip())

    def SaveToFile(self, filename):
        """Saves the history of paths."""
        with open(filename, 'w') as out_file:
            out_file.writelines(s + '\n' for s in reversed(self))

