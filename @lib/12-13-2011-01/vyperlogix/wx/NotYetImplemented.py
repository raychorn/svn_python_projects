import wx

def wx_NotYetImplemented_Dialog(parent=None,msg=''):
    dlg = wx.MessageDialog(parent, 'Not yet implemented.  %s' % (msg), 'INFO', wx.CANCEL | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
    dlg.ShowModal()
    dlg.Destroy()
    del dlg
