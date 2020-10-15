import wx
import wx.animate # ..\wx\animate.py

from vyperlogix.wx import AnimatedGIFPanel

app = wx.PySimpleApp()
frame = wx.Frame(None, -1, "wx.animate.GIFAnimationCtrl()", size = (500, 400))
AnimatedGIFPanel.AnimatedGIFPanel(frame, -1, filename="Z:/python projects/PDFexporter/animated_indicator.gif")
frame.Show(True)
app.MainLoop()