import testopt
import time
import pyui

def onbutton(self):
    print "got a button " 
    
def run():
    opts = testopt.parseCommandLine(800, 600)
    done = 1
    frame = 0
    t = time.time()
    pyui.init(*opts)
    w = pyui.widgets.Frame(50, 50, 400, 400, "clipme")
    b = pyui.widgets.Button( "A button is here", onbutton)
    w.addChild(b)
    w.pack()

    w.setBackImage("max.bmp")
    pyui.run()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
