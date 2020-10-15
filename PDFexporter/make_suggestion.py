
# Created with FarPy GUIE v0.5.5

import os,sys
import wx
import wx.calendar
from vyperlogix.wx import AnimatedGIFPanel

class MyFrame(wx.Frame):	
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, 'Please Send Feedback', wx.DefaultPosition, (700, 500), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | 0 | 0 | 0)
        self.panel = wx.Panel(self, -1)

	import help
	self.SetIcon(wx.IconFromBitmap(help.gethelpBitmap()))

	self.label1 = wx.StaticText(self.panel, -1, 'Summary:', (8,5), (100, 17))
        self.label1.SetFont(wx.Font(10.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.textSummary = wx.TextCtrl(self.panel, -1, '', (8,30), size=(670, 23))
        self.textSummary.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.textSummary.SetFont(wx.Font(10.75, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.textSummary.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.label2 = wx.StaticText(self.panel, -1, 'Details:', (8,60), (100, 17))
        self.label2.SetFont(wx.Font(10.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.label2.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.textDetails = wx.TextCtrl(self.panel, -1, "", (8,85), size=(670, 285), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.textDetails.SetInsertionPoint(0)
        
        self.textDetails.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.textDetails.SetFont(wx.Font(10.75, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.textDetails.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.label3 = wx.StaticText(self.panel, -1, 'If you want us to respond, kindly provide your return valid email address:', (8,375), (100, 17))
        self.label3.SetFont(wx.Font(10.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.label3.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.textEmailAddress = wx.TextCtrl(self.panel, -1, '', (8,400), size=(670, 23))
        self.textEmailAddress.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.textEmailAddress.SetFont(wx.Font(10.75, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.textEmailAddress.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

        self.btnSubmit = wx.Button(self.panel, -1, 'Submit Now', (256,440), (100, 23))
        self.btnSubmit.SetFont(wx.Font(9.75, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.btnSubmit.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

	self.activity_indicator = AnimatedGIFPanel.AnimatedGIFPanel(self.panel, -1, filename=os.sep.join([os.path.abspath('.'),'animated_indicator.gif']), pos=(350,440))
	self.activity_indicator.Show(True)

	self.btnCancel = wx.Button(self.panel, -1, 'Close', (578,442), (93, 19))
        self.btnCancel.SetFont(wx.Font(9.75, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Verdana'))
        self.btnCancel.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

if (__name__ == '__main__'):
    #---------------------------------------------------------------------------
    class MyApp(wx.App):
        def OnInit(self):
            frame = MyFrame(None, 'App')
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    
    app = MyApp(True)
    app.MainLoop()
