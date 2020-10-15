# test the wx.SpinCtrl() widget
# wx.SpinCtrl(parent, id, value, pos, size, style, min, max, initial)
# used for integer number input
# style =
# wx.SP_ARROW_KEYS  can use arrow keys to change the value
# wx.SP_WRAP  value wraps at the minimum and maximum.

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size=mysize)
        self.SetBackgroundColour("yellow")

        # create a spinctrl widget for inteer input
        self.spin = wx.SpinCtrl( self, wx.ID_ANY, value="",
            pos=(10, 20), size=(80, 25), min=-100, max=1000,
            initial=98, style=wx.SP_ARROW_KEYS)
        # bind mouse click on arrows to an action
        self.spin.Bind(wx.EVT_SPINCTRL, self.onAction)
        # you can edit the value directly
        self.spin.Bind(wx.EVT_TEXT, self.onAction)

        # create an output widget
        s1 = "click on arrows to change the spinbox value \n"
        s2 = "or type the integer value directly"
        self.label = wx.StaticText(self, wx.ID_ANY, s1+s2, pos=(10, 60))

    def onAction(self, event):
        """ some action code"""
        val = self.spin.GetValue()
        f = str(round(val * 9.0/5 + 32, 2))
        c = str(round((val - 32)*5/9.0, 2))
        v = str(val)
        s1 = v + " degree Fahrenheit is " + c + " degree Celcius \n"
        s2 = v + " degree Celcius is " + f + " degree Fahrenheit"
        self.label.SetLabel(s1 + s2)


app = wx.App(0)
# create a MyFrame instance and show the frame
MyFrame(None, 'testing the wx.SpinCtrl()', (300, 150)).Show()
app.MainLoop()