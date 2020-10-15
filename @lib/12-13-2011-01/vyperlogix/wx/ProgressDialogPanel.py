import wx

class ProgressDialogPanel(wx.Panel):
    def __init__(self, parent, title='Progress Dialog Title', message='', maximum=100, log=None, style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME): # wx.PD_CAN_ABORT | 
        self.log = log
        wx.Panel.__init__(self, parent, -1)
	
	self.__count = 0
	self.__message = message
	self.__maximum = maximum
	self.__keepGoing = True
	self.__skip = False

        self.dlg = wx.ProgressDialog(title, '', maximum=self.maximum, parent=self, style=style)
	self.dlg.Bind(wx.EVT_CLOSE, self.OnCloseDialog)

    def message():
        doc = "message"
        def fget(self):
            return self.__message
        def fset(self, message):
            self.__message = message
        return locals()
    message = property(**message())
    
    def count():
        doc = "count"
        def fget(self):
            return self.__count
        def fset(self, count):
            self.__count = count
        return locals()
    count = property(**count())
    
    def maximum():
        doc = "maximum"
        def fget(self):
            return self.__maximum
        def fset(self, maximum):
            self.__maximum = maximum
        return locals()
    maximum = property(**maximum())
    
    def keepGoing():
        doc = "keepGoing"
        def fget(self):
            return self.__keepGoing
        def fset(self, keepGoing):
            self.__keepGoing = keepGoing
        return locals()
    keepGoing = property(**keepGoing())
    
    def skip():
        doc = "skip"
        def fget(self):
            return self.__skip
        def fset(self, skip):
            self.__skip = skip
        return locals()
    skip = property(**skip())
    
    def update(self):
	_msg = 'Processed %d%%' % (self.count)
	try:
	    if (self.message.find('%') > -1):
		msg = self.message % (self.count)
	    else:
		msg = _msg
	except:
	    msg = _msg
	(self.keepGoing, self.skip) = self.dlg.Update(self.count,msg)
    
    def simulate(self):
        while self.keepGoing and (self.count < self.maximum):
            if count >= self.maximum / 2:
                (self.keepGoing, self.skip) = self.dlg.Update(self.count, 'count=%d, max=%d' % (self.count,self.maximum))
            else:
                (self.keepGoing, self.skip) = self.dlg.Update(self.count, 'count=%d, max=%d' % (self.count,self.maximum))
            wx.MilliSleep(250)

    def closeDialog(self):
	self.dlg.Destroy()
	self.dlg = None

    def OnCloseDialog(self, evt):
	self.closeDialog()

