#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Fri Aug 15 21:29:58 2008

import wx

# begin wxGlade: extracode
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "some text")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.label_1, 0, wx.ALL|wx.EXPAND, 3)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


class GetRegisteredDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GetRegisteredDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        self.bitmap_button_1 = wx.BitmapButton(self, -1, wx.Bitmap("Z:\\python projects\\PDFexporter\\assets\\icons\\shopping-cart.gif", wx.BITMAP_TYPE_ANY))
        self.btn_close = wx.Button(self, wx.ID_CLOSE, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onRegister, self.bitmap_button_1)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.btn_close)
        # end wxGlade

    def __set_properties(self):
	import shopping_cart
	
        self.SetTitle("Get Registered")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(shopping_cart.getshopping_cartBitmap())
        self.SetIcon(_icon)

    def __do_layout(self):
        # begin wxGlade: GetRegisteredDialog.__do_layout
        sizer_1 = wx.GridSizer(2, 2, 0, 0)
        sizer_1.Add(self.bitmap_button_1, 0, wx.ALL, 3)
        sizer_1.Add(self.btn_close, 0, wx.ALL, 3)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def onClose(self, event): # wxGlade: GetRegisteredDialog.<event_handler>
        print "Event handler `onClose' not implemented"
        self.Destroy()

    def onRegister(self, event): # wxGlade: GetRegisteredDialog.<event_handler>
        print "Event handler `onRegister' not implemented"
        event.Skip()

# end of class GetRegisteredDialog


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = GetRegisteredDialog(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
