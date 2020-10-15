import time
import pyui
from pyui.locals import *


class game:
    def __init__(self):

        o = open("test0.py")
        oo =o.read()
        
        # create gui objects
        self.grid = pyui.widgets.Frame(10, 100, 400, 400, "absolute")
        self.grid.setLayout( pyui.layouts.AbsoluteLayoutManager(400,400) )
        self.b3 = pyui.widgets.Button("a long name", self.onButton)
        self.entry = pyui.entry.Entry(oo)
        self.entry.resize(300,200)
        self.listbox = pyui.widgets.ListBox()
        for i in range(0,20):
            self.listbox.addItem("item %d" % i, 0)
        self.listbox.resize(120,120)
##        self.menu = pyui.widgets.MenuBarWidget()
##        for i in range(0,4):
##            m = pyui.widgets.Menu("test1")
##            m.addItem("testing")
##            m.addItem("testing")
##            m.addItem("testing")            
##            self.menu.addMenu(m)
        
        self.grid.addChild(self.b3, (330,30))
        self.grid.addChild(self.entry, (20, 20))
        self.grid.addChild(self.listbox, (0,230))
        #self.grid.addChild(self.menu, (0,0) )
        self.grid.pack()

        self.console = None
        
    def onButton(self, button):
        print "Button pressed", button
        if self.console:
            self.console.destroy()
            self.console = None
            return 1
        else:
            self.console = pyui.dialogs.Console(30,300,500,300)
            return 1

    def onInfoButton(self, button):
        pass


def run():
    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)

    g = game()
    pyui.run()


if __name__ == '__main__':
    run()
