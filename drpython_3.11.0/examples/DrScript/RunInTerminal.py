#drscript
#This currently only works on linux (if you have rxvt installed).
#You will need to modify it otherwise.

#By Daniel Pozmanter
#Released under the GPL

import os, sys

if sys.platform.find("linux") > -1:
    pathtoterminal = "/usr/bin/X11/rxvt"
    termarg = "-e"
    withargs = ""
    if DrScript.VariableExists("RunInTerminalArgs"):
        withargs = " " + DrScript.RunInTerminalArgs
        
    pyexec = "/usr/bin/python " + DrFrame.GetFileName() + withargs
    os.spawnl(os.P_NOWAIT, pathtoterminal, pathtoterminal, termarg, pyexec)
else:
    wx.MessageBox("Only supported under Linux", "RunInTerminal", wx.OK, DrFrame)