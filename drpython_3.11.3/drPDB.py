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

#pdb

import bdb
import sys

class drPdb(bdb.Bdb):
    """ Subclass of bdb that sends output to the prompt window """

    def __init__(self, drFrame):
        """ Set up for debugging """
        bdb.Bdb.__init__(self)

        self.save_stdout = sys.stdout
        self.save_stderr = sys.stderr

        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

        self.drFrame = drFrame

    def start(self,debugfile,globals=None,locals=None):
        """ Start debugging """

        # redirect output to prompt window
        sys.stdout = sys.stderr = self.drFrame.txtPrompt
        cmd = 'execfile("' + debugfile + '")'
        self.run(cmd,globals,locals)

        # get output back to original
        sys.stdout = self.save_stdout
        sys.stderr = self.save_stderr

