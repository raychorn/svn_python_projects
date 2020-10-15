############### captcha_dialog.py 
#!/usr/bin/env python 
# Author: Frank Wilder <frank.wil...@gmail.com> 
# License: GPLv2 
# 07/07/10 
# Python 2.5 / wxPython 2.8.0.1 
import wx 
import  wx.lib.iewin 
class NotEmptyValidator(wx.PyValidator): 
    """ validate textctrl fields """"
    def __init__(self): 
        wx.PyValidator.__init__(self) 
    def Clone(self): 
        return NotEmptyValidator() 
    def Validate(self, win): 
        textCtrl = self.GetWindow() 
        text = textCtrl.GetValue() 
        if len(text) == 0: 
            wx.MessageBox("This field cannot be empty", "Error") 
            return False 
        else: 
            return True 
    def TransferToWindow(self): 
        return True 
    def TransferFromWindow(self): 
        return True 

class CaptchaDialog (wx.Dialog): 
    def __init__(self, url, *args, **kwds): 
        wx.Dialog.__init__(self, None, -1, "Google Captcha Query") 
        self.panel_frame = wx.Panel(self, -1) 
        txt = 'Google has a problem. It thinks this program\n'\ 
              'is a a bot.\n\n'\ 
              'To get around this, you will need to type the\n'\ 
              'word displayed in the window below as a graphic\n'\ 
              'in the "Answer" field at the bottom of the screen.' 
        self.stHeader = wx.StaticText(self.panel_frame, -1, txt) 
        self.htmlWin = wx.lib.iewin.IEHtmlWindow(self, -1, size = (250,120), style = wx.NO_FULL_REPAINT_ON_RESIZE) 
        self.stAnswer = wx.StaticText(self.panel_frame, -1, "Answer: ", style=wx.ALIGN_RIGHT) 
        self.tcAnswer = wx.TextCtrl(self.panel_frame, -1, "", validator=NotEmptyValidator()) 
        self.bOkay = wx.Button(self.panel_frame, wx.ID_OK) 
        self.bCancel = wx.Button(self.panel_frame, wx.ID_CANCEL) 
        self.__set_properties() 
        self.__do_layout() 
        self.htmlWin.Navigate(url) 
    def GetCaptcha(self): 
        return self.tcAnswer.GetValue() 
    def __set_properties(self): 
        self.SetTitle("Google Captcha") 
        self.bOkay.SetDefault() 
    def __do_layout(self): 
        sizer_panel = wx.BoxSizer(wx.VERTICAL) 
        sizer_main = wx.BoxSizer(wx.VERTICAL) 
        sizer_main.Add(self.stHeader, 0, wx.ALL, 10) 
        sizer_main.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5) 
        sizer_main.Add(self.htmlWin, 1, wx.EXPAND, 0) 
        sizer_answer = wx.BoxSizer(wx.HORIZONTAL) 
        sizer_answer.Add(self.stAnswer, 0, wx.ALL, 10) 
        sizer_answer.Add(self.tcAnswer, 0, wx.ALL, 7) 
        sizer_main.Add(sizer_answer, 0, wx.EXPAND|wx.ALL, 10) 
        sizer_btns = wx.StdDialogButtonSizer() 
        sizer_btns.AddButton(self.bOkay) 
        sizer_btns.AddButton(self.bCancel) 
        sizer_btns.Realize() 
        sizer_main.Add(sizer_btns, 0, wx.EXPAND|wx.ALL, 5) 
        self.panel_frame.SetSizer(sizer_main) 
        sizer_panel.Add(self.panel_frame, 1, wx.EXPAND, 0) 
        self.SetSizer(sizer_panel) 
        sizer_panel.Fit(self) 
        #self.Layout() 

if __name__ == "__main__": 
    url = 'https://www.google.com/accounts/Captcha?ctoken='JVJLsVGwLg5' 
    val ='xxx' 
    app = wx.PySimpleApp() 
    dlg = CaptchaDialog(url) 
    if dlg.ShowModal() == wx.ID_OK: 
        val = dlg.GetCaptcha() 
    dlg.Destroy() 
    app.MainLoop() 
    print 'val =',val 
##### end captcha_dialog.py 

