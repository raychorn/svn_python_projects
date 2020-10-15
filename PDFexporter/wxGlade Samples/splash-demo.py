from wxPython.wx import *
from wxPython.html import *
'''This Module defines a wxPython Splash dialog with HTML rendering and many options.

SplashDialog(parent,ID,title,page,fullscreen,showok,timeout,pos,size,style)
    parent = parent wxApp
    ID = Frame ID (use -1)
    title = sring Title of window
    page = string HTML to be shown
    fullscreen = Boolean flag, if true show full screen
    showok = Boolean flag, if true Display OK button
    timeout = In mille seconds, if 0 don't timeout.
    pos = Location on screen (use wxSize)
    size = Size of inner HTML window (dialog shrinks to fit)
    style = wxWindows style
    #This dialog shows as normal but after 5 seconds it closes automatically

Run this module to see two examples - Application start and Application close.
'''

class SplashDialog(wxDialog): 
    
    def __init__(self, parent, ID, title='Splash', 
                 page='<html><body><b>Hello, world!</b></body></html>', 
                 fullscreen=False, 
                 showok=True, 
                 timeout=5000, 
                 pos=wxDefaultPosition, size=wxDefaultSize, 
                 style=wxDEFAULT_DIALOG_STYLE): 
        
        wxDialog.__init__(self, id = 1, name = '', parent = parent, 
              pos = pos, size = size, title = title)
        sizer = wxBoxSizer(wxVERTICAL)
        self.panel = wxHtmlWindow(self, -1, size = size)
        self.panel.SetPage(page)
        sizer.Add(self.panel, 1, wxEXPAND, 0)
        if showok: 
            btn = wxButton(self, wxID_OK, " OK ")
            btn.SetDefault()
            sizer.Add(btn, 0, wxEXPAND, 0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        #build the timeout event
        if timeout > 0: 
            self.ID_Timer = wxNewId()
            self.timer = wxTimer(self, self.ID_Timer)
            EVT_TIMER(self, self.ID_Timer, self.end)
            self.timer.Start(timeout)
        if fullscreen: 
            self.ShowFullScreen(true)

    def end(self, evt): 
        #This is the event handler assigned to our timer
        self.Destroy()
        
sample = '''<center><br><br>
Some content:
<pre  style="background: #EFEFEF;color: #000000; font-size: 8pt; font-weight: normal; font-style: normal; font-variant: normal;margin:0px; padding:6px; border:1px inset;  overflow:auto">        <font color="orange">def</font><font color="blue"> appClose</font>(self, evt): 
            <font color="red">#Hide the main window then bring up the splash dialog
</font>            self.frame.Show(false)
            dlg = SplashDialog(self.frame, -1, <font color="green">"Splash down!!"</font>, 
                               showok = True, 
                               fullscreen = False, 
                               timeout = 10000, 
                               size = wxSize(300, 300), 
                     style = wxDEFAULT_DIALOG_STYLE)
            dlg.ShowModal()
</pre><br>This window will not timeout</center>
<FONT SIZE=+3>
<center><a href="http://www.python.org/">>This is a link to Python's Home<</a></font><br></center>
'''
if __name__ == '__main__': 

    #an appllcation created just to show the splash dialog 
    class MyApp(wxApp): 
        def OnInit(self): 
            self.frame = wxFrame(NULL, -1, "Splash Demo")
            self.frame.Show(true)
            self.SetTopWindow(self.frame)
            #Handle the window closing event
            EVT_CLOSE(self.frame, self.appClose)
            return true
        
        def appClose(self, evt): 
            #Hide the main window then bring up the splash dialog
            self.frame.Show(false)
            dlg = SplashDialog(self.frame, -1, "Splash Down!!", 
                               showok = True, 
                               page = sample, 
                               fullscreen = True, 
                               timeout = 0, 
                               size = wxSize(300, 100), 
                     style = wxDEFAULT_DIALOG_STYLE)
            dlg.ShowModal()
            #let wxWindows do its stuff and delete things
            evt.Skip()
    #create an instance of MyApp
    app = MyApp(0)
    dlg = SplashDialog(app.frame, -1, "Splash Up!!", 
                       page = '''<center><FONT COLOR="#0000FF"><FONT SIZE=+6><br><br>Welcome</FONT></FONT></center>''', 
                       fullscreen = False, 
                       timeout = 2000, 
                       showok = False, 
                       size = wxSize(600, 100), 
             style = wxDEFAULT_DIALOG_STYLE)
    dlg.ShowModal()
    #Now service the GUI events
    app.MainLoop()
