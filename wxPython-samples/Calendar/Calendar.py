# explore the wx.calendar.CalendarCtrl() control
# allows for point and click date input

import wx
import wx.calendar as cal

class MyCalendar(wx.Dialog):
    """create a simple dialog window with a calendar display"""
    def __init__(self, parent, mytitle):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, mytitle)
        # use a box sizer to position controls vertically
        vbox = wx.BoxSizer(wx.VERTICAL)

        # wx.DateTime_Now() sets calendar to current date
        self.calendar = cal.CalendarCtrl(self, wx.ID_ANY, wx.DateTime_Now())
        vbox.Add(self.calendar, 0, wx.EXPAND|wx.ALL, border=20)
        # click on day
        self.calendar.Bind(cal.EVT_CALENDAR_DAY, self.onCalSelected)
        # change month
        self.calendar.Bind(cal.EVT_CALENDAR_MONTH, self.onCalSelected)
        # change year
        self.calendar.Bind(cal.EVT_CALENDAR_YEAR, self.onCalSelected)

        self.label = wx.StaticText(self, wx.ID_ANY, 'click on a day')
        vbox.Add(self.label, 0, wx.EXPAND|wx.ALL, border=20)

        button = wx.Button(self, wx.ID_ANY, 'Exit')
        vbox.Add(button, 0, wx.ALL|wx.ALIGN_CENTER, border=20)
        self.Bind(wx.EVT_BUTTON, self.onQuit, button)

        self.SetSizerAndFit(vbox)
        self.Show(True)
        self.Centre()

    def onCalSelected(self, event):
        #date = event.GetDate()
        date = self.calendar.GetDate()
        day = date.GetDay()
        # for some strange reason month starts with zero
        month = date.GetMonth() + 1
        # year is yyyy format
        year = date.GetYear()
        s1 = "%02d/%02d/%d \n" % (month, day, year)
        # or just take a slice of the first 8 characters to show mm/dd/yy
        s2 = str(date)[0:8]
        self.label.SetLabel(s1 + s2)

    def onQuit(self, event):
        self.Destroy()


app = wx.App()
MyCalendar(None, 'wx.calendar.CalendarCtrl()')
app.MainLoop()