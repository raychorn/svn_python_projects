import wx, threading, Queue, sys, time
from wx.lib.newevent import NewEvent

ID_BEGIN=100
wxStdOut, EVT_STDDOUT= NewEvent()
wxWorkerDone, EVT_WORKER_DONE= NewEvent()

def LongRunningProcess(lines_of_output):
    for x in range(lines_of_output):
        print "I am a line of output (hi!)...."
        time.sleep(1)

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(300, 300))
        self.requestQ = Queue.Queue() #create queues
        self.resultQ = Queue.Queue()

        #widgets
        p = wx.Panel(self)
        self.output_window = wx.TextCtrl(p, -1,
                             style=wx.TE_AUTO_SCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
        self.go = wx.Button(p, ID_BEGIN, 'Begin')
        self.output_window_timer = wx.Timer(self.output_window, -1)

        #frame sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.output_window, 10, wx.EXPAND)
        sizer.Add(self.go, 1, wx.EXPAND)
        p.SetSizer(sizer)

        #events
        wx.EVT_BUTTON(self, ID_BEGIN, self.OnBeginTest)
        self.output_window.Bind(EVT_STDDOUT, self.OnUpdateOutputWindow)
        self.output_window.Bind(wx.EVT_TIMER, self.OnProcessPendingOutputWindowEvents)
        self.Bind(EVT_WORKER_DONE, self.OnWorkerDone)

        #thread
        self.worker = Worker(self, self.requestQ, self.resultQ)

    def OnUpdateOutputWindow(self, event):
        value = event.text
        self.output_window.AppendText(value)

    def OnBeginTest(self, event):
        lines_of_output=7
        self.go.Disable()
        self.worker.beginTest(LongRunningProcess, lines_of_output)
        self.output_window_timer.Start(50)

    def OnWorkerDone(self, event):
        self.output_window_timer.Stop()
        self.go.Enable()

    def OnProcessPendingOutputWindowEvents(self, event):
        self.output_window.ProcessPendingEvents()

class Worker(threading.Thread):
    requestID = 0
    def __init__(self, parent, requestQ, resultQ, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.requestQ = requestQ
        self.resultQ = resultQ
        self.start()

    def beginTest(self, callable, *args, **kwds):
        Worker.requestID +=1
        self.requestQ.put((Worker.requestID, callable, args, kwds))
        return Worker.requestID

    def run(self):
        while True:
            requestID, callable, args, kwds = self.requestQ.get()
            self.resultQ.put((requestID, callable(*args, **kwds)))
            evt = wxWorkerDone()
            wx.PostEvent(wx.GetApp().frame, evt)

class SysOutListener:
    def write(self, string):
        sys.__stdout__.write(string)
        evt = wxStdOut(text=string)
        wx.PostEvent(wx.GetApp().frame.output_window, evt)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, -1, 'rebinding stdout')
        self.frame.Show(True)
        self.frame.Center()
        return True

#entry point
if __name__ == '__main__':
    app = MyApp(0)
    sys.stdout = SysOutListener()
    app.MainLoop()
