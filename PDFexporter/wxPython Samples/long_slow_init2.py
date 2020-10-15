import wx
import os, sys, time

from vyperlogix.misc import threadpool

_q = threadpool.ThreadQueue(2,isDaemon=True)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Window")

        panel = wx.Panel(self, -1)
        button = wx.Button(panel, -1, "click me, quick!", pos=(40,40))
        self.Bind(wx.EVT_BUTTON, self.onclick)

    def onclick(self, event):
        print "button clicked"

    def receive_result(self, result):
        print "Hey, I'm done with that long, slow initialization."
        print "The result was:", result


class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)


    def OnInit(self):  #called by wx.Python
        the_frame = MyFrame()
        the_frame.Show()

        t = MyThread(the_frame)

        return True

class MyThread:
    def __init__(self, a_frame):
        self.frame_obj = a_frame
        self.result = -1

        self.long_slow_init()

    @threadpool.threadify(_q)
    def long_slow_init(self):
        print "starting long_slow_init()..."
        time.sleep(6)
        self.result = 20.5
        wx.CallAfter(self.frame_obj.receive_result, self.result)


app = MyApp()
app.MainLoop()

print 'Waiting for the Q.'
_q.join()
print 'Exiting...'
sys.exit(1)
