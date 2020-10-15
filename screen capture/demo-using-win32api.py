import win32gui,  win32ui,  win32con, win32api
 
hwnd = win32gui.GetDesktopWindow()
print hwnd
 
# you can use this to capture only a specific window
#l, t, r, b = win32gui.GetWindowRect(hwnd)
#w = r - l
#h = b - t
 
# get complete virtual screen including all monitors
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
r = l + w
b = t + h
 
print l, t, r, b, ' -> ', w, h
 
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
 
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(saveBitMap)
saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)
saveBitMap.SaveBitmapFile(saveDC,  'screencapture.bmp')
 