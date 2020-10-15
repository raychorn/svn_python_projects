#drscript
#This currently only works on linux (if you have rxvt installed).
#You will need to modify it otherwise.

#By Daniel Pozmanter
#Released under the GPL

import os

pathtoterminal = "/usr/bin/X11/rxvt"
termarg = "-e"
withargs = ""
if DrScript.VariableExists("RunInTerminalArgs"):
    withargs = DrScript.RunInTerminalArgs
d = wx.TextEntryDialog(DrFrame, "Arguments:", "Set Arguments For Run In Terminal", withargs)
if d.ShowModal() == wx.ID_OK:
    DrScript.RunInTerminalArgs = d.GetValue()