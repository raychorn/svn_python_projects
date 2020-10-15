import time
import pyui
from pyui.locals import *

from pyui.desktop import getDesktop
import profile

class game:
    def __init__(self):

        # create gui objects
        self.grid = None
        self.makeWindow()
	#self.dbutton = pyui.widgets.Button("Delete!", self.onDelete)
        getDesktop().registerHandler(DIALOGCLOSED, self.onDialogClosed)

    def onDialogClosed(self, event):
        if self.d:
            print self.d.modal
            self.d.destroy()
            self.d = None
        if self.td:
            self.td.destroy()
            self.td = None
        
    def onDelete(self, button):
        if self.grid:
            self.grid.destroy()
            self.b3 = None
            self.b4 = None
            self.b5 = None
            self.b6 = None
            self.b7 = None
            self.grid = None
        else:
            self.makeWindow()

    def makeWindow(self):
        self.grid = pyui.widgets.Frame(10, 20, 400, 400, "border Layout")
        self.grid.setLayout( pyui.layouts.BorderLayoutManager() )
        self.b3 = pyui.widgets.Button("a long name", self.onButton)
        self.b4 = pyui.widgets.Button("Button 4", self.onButton)
        self.b5 = pyui.widgets.Button("Button 5", self.onButton)
        self.b6 = pyui.widgets.Button("Button 6", self.onButton)
        self.b7 = pyui.widgets.Button("Big Butt", self.onButton)

        self.b3.bgColor = (255,0,0,255)
        self.b4.bgColor = (255,0,255,255)
        self.b5.bgColor = (255,255,0,255)
        self.grid.addChild(self.b3, NORTH)
        self.grid.addChild(self.b5, WEST)
        self.grid.addChild(self.b7, CENTER)     
        self.grid.addChild(self.b6, EAST)
        self.grid.addChild(self.b4, SOUTH)
        self.grid.pack()

        self.d = pyui.dialogs.StdDialog("title", "Select the OK or the CANCEL button!!!")
        self.d.alpha = 100
        self.td = None
        self.d.doModal()
        

    def onButton(self, button):
        print "Button:", button
        self.td = testDialog()
        self.td.doModal()

    def onInfoButton(self, button):
        pass


class testDialog(pyui.dialogs.Dialog):
    """Dialog to setup options for a trade route"""
    def __init__(self):
        pyui.dialogs.Dialog.__init__(self, 200, 200, 200, 200, "Test Dialog")
        self.setLayout(pyui.layouts.BorderLayoutManager())
        self.topPanel = pyui.widgets.Panel()
        self.myLabel = pyui.widgets.Label("Number:")
        self.myAmount = pyui.widgets.Edit("00000", 8, self.onButton)
        self.button = pyui.widgets.Button("choose", self.onButton)
        self.aList = pyui.widgets.ListBox()
        self.aList.addItem("item 1", 1)
        self.aList.addItem("another item", 2)
        self.aList.addItem("last item", 3)
        self.topPanel.setLayout(pyui.layouts.GridLayoutManager(2,1))
        self.topPanel.addChild(self.myLabel)
        self.topPanel.addChild(self.myAmount)
        
        self.addChild(self.topPanel, NORTH)
        self.addChild(self.aList, CENTER)
        self.addChild(self.button, SOUTH)
        self.pack()

    def onButton(self, button):
        item = self.aList.getSelectedItem()
        if not item:
            return
        self.close()

    def close(self):
        self.topPanel = None
        self.myLabel = None
        self.button = None
        self.aList = None
        self.myAmount = None
        pyui.dialogs.Dialog.close(self)
        

def run():
    
    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)
    g = game()

    pyui.run()


if __name__ == '__main__':
    run()
