import time
import pyui
from pyui.locals import *

class app:
	def __init__(self):

		# create gui objects
		menu1 = pyui.widgets.Menu("Layouts")
		menu1.addItem("Flow", self.onFlowLayout)
		menu1.addItem("Grid", self.onGridLayout)
		menu1.addItem("Border", self.onBorderLayout)
		menu1.addItem("Absolute", self.onAbsoluteLayout)
                menu1.addItem("Table", self.onTableLayout)

		self.mbar = pyui.widgets.MenuBar()
		self.mbar.addMenu(menu1)

		# window slots
		self.flow = None
		self.grid = None
		self.border = None
		self.absolute = None

	def onClose(self, button):
		if self.flow:
			self.flow.destroy()
			self.flow = None
		if self.grid:
			self.grid.destroy()
			self.grid = None
		if self.border:
			self.border.destroy()
			self.border = None
		if self.absolute:
			self.absolute.destroy()
			self.absolute = None
		return 1
	
	def onButton(self, button):
		print "Button pressed", button
		return 1
	
	def onFlowLayout(self, event):
		self.flow = pyui.widgets.Frame(100,100,450,200,"Flow Layout")
		self.flow.addChild( pyui.widgets.Button("Button one", self.onButton) )
		self.flow.addChild( pyui.widgets.Button("Button two", self.onButton) )
		self.flow.addChild( pyui.widgets.Button("Button three", self.onButton) )
		self.flow.addChild( pyui.widgets.Button("Button four", self.onButton) )
		self.flow.addChild( pyui.widgets.Button("Exit", self.onClose) )
		self.flow.pack()

	def onGridLayout(self, event):
		self.grid = pyui.widgets.Frame(100,100,450,200,"Grid Layout")
		self.grid.setLayout(pyui.layouts.GridLayoutManager(3, 3))
		self.grid.addChild( pyui.widgets.Button("Button one", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button two", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button three", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button four", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button five", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button six", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button seven", self.onButton) )
		self.grid.addChild( pyui.widgets.Button("Button eight", self.onButton) )		
		self.grid.addChild( pyui.widgets.Button("Exit", self.onClose) )
		self.grid.pack()

	def onBorderLayout(self, event):
		self.border = pyui.widgets.Frame(100,100,450,200,"Border Layout")
		self.border.setLayout(pyui.layouts.BorderLayoutManager())
		self.border.addChild( pyui.widgets.Button("Button one", self.onButton), NORTH )
		self.border.addChild( pyui.widgets.Button("Button two", self.onButton), SOUTH )
		self.border.addChild( pyui.widgets.Button("Button four", self.onButton), WEST )
		self.border.addChild( pyui.widgets.Button("Exit", self.onClose), CENTER )
		self.border.addChild( pyui.widgets.Button("Button three", self.onButton), EAST )        
		self.border.pack()
	

	def onAbsoluteLayout(self, event):
		self.absolute = pyui.widgets.Frame(100,100,450,400,"Absolute Layout")
		self.absolute.setLayout(pyui.layouts.AbsoluteLayoutManager())
		self.absolute.addChild( pyui.widgets.Button("Button one", self.onButton), (10,10) )
		self.absolute.addChild( pyui.widgets.Button("Button two", self.onButton), (10, 50) )
		self.absolute.addChild( pyui.widgets.Button("Button three", self.onButton), (80, 10) )
		self.absolute.addChild( pyui.widgets.Button("Button seven", self.onButton), (80, 50) )
		self.absolute.addChild( pyui.widgets.Button("Exit", self.onClose), (80, 80) )
		self.absolute.pack()

        def onTableLayout(self, event):
                self.table = pyui.widgets.Frame(100,100,450,400, "Table layout")
                self.table.setLayout(pyui.layouts.TableLayoutManager(10, 10 ))
                self.table.addChild( pyui.widgets.Button("Button one", self.onButton), (2, 2, 2, 3) )
                self.table.addChild( pyui.widgets.Button("Button two", self.onButton), (4, 0, 1, 5) )
                self.table.addChild( pyui.widgets.Button("Button three", self.onButton), (7, 2, 2, 7) )
                self.table.addChild( pyui.widgets.Button("Button four", self.onButton), (0, 6, 1, 1) )
                self.table.addChild( pyui.widgets.Button("Button five", self.onButton), (1, 6, 1, 1) )
                self.table.addChild( pyui.widgets.Button("Button six", self.onButton), (0, 9, 10, 1) )                
                self.table.addChild( pyui.widgets.Button("Exit", self.onClose), (1, 7, 1, 1) )                
                self.table.pack()

def run():
    done = 1

    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)
    g = app()
    pyui.run()

    
if __name__ == '__main__':
	run()
