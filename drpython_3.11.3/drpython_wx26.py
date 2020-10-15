#!/usr/bin/env python

#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2004 Daniel Pozmanter
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
#

# drpython 2.6
  
#  To Run:
#
#   Windows Users:  Make sure ".pyw" files are associated with the pythonw.exe file in your python-directory.
#
#   Linux/Unix Users:  Make sure the first line of this file is the correct path to python:
#   "/bin/python", "/usr/bin/python", "/usr/local/bin/python" are all suggestions.
#   Using "/bin/env python" should find it for you though.
#


## testfile for older version
import wxversion
wxversion.select("2.60-msw-ansi")

if __name__ == '__main__':
    import drpython
    app = drpython.DrApp(0)
    app.MainLoop()
