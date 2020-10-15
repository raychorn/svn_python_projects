from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

#This dialog shows as normal but after 5 seconds it closes automatically
class SplashDialog(wxDialog): 
    def __init__(self, fparent, ID, title='Splash', 
                 line1='Line 1', 
                 line2='Line 2', 
                 pos=wxDefaultPosition, size=wxDefaultSize, 
                 style=wxDEFAULT_DIALOG_STYLE): 
        wxDialog.__init__(self, id = 1, name = '', parent = fparent, 
              pos = wxPoint(413, 268), size = wxSize(416, 262), 
              title = title)
        sizer = wxBoxSizer(wxVERTICAL)
        label = wxStaticText(self, -1, line1)
        sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
        label = wxStaticText(self, -1, line2)
        sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
        btn = wxButton(self, wxID_OK, " OK ")
        btn.SetDefault()
        sizer.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        #build the timeout event
        self.ID_Timer = wxNewId()
        self.timer = wxTimer(self, self.ID_Timer)
        EVT_TIMER(self, self.ID_Timer, self.end)
        self.timer.Start(5000)

    def end(self, evt): 
        #This is the event handler assigned to our timer
        self.Destroy()

if __name__ == '__main__': 

    #an appllcation created just to show the splash dialog 
    class MyApp(wxApp): 
        def OnInit(self): 
            self.frame = wxFrame(NULL, -1, "Splash Demo")
            self.frame.Show(true)
            self.SetTopWindow(self.frame)
            
            #Handle the window closing event
            EVT_CLOSE(self.frame, self.appClose)

            dlg = SplashDialog(self.frame, -1, "Splash up!!", 
                               "Welcome to my splash demo.",
                               '',
                               size = wxSize(450, 300), 
                     style = wxDEFAULT_DIALOG_STYLE)
            dlg.ShowModal()
            return true
        
        def appClose(self, evt): 
            #Hide the main window then bring up the splash dialog
            self.frame.Show(false)
            dlg = SplashDialog(self.frame, -1, "Splash down!!", 
                               "Don't forget to mail me at\n me@mine.org!", 
                               "See more at www.python.org", 
                               size = wxSize(350, 200), 
                     style = wxDEFAULT_DIALOG_STYLE)
            dlg.ShowModal()
            #let wxWindows do its stuff and delete things
            evt.Skip()
    #create an instance of MyApp
    app = MyApp(0)
    #Now service the GUI events
    app.MainLoop()

