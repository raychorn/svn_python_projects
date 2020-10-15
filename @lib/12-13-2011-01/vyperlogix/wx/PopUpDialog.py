import wx

def wx_PopUp_Dialog(parent=None,msg='',title='INFO',styles=wx.CANCEL|wx.ICON_INFORMATION):
    '''styles can be one of the following:
    wx.OK ................ show Ok button
    wx.CANCEL ............ show Cancel button
    wx.YES_NO .............show Yes, No buttons
    wx.YES_DEFAULT ........make Yes button the default
    wx.NO_DEFAULT .........make No button the default
    wx.ICON_EXCLAMATION ...show an alert icon
    wx.ICON_ERROR .........show an error icon
    wx.ICON_HAND ..........same as wx.ICON_ERROR
    wx.ICON_INFORMATION ...show an info icon
    wx.ICON_QUESTION ......show a question icon
    
    Shows the dialog, returning one of wx.ID_OK, wx.ID_CANCEL, wx.ID_YES, wx.ID_NO
    '''
    if ((styles & wx.OK) == 0) and ((styles & wx.YES_NO) == 0):
        styles |= wx.CANCEL
    dlg = wx.MessageDialog(parent, '%s' % (msg), title, styles | wx.CENTRE | wx.STAY_ON_TOP)
    resp = dlg.ShowModal()
    dlg.Destroy()
    del dlg
    return resp
