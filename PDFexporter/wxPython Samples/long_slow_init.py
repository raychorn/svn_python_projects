import wx
import threading
import time

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
        t.start()  #calls t.run()

        return True

class MyThread(threading.Thread):
    def __init__(self, a_frame):
        threading.Thread.__init__(self)
        self.frame_obj = a_frame

    def run(self):
        result = self.long_slow_init()

        wx.CallAfter(self.frame_obj.receive_result, result)
        #CallAfter() calls the specified function with the
        #specified argument when the next pause in execution
        #occurs in this thread:

    def long_slow_init(self):
        print "starting long_slow_init()..."
        time.sleep(6)
        result = 20.5
        return result


app = MyApp()
app.MainLoop()
