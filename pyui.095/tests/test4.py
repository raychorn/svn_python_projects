import time
import pyui
from pyui.locals import *

class game:
    def __init__(self):

        # create gui objects
        self.flow = pyui.widgets.Frame(50,50, 400,200,"flow window")
        self.flow.alpha = 133
        self.firstButton = pyui.widgets.Button("button1", self.onButton )
        self.secondButton = pyui.widgets.Button("another button", self.onButton )
        self.fps = pyui.widgets.Label("fps 5555.....")
        
        self.flow.addChild(self.firstButton)
        self.flow.addChild(self.secondButton)
        self.flow.addChild(self.fps)
        self.flow.pack()

        popup = pyui.widgets.MenuPopup()
        popup.addItem("Popup Menu")
        popup.addItem("-")
        popup.addItem("one", self.onMenu)
        popup.addItem("two", self.onMenu)
        popup.addItem("three", self.onMenu)
        self.flow.addPopup(popup)

        menu1 = pyui.widgets.Menu("StartMenu")
        menu1.addItem("OPEN", self.onOpen)
        menu1.addItem("two", self.onMenu)
        menu1.addItem("three", self.onMenu)
        menu1.addItem("four", self.onMenu)
        menu1.addItem("five", self.onMenu)

        menu4 = pyui.widgets.Menu("end of menus")
        for i in range(0,10):
            menu4.addItem("item num %d"% i, self.onMenu)

        menu2 = pyui.widgets.Menu("test")
        menu2.addItem("foo",self.onMenu)
        menu2.addItem("hello",self.onMenu)
        menu2.addItem("-")
        menu2.addItem("go go go go go ", self.onMenu)
        menu2.addItem("this is a long one", self.onMenu, menu4)
            
        menu3 = pyui.widgets.Menu("Last")
        menu3.addItem("This is a test",self.onMenu)
        menu3.addItem("another test",self.onMenu)
        menu3.addItem("short", self.onMenu)
        menu3.addItem("this is a long one", self.onMenu, menu2)

        self.mbar = pyui.widgets.MenuBar()
        self.mbar.addMenu(menu1)
        #self.mbar.addMenu(menu2)
        self.mbar.addMenu(menu3)
        
    def onButton(self, button):
        print "button pressed"

    def onMenu(self, item):
        print "Menu item ", item.text

    def onOpen(self, menu):
        d = pyui.dialogs.FileDialog("C:/", self.onFile, ".*png")

    def onFile(self, filename):
        print "got filename:", filename
        
def run():
    import testopt
    opts = testopt.parseCommandLine(640, 480)
    pyui.init(*opts)
    g = game()
    pyui.run()


if __name__ == '__main__':
    run()
