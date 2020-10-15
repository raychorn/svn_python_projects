import time

import pyui
from pyui.locals import *

class app:
    def __init__(self):

        # create gui objects
        print "Initializing"
        self.grid = pyui.widgets.Frame(10, 10, 400, 400, "grid")
        self.grid.setLayout( pyui.layouts.GridLayoutManager(3, 4) )
        
        self.b3 = pyui.widgets.Button("a long name", self.onButton)
        self.b4 = pyui.widgets.ImageButton("max.bmp", self.onButton)
        self.s = pyui.widgets.SliderBar(self.onSlide, 40, 13)
        self.d = pyui.widgets.DropDownBox(9)
        self.d.addItem("item goes here", None)
        self.d.addItem("sdklahfkjdsafh here", None)
        self.d.addItem("askjdhfkjksjdhf", None)
        for i in range(0,25):
            self.d.addItem("testing%s" % i, None)
        
        self.b7 = pyui.widgets.Button("Big Butt", self.onButton)
        #self.pic = pyui.widgets.Picture("max.bmp")
        self.l1 = pyui.widgets.Label("Label #1")
        self.l2 = pyui.widgets.Label("Label #2")
        self.l3 = pyui.widgets.Label("Another label!")
        self.fps = pyui.widgets.Label("fps 5555.....")
        
        self.grid.addChild(self.fps)
        self.grid.addChild(self.b3)
        self.grid.addChild(self.s)
        self.grid.addChild(self.b7)
        #self.grid.addChild(self.pic)
        self.grid.addChild(self.l1)
        self.grid.addChild(self.l2)
        self.grid.addChild(self.l3)
        self.grid.addChild(self.b4)
        self.grid.addChild(self.d)                
        self.grid.pack()

        newFrame = pyui.widgets.Frame(0,505, 200,100, "close me")

        pyui.desktop.getRenderer().setBackMethod(self.drawBack)
        
    def drawBack(self):
        """Called every frame to draw the background.
        """
        renderer = pyui.desktop.getRenderer()
        renderer.setup2D()
        
        renderer.clear()
        for x in range(0,10):
            renderer.drawLine(x*80,1,x*80, 600, (0,255,255,255) )

        renderer.drawRect( pyui.colors.red, (100,100,600,400) )            

        renderer.teardown2D()
        
        
    def onSlide(self, value):
        print "slider says:", value
        
    def onButton(self, button):
        print "Button:", button

    def cleanup(self):
        self.fps = None
        self.b3 = None
        self.b4 = None
        self.b5 = None
        self.b6 = None
        self.b7 = None
        #self.pic = None
        self.l1 = None
        self.l2 = None
        self.l3 = None      
        self.grid.destroy()
        self.grid = None

def run():
    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)
    #pyui.core.setTheme(pyui.greenTheme.greenTheme(pyui.core.gRenderer, 640, 480))
    g = app()

    pyui.run()

    print "done X"
    g.cleanup()
    pyui.quit()
    print "quit."



if __name__ == '__main__':
    run()
