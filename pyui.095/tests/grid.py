import testopt
import time
import pyui
import random

from pyui.desktop import getDesktop, getTheme, getRenderer

class CalcGrid(pyui.grid.GridPanel):
    """A spreadsheet grid"""
    def __init__(self, w, h):
        pyui.grid.GridPanel.__init__(self, w, h, 0, 1)
        for x in range(0,w):
            head = chr( ord('A') + x) 
            self.setColumnName(x, head)
            print w, head
            for y in range(0,h):
                self.putCellAt( CalcCell(self), x, y)

        self.locals = {
            "cell":self.getCellValue
            }

    def getCellValue(self, cellString):
        column = cellString[0]
        column = ord(column) - ord('A')
        row = int(cellString[1:])
        print "(%d,%d)" % (column, row)
        cell = self.getCellAt( column, row)
        print cell.text
        return int(cell.text)
        

class CalcCell(pyui.widgets.Edit):
    """A cell in a spreadsheet.
    """

    def __init__(self, sheet,text=""):
        self.sheet = sheet
        pyui.widgets.Edit.__init__(self, text, 32, self.onEnter)
        self.expression = ""
        
    def onEnter(self, cell):
        print "TEXT: <%s>" % cell.text
        self.expression = cell.text
        result = self.eval(cell.text)
        print "RESULT <%s>" % result
        self.text = repr(result)
        self.setDirty(1)
        return 1

    def getFocus(self):
        self.text = self.expression
        return pyui.widgets.Edit.getFocus(self)

    def loseFocus(self):
        if self.text:
            self.expression = self.text
            self.text = repr(self.eval(self.text))
        return pyui.widgets.Edit.loseFocus(self)

    def draw(self):
        if getDesktop().focusWidget == self:
            getRenderer().drawRect(pyui.colors.black, self.windowRect)
        pyui.widgets.Edit.draw(self)

    def eval(self, str):
        return eval(str, {}, self.sheet.locals)
    
def onbutton(self):
    print "got a button " 
    
def run():
    opts = testopt.parseCommandLine(800, 600)
    done = 1
    frame = 0
    t = time.time()
    pyui.init(*opts)
    w = pyui.widgets.Frame(50, 50, 600, 450, "clipme")

    g = pyui.grid.GridPanel(6,10)

    for i in range(0,10):
        g.putCellAt( pyui.widgets.Button("button #%d" % i, None), random.randrange(0,4), random.randrange(0,5) )
        g.putCellAt( pyui.widgets.Label("label #%d" % i), random.randrange(0,4), random.randrange(5,10) )
        g.putCellAt( pyui.widgets.Edit("label #%d" % i, 12, None), random.randrange(0,4), random.randrange(10,15) )
        g.putCellAt( pyui.widgets.SliderBar(onbutton, 50, 30), random.randrange(0,4), random.randrange(15,20) )                        
        
                     
    w.replacePanel(g)

    w.pack()
    
    pyui.run()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
