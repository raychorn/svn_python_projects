import win32con
import win32gui
import win32process

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

def get_hwnds_for_pid(pid):
  '''
  http://timgolden.me.uk/python/win32_how_do_i.html
  '''
  def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
      i, found_pid = win32process.GetWindowThreadProcessId(hwnd)
      if found_pid == pid:
        hwnds.append(hwnd)
    return True
    
  hwnds = []
  win32gui.EnumWindows(callback, hwnds)
  return hwnds

if __name__ == "__main__":
  import sys
  print >>sys.stdout, __copyright__
  print >>sys.stderr, __copyright__
  
  import subprocess
  import time
  notepad = subprocess.Popen([r"notepad.exe"])
  #
  # sleep to give the window time to appear
  #
  time.sleep(2.0)
  
  for hwnd in get_hwnds_for_pid(notepad.pid):
    print hwnd, "=>", win32gui.GetWindowText(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWMINIMIZED)
    time.sleep(2.0)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
