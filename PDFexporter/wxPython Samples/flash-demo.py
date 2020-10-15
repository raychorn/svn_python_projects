# Explore the wxPython FlashWindow component
# to play animated flash files (extension .swf)
# uses the wx.lib.pdfwin.FlashWindow class ActiveX control
# from wxPython's new wx.activex module, this allows one
# to use an ActiveX control, as if it would be a wx.Window
# embeds the ShockWave Flash control
# as far as HB knows this works only with Windows
# tested with Python25 and wxPython27 by HB
 
import wx
 
if wx.Platform == '__WXMSW__':
    from wx.lib.flashwin import FlashWindow
 
 
class MyPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, -1)
        self.pdf = None
         
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
         
        self.flash = FlashWindow(self, style=wx.SUNKEN_BORDER)
        sizer.Add(self.flash, proportion=1, flag=wx.EXPAND)
         
        btn = wx.Button(self, wx.NewId(), "Open a Flash File")
        self.Bind(wx.EVT_BUTTON, self.OnOpenFileButton, btn)
        btnSizer.Add(btn, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
         
        btn = wx.Button(self, wx.NewId(), "Open a Flash URL")
        self.Bind(wx.EVT_BUTTON, self.OnOpenURLButton, btn)
        btnSizer.Add(btn, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
         
        btnSizer.Add((50,-1), proportion=2, flag=wx.EXPAND)
        sizer.Add(btnSizer, proportion=0, flag=wx.EXPAND)
         
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
     
    def OnOpenFileButton(self, event):
        # make sure you have flash files available on drive
        dlg = wx.FileDialog(self, wildcard="*.swf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.flash.LoadMovie(0, 'file://' + dlg.GetPath())
            wx.EndBusyCursor()
        dlg.Destroy()
     
    def OnOpenURLButton(self, event):
        # you can retrieve flash files from internet too
        dlg = wx.TextEntryDialog(self, "Enter a URL of a .swf file", "Enter URL")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            # setting the movie property works too
            self.flash.movie = dlg.GetValue()
            wx.EndBusyCursor()
        dlg.Destroy()
     
 
app = wx.PySimpleApp()
# create window/frame, no parent, -1 is default ID, title, size
# change size as needed
frame = wx.Frame(None, -1, "FlashWindow", size = (500, 400))
# make instance of class, -1 is default ID
MyPanel(frame, -1)
# show frame
frame.Show(True)
# start event loop
app.MainLoop()