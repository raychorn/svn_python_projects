from wxPython.wx import *
import shellapi, PyAppBar, win32api, win32con

class AppBarFrame(wxFrame):
 edges = (shellapi.ABE_TOP, shellapi.ABE_LEFT, shellapi.ABE_RIGHT,
shellapi.ABE_BOTTOM)

 def __init__(self):
  wxFrame.__init__(self, None, -1, "", style=wxFRAME_TOOL_WINDOW | wxSIMPLE_BORDER)
  self.SetPosition((0,0))
  self.SetSize((1024, 100))
  self.n_edge = 0
  self.IsDocked = 0
  self.hWnd = self.GetHandle()
  EVT_LEFT_DOWN(self, self.OnClick)
  EVT_RIGHT_DOWN(self, self.OnChange)
  EVT_SIZE(self, self.OnSize)
  self.Dock()
  self.Show(true)

 def OnClick(self, evt):
  print "OnClick()"
  self.UnDock()
  self.Close()

 def OnSize(self, evt):
  print "OnSize()"
  self.ReDock(evt)

 def OnChange(self, evt):
  print "OnChange()"
  self.UnDock()
  self.n_edge = (self.n_edge + 1) % 4
  self.Dock()

 def ReDock(self, evt):
  print "ReDock()"
  self.UnDock()
  self.Dock()

 def CurrEdge(self):
  result = self.edges[self.n_edge]
  if result == shellapi.ABE_BOTTOM:
   side = "Bottom"
  elif result == shellapi.ABE_LEFT:
   side = "Left"
  elif result == shellapi.ABE_RIGHT:
   side = "Right"
  elif result == shellapi.ABE_TOP:
   side = "Top"
  print "CurrEdge(): n_edge = %s -> %s" % (self.n_edge, side)
  return self.edges[self.n_edge]

 def UnDock(self):
  print "UnDocking...",
  rect = self.GetRect()
  abd = PyAppBar.AppBarData()
  abd.hWnd = self.hWnd
  abd.uEdge = self.CurrEdge()
  (abd.rc.left, abd.rc.top, abd.rc.right, abd.rc.bottom) = (rect.GetLeft(),
rect.GetTop(), rect.GetRight(), rect.GetBottom())
  PyAppBar.SHAppBarMessage(shellapi.ABM_REMOVE, abd)
  self.IsDocked = 0
  print "done"

 def Dock(self):
  print
  print "Docking...",
  rect = self.GetRect()

  abd = PyAppBar.AppBarData()
  abd.hWnd = self.hWnd
  abd.uEdge = self.CurrEdge()
  (abd.rc.left, abd.rc.top, abd.rc.right, abd.rc.bottom) = (rect.GetLeft(),
rect.GetTop(), rect.GetRight(), rect.GetBottom())
  abd.uCallbackMessage = wxEVT_SIZE

  if (PyAppBar.SHAppBarMessage(shellapi.ABM_NEW, abd) == 0):
   print "Failed to register"
   return 0

  self.AppBarQueryPos(abd)
  self.IsDocked = 1
  print "done"
  return 1

 def AppBarQueryPos(self, abd):
  print "Querying Position...",
  iHeight = 100;
  iWidth = 100;
  screenX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
  screenY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
  print "screenX, Y = %s, %s" % (screenX, screenY)

  # Copy the screen coordinates of the appbar's bounding
  # rectangle into the APPBARDATA structure.
  abd.rc.top = 0
  abd.rc.bottom = screenY
  abd.rc.left = 0
  abd.rc.right = screenX

  if (abd.uEdge == shellapi.ABE_LEFT):
   abd.rc.right = abd.rc.left + iWidth
  elif (abd.uEdge == shellapi.ABE_RIGHT):
   abd.rc.right = screenX
   abd.rc.left = abd.rc.right - iWidth
  elif (abd.uEdge == shellapi.ABE_TOP):
   abd.rc.bottom = abd.rc.top + iHeight
  elif (abd.uEdge == shellapi.ABE_BOTTOM):
   abd.rc.top = abd.rc.bottom - iHeight

  # Query the system for an approved size and position.
  print "initial abd = " + str(abd)
  PyAppBar.SHAppBarMessage(shellapi.ABM_QUERYPOS, abd)

  # Adjust the rectangle, depending on the edge to which the
  # appbar is anchored.
  if (abd.uEdge == shellapi.ABE_LEFT):
   abd.rc.right = abd.rc.left + iWidth
  elif (abd.uEdge == shellapi.ABE_RIGHT):
   abd.rc.left = abd.rc.right - iWidth
  elif (abd.uEdge == shellapi.ABE_TOP):
   abd.rc.bottom = abd.rc.top + iHeight
  elif (abd.uEdge == shellapi.ABE_BOTTOM):
   abd.rc.top = abd.rc.bottom - iHeight

  #Pass the final bounding rectangle to the system.
  print "final abd = " + str(abd)
  PyAppBar.SHAppBarMessage(shellapi.ABM_SETPOS, abd)
  self.SetDimensions(abd.rc.left, abd.rc.top, abd.rc.right - abd.rc.left, abd.rc.bottom - abd.rc.top)
  print "done"

class App(wxApp):
 def OnInit(self):
  frame = AppBarFrame()
  return true

if __name__ == '__main__':
 app = App(0)
 app.MainLoop()
