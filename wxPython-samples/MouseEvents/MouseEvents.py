# get the position of the mouse when clicked or moved

import wx

class MyFrame(wx.Frame):
    """create a color frame, inherits from wx.Frame"""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, "Move or click mouse")
        self.SetBackgroundColour('Goldenrod')
        # give it a fancier cursor
        self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))

        # bind some mouse events
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

    def OnLeftDown(self, event):
        """left mouse button is pressed"""
        pt = event.GetPosition()  # position tuple
        self.SetTitle('LeftMouse click at = ' + str(pt))

    def OnRightDown(self, event):
        """right mouse button is pressed"""
        pt = event.GetPosition()
        self.SetTitle('RightMouse click at = ' + str(pt))

    def OnMotion(self, event):
        """mouse in motion"""
        pt = event.GetPosition()
        self.SetTitle('Mouse in motion at = ' + str(pt))


app = wx.App(0)
MyFrame(None).Show()
app.MainLoop()