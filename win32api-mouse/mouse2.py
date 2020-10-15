import win32api
import time
import math

def sleep(secs):
    time.sleep(secs)

def move_mouse():
    x = 500+math.sin(math.pi*i/100)*500
    y = 500+math.cos(i)*100
    win32api.SetCursorPos((int(x),int(y)))

def read_mouse():
    x, y = win32api.GetCursorPos()
    print x,y

count = 100
while (count):
    read_mouse()
    sleep(0.01)
    count -= 1