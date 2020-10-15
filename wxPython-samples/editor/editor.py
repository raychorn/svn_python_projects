# the start of one small text <strong class="highlight">editor</strong> with toolbar and image icons
# notice that the wx.TextCtrl() surface has already some advanced
# features: select text, right click to cut, copy and paste etc.

import os
import wx

class MyFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, wx.ID_ANY, title, size=(500, 300))
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)

        # statusBar at the bottom of the window
        self.CreateStatusBar()
        self.SetStatusText(" Click on the icon")

        # ToolBar at the top of the window
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.NO_BORDER)
        toolbar.SetToolBitmapSize(size=(24,24))
        toolbar.AddSimpleTool(wx.ID_OPEN, self.getBMP(wx.ART_FILE_OPEN),
            "Load", " Load a text file")
        toolbar.AddSimpleTool(wx.ID_SAVE, self.getBMP(wx.ART_FILE_SAVE),
            "Save", " Save the text file")
        toolbar.AddSimpleTool(wx.ID_ABOUT, self.getBMP(wx.ART_INFORMATION),
            "About"," About message")
        toolbar.AddSeparator()
        toolbar.AddSimpleTool(wx.ID_EXIT, self.getBMP(wx.ART_QUIT),
            "Exit"," Exit the program")
        toolbar.Realize()
        self.SetToolBar(toolbar)

        # bind the various toolbar <strong class="highlight">icon</strong> click events to some action
        self.Bind(wx.EVT_TOOL, self.onLoad, id=wx.ID_OPEN)
        self.Bind(wx.EVT_TOOL, self.onSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.onAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_TOOL, self.onExit, id=wx.ID_EXIT)

    def getBMP(self, pic_id):
        """get the bitmap image from the <strong class="highlight">wxPython</strong> art provider"""
        return wx.ArtProvider.GetBitmap(pic_id, wx.ART_TOOLBAR, wx.Size(24, 24))

    def onAbout(self, e):
        """ the about box """
        about = wx.MessageDialog( self, " A very simple text <strong class="highlight">editor</strong> \n"
            " using the <strong class="highlight">wxPython</strong> GUI toolkit", "About Simple Editor", wx.OK)
        about.ShowModal()
        about.Destroy()

    def onLoad(self, e):
        """ open text file"""
        self.dirname = ''
        mask = "Text (.txt)|*.txt|All (.*)|*.*"
        dlg = wx.FileDialog(self, "Choose a file to load",
            self.dirname, "", mask, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname,self.filename),'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def onSave(self, e):
        """ Save text file"""
        self.dirname = ''
        mask = "Text (.txt)|*.txt|All (.*)|*.*"
        dlg = wx.FileDialog(self, "Choose or create a file to save to",
            self.dirname, self.filename, mask, 
            wx.OVERWRITE_PROMPT|wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname,self.filename),'w')
            f.write(self.control.GetValue())
            f.close()
        dlg.Destroy()

    def onExit(self, e):
        self.Close(True)


app = wx.App(0)
# create instance of MyFrame and show it
MyFrame(title="A Simple Editor").Show()
app.MainLoop()