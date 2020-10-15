import time
import pyui
from pyui.locals import *

        
class game:
    def __init__(self):

        # create gui objects
        self.win = pyui.widgets.Frame(10, 100, 400, 400, "Tabbed Dialog test")
        self.win.setLayout(pyui.layouts.BorderLayoutManager())

        # create panels
        self.tabbed = pyui.widgets.TabbedPanel()
        self.splitter = pyui.widgets.SplitterPanel(pyui.widgets.SplitterPanel.HORIZONTAL, pyui.widgets.SplitterPanel.PERCENTAGE, 30)
        self.tabbed.addPanel("one", self.splitter)
        self.tabbed.addPanel("Two is more")
        self.tabbed.addPanel("three is all")
        self.tabbed.resize(400,400)

        # create widgets
        self.b1 = pyui.widgets.Button("One button", self.button)
        self.b2 = pyui.widgets.Button("Two button", self.button)
        self.listbox = pyui.widgets.ListBox()
        self.listbox.resize(180,30)
        for i in range(0,24):
            self.listbox.addItem("item number %d" % i, 0)

        # setup splitter panels
        self.splitter.getSecondPanel().setLayout(pyui.layouts.GridLayoutManager(2,1))
        self.splitter.getFirstPanel().setLayout(pyui.layouts.GridLayoutManager(1,1))
        self.splitter.getFirstPanel().addChild(self.listbox)
        self.splitter.getSecondPanel().addChild(self.b2)
        self.splitter.getSecondPanel().addChild(self.b1)
        self.splitter.pack()

        # add widgets to tabs
        two = self.tabbed.getPanel(1)
        two.setLayout(pyui.layouts.GridLayoutManager(2,2))
        l1 = pyui.widgets.Label("Testasd")
        l2 = pyui.widgets.Label("Tes234")
        l3 = pyui.widgets.Label("Tes32413245")
        l4 = pyui.widgets.Label("Testcxvb vc")
        two.addChild(l1)        
        two.addChild(l2)
        two.addChild(l3)
        two.addChild(l4)
        two.pack()
        three = self.tabbed.getPanel(2)
        three.setLayout(pyui.layouts.GridLayoutManager(1,1))
        pic = pyui.widgets.Picture("max.bmp")
        pic.setRotation(45)
        three.addChild(pic)
        three.pack()

        # put panels in the window.
        self.win.replacePanel(self.tabbed)
        self.win.pack()

    def button(self, button):
        print "Button", button
        
def run():
    done = 1
    frame = 0
    t = time.time()

    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)
    
    g = game()
    pyui.run()


if __name__ == '__main__':
    run()
