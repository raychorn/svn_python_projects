def wxGetNumberFromUser(message,caption,default_value,i_begin,i_end,parent):
    import wx

    isError = False
    while (1):
        x = wx.GetTextFromUser(message,caption,str(default_value),parent)
        try:
            isDigits = str(x).isdigit()
            x = int(x)
        except:
            isError = True
        if (not isDigits) or (isError):
            dlg = wx.MessageDialog(parent, 'The value (%s) entered is either not a number or is out of range (%s to %s).\nPlease try again...' % (x,i_begin,i_end), 'Data Input Error', wx.CANCEL | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            break
    return x

