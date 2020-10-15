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

# drSaveRootFile.py
# for saving files with root rights in gtk

# called from drpython.py
# with os.system("gksudo python %s %s %d" % (drSaveRootFile, self.txtDocumentArray[docPos].filename, backupfile)

import os
import sys
import wx
import shutil

#print len(sys.argv), str(sys.argv)
#4 ['/home/franz/bin/DrPython/drSaveRootFile.py', '/etc/uniconf.conf', '/home/franz/savetmpfile.tmp', '0']

savefilename = sys.argv[1] #filename with root rights
tmpfilename = sys.argv[2] #savetmpfile.tmp
makebackupfile = sys.argv[3]

#print makebackupfile, type(makebackupfile), len(makebackupfile)
if makebackupfile == "1":
    try:
        shutil.copyfile(savefilename, savefilename+".bak")
        #app = wx.App()
        #wx.MessageBox("Backing up to: '" + savefilename + ".bak'", "DrPython Save Backup File Root")
    except:
        app = wx.App()
        wx.MessageBox("Error Backing up to: '" + savefilename + ".bak'", "DrPython Save Backup File Root Error")


#open the tmpfilename
tmpfile = open(tmpfilename, 'rb')
text = tmpfile.read()
tmpfile.close()

#save to filename
savefile = open(savefilename, 'wb')
savefile.write(text)
savefile.close()

#delete tmpfile, when successful
#print tmpfilename
os.remove(tmpfilename)
