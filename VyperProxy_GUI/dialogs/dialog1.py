
# Created with FarPy GUIE v0.5.5

import wx
import wx.calendar

class MyFrame(wx.Frame):	
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, -1, 'form title', wx.DefaultPosition, (700, 500), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
		self.panel = wx.Panel(self, -1)

		self.label1 = wx.StaticText(self.panel, -1, 'HTTP 1.1 Web App URL:', (16,16), (135, 23))
		self.label1.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.txtWebAppURL = wx.TextCtrl(self.panel, -1, ' ', (168,16), size=(400, 20))
		self.txtWebAppURL.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.txtWebAppURL.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.txtWebAppURL.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label2 = wx.StaticText(self.panel, -1, 'label', (16,40), (500, 100))
		self.label2.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label2.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label3 = wx.StaticText(self.panel, -1, 'HTTP 1.1 Proxy:', (16,160), (100, 23))
		self.label3.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label3.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.txtProxyAddress = wx.TextCtrl(self.panel, -1, '127.0.0.1', (160,160), size=(55, 20))
		self.txtProxyAddress.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.txtProxyAddress.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.txtProxyAddress.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.label4 = wx.StaticText(self.panel, -1, 'Port:', (24,200), (40, 23))
		self.label4.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.label4.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.txtProxyPort = wx.TextCtrl(self.panel, -1, '8888', (80,208), size=(50, 20))
		self.txtProxyPort.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.txtProxyPort.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.txtProxyPort.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.btnStartProxy = wx.Button(self.panel, -1, 'Start Proxy', (33,275), (75, 22))
		self.btnStartProxy.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.btnStartProxy.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		self.btnStopProxy = wx.Button(self.panel, -1, 'Stop Proxy', (176,272), (75, 23))
		self.btnStopProxy.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.btnStopProxy.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		
#---------------------------------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, 'App')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

app = MyApp(True)
app.MainLoop()