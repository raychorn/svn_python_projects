# bind keyevent to key down and display the key value

import wx

class KeyEvent(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 70))
        self.SetBackgroundColour("yellow")
        # create a label
        self.label = wx.StaticText(self, wx.ID_ANY, label="  ", pos=(20, 30))

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.Show(True)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        s = "Key value = " + str(keycode)
        self.label.SetLabel(s)
        if keycode == wx.WXK_ESCAPE:
            choice = wx.MessageBox('Are you sure you want to quit? ',
                'Question', wx.YES_NO|wx.CENTRE|wx.NO_DEFAULT, self)
            if choice == wx.YES:
                self.Close()
        event.Skip()


app = wx.App()
KeyEvent(None, wx.ID_ANY, 'press any key (press escape to exit)')
app.MainLoop()