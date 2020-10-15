
import wx


# Show how to derive a custom wxLog class

class My_Log(wx.PyLog):
    def __init__(self, textCtrl, log_time=0):
        wx.PyLog.__init__(self)
        self.tc = textCtrl
        self.log_time = log_time
        
        
    def DoLogString(self, message, time_stamp):
        #print message, time_stamp
        #if self.log_time:
        #    message = time.strftime("%X", time.localtime(time_stamp)) + \
        #              ": " + message
        if self.tc:
            self.tc.AppendText(message + '\n')
            
