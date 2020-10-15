#drscript
#This currently only works on linux (if you have xterm installed).
#You will need to modify it otherwise.

#By Daniel Pozmanter
#Released under the GPL

import os, sys

if 'linux' in sys.platform:
    pathtoterminal = "/usr/bin/xterm"
    termarg = "-e"
    arguments = getattr(DrScript, 'RunInTerminalArgs', '')
    command = sys.executable + ' ' + DrFrame.GetFileName() + ' ' + arguments
    os.spawnl(os.P_NOWAIT, pathtoterminal, pathtoterminal, termarg, command)
else:
    wx.MessageBox("Only supported under Linux", "RunInTerminal", wx.OK, DrFrame)
