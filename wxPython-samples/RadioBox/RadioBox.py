# test the wx.RadioBox() widget
# wx.RadioBox(parent, id, label, pos, size, choices, style)
# combines a wx.StaticBox() with wx.RadioButton()
# only one radiobutton can be selected

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size=mysize)
        self.SetBackgroundColour("yellow")

        self.options = ['now', 'later', 'much later', 'never']
        # create an input widget
        self.radiobox = wx.RadioBox(self, wx.ID_ANY, "Select one option",
            pos=(10, 10), choices=self.options, style=wx.VERTICAL)
        # set radio button 1 as selected (first button is 0)
        self.radiobox.SetSelection(1)
        # bind mouse click to an action
        self.radiobox.Bind(wx.EVT_RADIOBOX, self.onAction)
        # create an output widget
        self.label = wx.StaticText(self, wx.ID_ANY, "" , pos=(10, 120))
        # show present selection
        self.onAction(None)

    def onAction(self, event):
        """ some action code"""
        #index = self.radiobox.GetSelection()
        #s = "You selected option " + self.options[index]
        # better ...
        s = "You selected option " + self.radiobox.GetStringSelection()
        self.label.SetLabel(s)


app = wx.App(0)
# create a MyFrame instance and show the frame
MyFrame(None, 'testing wx.RadioBox()', (300, 200)).Show()
app.MainLoop()