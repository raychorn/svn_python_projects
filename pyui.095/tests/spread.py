import testopt
import time
import pyui

def onChanged(x, y, value):
    print "Cell (%d,%d) Set to <%s>" % ( x, y, value)

def onInserted(x, y, value):
    print "Cell inserted (%d,%d) Set to <%s>" % ( x, y, value)
    
def run():
    opts = testopt.parseCommandLine(800, 600)
    done = 1
    frame = 0
    t = time.time()
    pyui.init(*opts)

    
    for i in range(0,4):
	w = pyui.widgets.Frame(50+i*20, 50+i*20, 400, 400, "spreadsheet")
        w.setLayout(pyui.layouts.GridLayoutManager(1,1,0))
        b = pyui.sheet.Sheet(onChanged, onInserted)
        b.setColumnTitle(3,"A very Long one")
        b.setColumnTitle(2,"Table name")
        b.setColumnTitle(1,"Something goes here....")
        w.addChild(b)
        w.pack()

    pyui.run()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
