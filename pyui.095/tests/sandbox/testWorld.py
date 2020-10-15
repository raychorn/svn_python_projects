import time
import pyui


def onbutton(self):
    print "got a button " 
    
def run():
    done = 1
    frame = 0
    t = time.time()

    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)
    

    w = pyui.widgets.WorldWindow(50, 50, 400, 400)
    w.pack()
    
    while done:
        pyui.draw()
        done = pyui.update()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
