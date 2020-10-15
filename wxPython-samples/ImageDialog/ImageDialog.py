# test the wx.lib.imagebrowser.ImageDialog()
# and display the loaded image on a scrolled window

import wx
import os
import wx.lib.imagebrowser

class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size=(600,400),
            style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        # create a srolled window to put the image on
        self.scrollw = wx.ScrolledWindow(self, wx.ID_ANY)
        self.scrollw.SetBackgroundColour('green')
        # set EnableScrolling(bool x_scrolling, bool y_scrolling)
        self.scrollw.EnableScrolling(True, True)
        # create the scroll bars, set max width and height
        max_width = 1000
        max_height = 1000
        # SetScrollbars(pixelsPerUnitX, pixelsPerUnitY, noUnitsX, noUnitsY)
        self.scrollw.SetScrollbars(20, 20, max_width/20, max_height/20)

        # create a statusbar at the bottom of the frame
        self.CreateStatusBar()

        # create the menubar at the top of the frame
        menubar = wx.MenuBar()
        # setting up the menu
        filemenu = wx.Menu()
        # alt/o is hotkey, "Open file" shows up in statusbar
        filemenu.Append(wx.ID_OPEN, "&Open","Open image file")
        filemenu.AppendSeparator()
        # alt/x is hotkey
        filemenu.Append(wx.ID_EXIT,"E&xit","Exit program")
        # add the filemenu to the menubar
        menubar.Append(filemenu,"&File")
        # add the finished menubar to the frame/window
        self.SetMenuBar(menubar)

        # bind event to an action
        self.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onOpen, id=wx.ID_OPEN)

    def onExit(self,event):
        """close the frame"""
        self.Close(True)

    def onOpen(self,event):
        """open an image file via wx.lib.imagebrowser.ImageDialog()"""
        dirname = ''
        dialog = wx.lib.imagebrowser.ImageDialog(self, dirname)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetFile()
            image = wx.Bitmap(filename)
            self.SetStatusText(filename)
            # bitmap upper left corner is in position (x, y) = (5, 5)
            wx.StaticBitmap(self.scrollw, wx.ID_ANY, image, pos=(5, 5),
                size=(image.GetWidth(), image.GetHeight()))
        dialog.Destroy()


app = wx.App(0)
# create MyFrame instance and show the frame
MyFrame(None, "Test wx.lib.imagebrowser.ImageDialog()").Show()
app.MainLoop()