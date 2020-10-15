import dirssync_gui
from wxPython.wx import *


class DsApp(wxApp):
    def OnInit(self):
        frame=dirssync_gui.MyFrame(None,-1,"Directories Synchronizer")
        frame.Show(true)
        self.SetTopWindow(frame)
        return true



if __name__ == "__main__":
    app=DsApp(0)
    app.MainLoop()
					    
