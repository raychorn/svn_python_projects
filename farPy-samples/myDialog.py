
# Created with FarPy GUIE v0.5.5

import wx
import wx.calendar

class MyFrame(wx.Frame):	
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, -1, 'myDialog', wx.DefaultPosition, (560, 472), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
		self.panel = wx.Panel(self, -1)

		self.button1 = wx.Button(self.panel, -1, 'Click Me !', (440,408), (75, 19))
		self.button1.SetFont(wx.Font(8.25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, 'Microsoft Sans Serif'))
		self.button1.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		
#---------------------------------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, 'App')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

app = MyApp(True)
app.MainLoop()