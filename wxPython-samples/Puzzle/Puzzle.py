#!/usr/bin/python

# puzzle.py

import wx
import random

class Puzzle(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)

        images = ['images/one.jpg', 'images/two.jpg', 'images/three.jpg', 'images/four.jpg', 
		'images/five.jpg', 'images/six.jpg', 'images/seven.jpg', 'images/eight.jpg']

        self.pos = [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]

        self.sizer = wx.GridSizer(3, 3, 0, 0)

        numbers = [0, 1, 2, 3, 4, 5, 6, 7]
        random.shuffle(numbers)

        for i in numbers:
                button = wx.BitmapButton(self, i, wx.Bitmap(images[i]))
                button.Bind(wx.EVT_BUTTON, self.OnPressButton, id=button.GetId())
                self.sizer.Add(button)

        self.panel = wx.Button(self, -1, size=(112, 82))
        self.sizer.Add(self.panel)

        self.SetSizerAndFit(self.sizer)
        self.Centre()
        self.ShowModal()
        self.Destroy()

    def OnPressButton(self, event):

        button = event.GetEventObject()
        sizeX = self.panel.GetSize().x
        sizeY = self.panel.GetSize().y

        buttonX = button.GetPosition().x
        buttonY = button.GetPosition().y
        panelX = self.panel.GetPosition().x
        panelY = self.panel.GetPosition().y
        buttonPosX = buttonX / sizeX
        buttonPosY = buttonY / sizeY

        buttonIndex = self.pos[buttonPosY][buttonPosX]
        if (buttonX == panelX) and (panelY - buttonY) == sizeY:
            self.sizer.Remove(self.panel)
            self.sizer.Remove(button)
            self.sizer.Insert(buttonIndex, self.panel)
            self.sizer.Insert(buttonIndex+3, button)
            self.sizer.Layout()

        if (buttonX == panelX) and (panelY - buttonY) == -sizeY:
            self.sizer.Remove(self.panel)
            self.sizer.Remove(button)
            self.sizer.Insert(buttonIndex-3, button)
            self.sizer.Insert(buttonIndex, self.panel)
            self.sizer.Layout()

        if (buttonY == panelY) and (panelX - buttonX) == sizeX:
            self.sizer.Remove(self.panel)
            self.sizer.Remove(button)
            self.sizer.Insert(buttonIndex, self.panel)
            self.sizer.Insert(buttonIndex+1, button)
            self.sizer.Layout()

        if (buttonY == panelY) and (panelX - buttonX) == -sizeX:
            self.sizer.Remove(self.panel)
            self.sizer.Remove(button)
            self.sizer.Insert(buttonIndex-1, button)
            self.sizer.Insert(buttonIndex, self.panel)
            self.sizer.Layout()

app = wx.App()
Puzzle(None, -1, 'Puzzle')
app.MainLoop()
