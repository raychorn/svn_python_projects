# test the wx.Choice() widget and wx.lib.colourdb
# wx.Choice(parent, id, pos, size, choices, style)
# has no style options

import wx
import wx.lib.colourdb as colourdb

class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size=mysize)
        # create a panel to show the selected colour
        self.panel = wx.Panel(self, wx.ID_ANY, pos=(0,40), size=(250, 130))

        # create a sorted colour list from the wx colour data base
        colourdb.updateColourDB()
        colour_list = sorted(colourdb.getColourList())
        # create a choice widget
        self.choice = wx.Choice(self, wx.ID_ANY, choices=colour_list)
        # select item 0 (first item) in sorted colour list
        self.choice.SetSelection(0)
        # set the current frame color to the choice
        self.SetBackgroundColour(self.choice.GetStringSelection())
        # bind the checkbox events to an action
        self.choice.Bind(wx.EVT_CHOICE, self.onChoice)

    def onChoice(self, event):
        bgcolour = self.choice.GetStringSelection()
        # change colour of the panel to the selected colour ...
        self.panel.SetBackgroundColour(bgcolour)
        self.panel.Refresh()
        # show the selected color in the frame title
        self.SetTitle(bgcolour.lower())


app = wx.App(0)
# create a MyFrame instance and show
MyFrame(None, 'Select a colour', (250, 170)).Show()
app.MainLoop()