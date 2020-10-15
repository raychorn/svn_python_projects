import os, sys

import wx
import wx.animate

class AnimatedGIFPanel(wx.Panel):
    """ AnimatedGIFPanel creates a panel, inherits wx.Panel """
    def __init__(self, parent, id, back_color="white", filename='', pos=(10, 10)):
        if (os.path.exists(filename)):
            wx.Panel.__init__(self, parent, id)
            isBackColorValid = lambda c:(c is not None) and (len(c) > 0)
            if (isBackColorValid(back_color)):
                self.SetBackgroundColour(back_color)
            ag = wx.animate.GIFAnimationCtrl(self, id, filename, pos=pos)
            if (isBackColorValid(back_color)):
                ag.GetPlayer().UseBackgroundColour(True)
            ag.Play()
        else:
            print >>sys.stderr, 'Cannot use the filename of "%s".' % (filename)
 
class AnimatedPanel(wx.Panel):
    """ AnimatedGIFPanel creates a panel, inherits wx.Panel """
    def __init__(self, parent, id, back_color="white", filename='', pos=(10, 10)):
        if (os.path.exists(filename)):
            wx.Panel.__init__(self, parent, id)
            isBackColorValid = lambda c:(c is not None) and (len(c) > 0)
            if (isBackColorValid(back_color)):
                self.SetBackgroundColour(back_color)
            ani = wx.animate.Animation(filename)
            self.ctrl = wx.animate.AnimationCtrl(self, -1, ani)
            self.ctrl.SetUseWindowBackgroundColour()
            self.ctrl.Play()
        else:
            print >>sys.stderr, 'Cannot use the filename of "%s".' % (filename)
 
