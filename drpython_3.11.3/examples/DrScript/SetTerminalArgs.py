#drscript
#This currently only works on linux (if you have xterm installed).
#You will need to modify it otherwise.

#By Daniel Pozmanter
#Released under the GPL

import wx

arguments = getattr(DrScript, 'RunInTerminalArgs', '')
dialog = wx.TextEntryDialog(DrFrame,
                            'Arguments:',
                            'Set Arguments For Run In Terminal',
                            arguments)c
if dialog.ShowModal() == wx.ID_OK:
    DrScript.RunInTerminalArgs = dialog.GetValue()
