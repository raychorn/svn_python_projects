import wx
 
app = wx.PySimpleApp()
 
context = wx.ScreenDC()
r, b = context.GetSize()
 
# i have a second monitor left of my primary, so these value are negativ
#l, t = (-1280, -256) # coulfn't find a wx function to get these
l, t = (0, 0) # coulfn't find a wx function to get these
 
w, h = (r - l, b - t)
bitmap = wx.EmptyBitmap(w, h, -1)
 
memory = wx.MemoryDC()
memory.SelectObject(bitmap)
memory.Blit(0, 0, w, h, context, l, t)
memory.SelectObject(wx.NullBitmap)
 
#bitmap.SaveFile("screencapture.bmp", wx.BITMAP_TYPE_BMP)
#bitmap.SaveFile("screencapture.jpg", wx.BITMAP_TYPE_JPEG)
bitmap.SaveFile("screencapture.png", wx.BITMAP_TYPE_PNG)
 