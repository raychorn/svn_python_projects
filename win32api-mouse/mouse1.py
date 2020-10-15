import win32api
import time
import math

def sleep():
    time.sleep(.01)

def move_mouse():
    x = 500+math.sin(math.pi*i/100)*500
    y = 500+math.cos(i)*100
    win32api.SetCursorPos((int(x),int(y)))

x = [i for i in xrange(0,500)]
for i in x:
    move_mouse()
    sleep()
