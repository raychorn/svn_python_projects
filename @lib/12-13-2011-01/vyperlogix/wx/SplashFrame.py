import wx
import os

from vyperlogix.misc import ObjectTypeName

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class TopFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.STAY_ON_TOP
        self.bitmapFile = kwds['bitmapFile']
        del kwds['bitmapFile']
        wx.Frame.__init__(self, *args, **kwds)

        if (ObjectTypeName.typeName(self.bitmapFile) == 'wx._core.Image'):
            self.bitmap = wx.StaticBitmap(self, -1, wx.BitmapFromImage(self.bitmapFile))
        elif (os.path.exists(self.bitmapFile)):
            self.bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(self.bitmapFile, wx.BITMAP_TYPE_ANY))
        else:
            self.bitmap = None

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        if (self.bitmap):
            self.SetSize(self.bitmap.GetSize())

    def __do_layout(self):
        # begin wxGlade: TopFrame.__do_layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        if (self.bitmap):
            self.sizer.Add(self.bitmap, 0, 0, 0)
        self.SetSizer(self.sizer)
        self.Layout()
        self.Centre()
        # end wxGlade

class SplashApp(wx.App): 
    def __init__(self, *args, **kwds):
	self.isVerbose = False
        if (kwds.has_key('isVerbose')):
	    self.isVerbose = kwds['isVerbose']
            del kwds['isVerbose']
        self.delay = -1
        if (kwds.has_key('delay')):
            delay = kwds['delay']
	    try:
		self.delay,self.min_delay,self.__delay__ = delay
	    except:
		self.delay,self.min_delay,self.__delay__ = (1000,5000,10000)
	    if (self.isVerbose):
		print '(%s) :: self.delay=%s, self.min_delay=%s, self.__delay__=%s' % (ObjectTypeName.objectSignature(self),self.delay,self.min_delay,self.__delay__)
            del kwds['delay']
        self.__callback__ = None
        if (kwds.has_key('callback')):
            self.__callback__ = kwds['callback']
            del kwds['callback']
        self.bitmapFile = ''
        if (kwds.has_key('bitmapFile')):
            self.bitmapFile = kwds['bitmapFile']
            del kwds['bitmapFile']
        wx.App.__init__(self, *args, **kwds)
        
    def OnInit(self): 
        wx.InitAllImageHandlers()
        self.frame = TopFrame(None, -1, "", bitmapFile=self.bitmapFile)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        self.frame.Center()
        self.SetTopWindow(self.frame)
        self.ID_Timer = wx.NewId()
        self.timer = wx.Timer(self, self.ID_Timer)
        wx.EVT_TIMER(self, self.ID_Timer, self.end)
        wx.EVT_LEFT_UP(self,self.mouse_action)
        wx.EVT_RIGHT_UP(self,self.mouse_action)
        wx.EVT_MIDDLE_UP(self,self.mouse_action)
        self.timer.Start(self.delay)
        return True

    def end(self, evt):
        if (ObjectTypeName.typeName(self.frame) != 'wx._core._wxPyDeadObject'):
	    self.__delay__ -= self.delay
	    self.min_delay -= self.delay
	    if (self.isVerbose):
		print '(%s) :: self.delay=%s, self.min_delay=%s, self.__delay__=%s' % (ObjectTypeName.objectSignature(self),self.delay,self.min_delay,self.__delay__)
	    bool = False
	    if (callable(self.__callback__)):
		bool = self.__callback__() and (self.min_delay <= 0)
		if (self.isVerbose):
		    print '(%s) :: bool=%s, self.min_delay=%s' % (ObjectTypeName.objectSignature(self),bool,self.min_delay)
	    if (bool) or (self.__delay__ <= 0):
		if (bool):
		    self.timer.Stop()
		    self.frame.Destroy()

    def mouse_action(self, evt): 
	if (callable(self.__callback__)):
	    return
        self.timer.Stop()
        if (ObjectTypeName.typeName(self.frame) != 'wx._core._wxPyDeadObject'):
            self.frame.Destroy()

class Splash: 
    def __init__(self, delay=(1000,5000,10000), bitmapFile='', callback=None, isVerbose=False):
        sApp = SplashApp(0,delay=delay,bitmapFile=bitmapFile,callback=callback,isVerbose=isVerbose)
        sApp.MainLoop()
