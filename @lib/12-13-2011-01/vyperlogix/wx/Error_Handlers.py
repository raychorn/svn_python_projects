from vyperlogix.classes.CooperativeClass import Cooperative

import wx

class WxStderr(Cooperative):
    def __init__(self, size=(700,500)):
	self.msg = ''
	self.dlg = None
	self.textctrl = None
	self.__size__ = size
    
    def write(self, message):
	if self.dlg == None:
	    self.dlg = wx.Dialog(None, -1, 'Error', size=self.__size__,style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP|wx.CENTRE|wx.USER_ATTENTION_ERROR)
	    self.textctrl = wx.TextCtrl(self.dlg, -1, '',style=wx.TE_MULTILINE|wx.TE_READONLY)
	    border = wx.BoxSizer(wx.VERTICAL)
	    border.Add(self.textctrl, 1, wx.GROW|wx.ALL, 0)
	    self.dlg.SetSizer(border)
	    self.dlg.SetAutoLayout(True)
	    self.dlg.Layout()
	    self.dlg.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
	    self.dlg.Show(True)
	
	self.msg += message
	self.textctrl.SetValue(self.msg)
	
    def flush(self):
	# simulated for compatibility...
	pass
    
    def close(self):
	# simulated for compatibility...
	pass
    
    def OnCloseWindow(self, evt):
	self.msg = ''
	self.dlg.Destroy()
	self.dlg = None

