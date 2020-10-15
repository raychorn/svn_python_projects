import time
import wx

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# GUI Frame class that spins off the worker thread
class MainFrame(wx.Frame):
    """Class MainFrame."""
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, 'Idle Test')

        # Dumb sample frame with two buttons
        wx.Button(self, ID_START, 'Start',pos=(0,0))
        wx.Button(self, ID_STOP, 'Stop', pos=(0,50))
        self.status = wx.StaticText(self, -1, '', pos=(0,100))

        self.Bind (wx.EVT_BUTTON, self.OnStart, id=ID_START)
        self.Bind (wx.EVT_BUTTON, self.OnStop, id=ID_STOP)
        self.Bind (wx.EVT_IDLE, self.OnIdle)

        # Indicate we aren't working on it yet
        self.working = 0

    def OnStart(self, event):
        """Start Computation."""
        # Set up for processing and trigger idle event
        if not self.working:
            self.status.SetLabel('Starting Computation.')
            self.count = 0
            self.working = 1
            self.need_abort = 0

    def OnIdle(self, event):
        """Idle Handler."""
        if self.working:
            # This is where the processing takes place, one bit at a time
            if self.need_abort:
                self.status.SetLabel('Computation aborted.')
            else:
                self.count = self.count + 1
                time.sleep(1)
                s_label = self.status.GetLabel()
                self.status.SetLabel(s_label.split('.')[0]+'.%d' % (self.count))
                if self.count < 10:
                    # Still more work to do so request another event
                    event.RequestMore()
                    return
                else:
                    self.status.SetLabel('Computation completed.')

            # Reaching here is an abort or completion - end in either case
            self.working = 0

    def OnStop(self, event):
        """Stop Computation."""
        if self.working:
            self.status.SetLabel('Trying to abort computation.')
            self.need_abort = 1

class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
