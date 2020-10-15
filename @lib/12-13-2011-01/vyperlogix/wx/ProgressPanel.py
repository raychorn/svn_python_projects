import wx

import math

from vyperlogix.misc import _utils

class ProgressPanel(wx.Panel):
    def __init__(self, parent, title='', gauge_size=(250, 20), log=None):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.max = 100
        self.timer = None

        self.__begin_time__ = None
        self.__start_time__ = None
	
	self.__title__ = 'Processed'
	
        self.text = wx.StaticText(self, -1, self.title, (45, 15))
        self.gauge = wx.Gauge(self, -1, self.max, (110, 30), gauge_size)
        self.textElapsedLabel = wx.StaticText(self, -1, '     Elapsed Time:', (45, 15))
        self.textElapsedTime = wx.StaticText(self, -1, '00:00:00', (45, 15))
        self.textTotalLabel = wx.StaticText(self, -1, '         Total Time:', (45, 15))
        self.textTotalTime = wx.StaticText(self, -1, '00:00:00', (45, 15))
        self.textRemainingLabel = wx.StaticText(self, -1, 'Remaining Time:', (45, 15))
        self.textRemainingTime = wx.StaticText(self, -1, '00:00:00', (45, 15))
        
        vbox = wx.BoxSizer(wx.VERTICAL)

        hboxes = []
        
        hboxes.append(wx.BoxSizer(wx.HORIZONTAL))

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        vbox2.Add(self.gauge, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
	
	hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.textElapsedLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        hbox1.Add(self.textElapsedTime, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

	hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.textTotalLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        hbox2.Add(self.textTotalTime, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

	hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.textRemainingLabel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        hbox3.Add(self.textRemainingTime, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        vbox2.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, -1)
        vbox2.Add(hbox2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, -1)
        vbox2.Add(hbox3, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, -1)
	
        vbox2.Add((-1, 1))
        hboxes[-1].Add(vbox2, 1)

        vbox.Add(hboxes[-1], 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        vbox.Add((-1, 1))

        self.SetSizer(vbox)

        vbox.Fit(self)
	
	self.restart()
	
    def restart(self):
	self.__number__ = 100
	self.__count__ = 1
        self.count = 0
    
    def run(self, msg='', max=100, isSimulated=False):
        self.max = max
	self.text.SetLabel(msg)
	self.gauge.SetRange(max)
        if (isSimulated):
            self.Bind(wx.EVT_TIMER, self.TimerHandler)
            self.timer = wx.Timer(self)
            self.timer.Start(250)
	    
    def number():
        doc = "number"
        def fget(self):
            return self.__number__
        def fset(self, number):
            self.__number__ = number
	    self.__start_time__ = None
	    self.__begin_time__ = None
        return locals()
    number = property(**number())
    
    def title():
        doc = "title"
        def fget(self):
            return self.__title__
        def fset(self, title):
            self.__title__ = title
        return locals()
    title = property(**title())

    def count():
        doc = "count"
        def fget(self):
            return self.__count__
        def fset(self, count):
            self.__count__ = count
	    _pcent = (float(self.__count__) / float(self.number))
	    pcent = math.ceil(_pcent * 100.0)
	    self.text.SetLabel('%s %3.0f%%' % (self.title,pcent))
	    self.SetGaugeValue(pcent)
	    if (self.__start_time__ is None):
		self.__start_time__ = _utils.timeSeconds()
	    if (self.__begin_time__ is None):
		self.__begin_time__ = _utils.timeSeconds()
	    time_now = _utils.timeSeconds()
	    if (self.__start_time__ is not None):
		_et = et = time_now - self.__start_time__
		s_t = _utils.secs_to_time(et)
		self.textElapsedTime.SetLabel(str(s_t))
		
		if (self.__begin_time__ is not None):
		    et = time_now - self.__begin_time__
		    s_t = _utils.secs_to_time(et)
		    self.textTotalTime.SetLabel(str(s_t))
		    
		et = (1.0 - _pcent) * _et
		s_t = _utils.secs_to_time(et)
		self.textRemainingTime.SetLabel(str(s_t))
        return locals()
    count = property(**count())
    
    def start(self):
	self.__begin_time__ = _utils.timeSeconds()

    def __del__(self):
        if (self.timer):
            self.timer.Stop()

    def SetGaugeValue(self,value):
        self.gauge.SetValue(self.count)
    
    def TimerHandler(self, event):
        self.count = self.count + 1

        if self.count >= self.max:
            self.text.SetLabel('Done %s' % (self.text.GetLabel()))
            self.timer.Stop()

        self.SetGaugeValue(self.count)
    
    def signalDone(self):
        self.text.SetLabel('Done %s' % (self.text.GetLabel()))
