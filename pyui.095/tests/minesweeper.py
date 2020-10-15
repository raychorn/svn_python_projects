import time
import whrandom
import pyui
from pyui.locals import *

from pyui.desktop import getDesktop, getTheme, getRenderer

sx = 350
sy = 450


class gridSquare(pyui.widgets.Button):
    """A grid square im the mine sweeper game. this also holds the state information for the game."""
    def __init__(self, x, y, handler, game):
        pyui.widgets.Button.__init__(self,"",  handler)
        self.registerEvent(RMOUSEBUTTONDOWN, self.onMined)        
        self.x = x
        self.y = y
        self.game = game
        self.reset()
	self.grey = getRenderer().packColor( 150, 150, 50 )

    def reset(self):
        """reset the game square for a new game."""
        self.cleared = 0
        self.neighbors = -1
        self.mined = 0
        self.flagged = 0
        self.surf = None
        
    def draw(self, renderer):
        if self.cleared == 1:
            if self.neighbors > 0:
                renderer.drawText( "%d" % self.neighbors, (self.windowRect[0]+2, self.windowRect[1]+2), pyui.colors.black)
                renderer.drawText( "%d" % self.neighbors, (self.windowRect[0], self.windowRect[1]), pyui.colors.white)                
            return
        if self.status == pyui.widgets.Button.DOWN:
            getTheme().draw3DRect( self.windowRect, pyui.colors.grey, 1)
        else:
            getTheme().draw3DRect( self.windowRect, pyui.colors.white, 1)

        if self.flagged:
            renderer.drawText( "X", (self.windowRect[0], self.windowRect[1]), self.bgColor)

    def clear(self, neighbors):
        self.neighbors = neighbors
        self.cleared = 1

    def onMined(self, event):
        """handles right button flagging of mine squares"""
        if not self.hit(event.pos):        
            return 0
        if self.flagged:
            self.flagged = 0
            self.game.unflag(self.x, self.y, self.mined)
        else:
            self.game.flag(self.x, self.y, self.mined)
            self.flagged = 1
        return 1
        
class game:
    """Minesweeper game object. """
    RUNNING = 0
    LOST = 1
    WON = 2
    
    def __init__(self):
        self.gridSize = 10
        self.gameGrid = []
        self.setupGui(self.gridSize)
        self.gameSetup()
        game.status = game.RUNNING

    def setupGui(self, gridSize):
        """One-time setup of GUI objects for the game."""
        # create gui objects
        self.mainWindow = pyui.widgets.Frame(25, 15, 300, 400, "minesweeper")
        self.splitter = pyui.widgets.SplitterPanel(pyui.widgets.SplitterPanel.HORIZONTAL, pyui.widgets.SplitterPanel.PIXELS, 32)
        self.mainWindow.replacePanel(self.splitter)
        self.mainWindow.setBackImage("max.bmp")
        
        # seup top panel
        self.foundLabel = pyui.widgets.Label("000")
        self.newGameButton = pyui.widgets.Button("New", self.onNewGame)
        self.timerLabel = pyui.widgets.Label("000")
        self.topPanel = self.splitter.getFirstPanel()
        self.topPanel.setLayout(pyui.layouts.GridLayoutManager(3,1))
        self.topPanel.addChild(self.foundLabel)
        self.topPanel.addChild(self.newGameButton)
        self.topPanel.addChild(self.timerLabel)
        self.splitter.pack()

        #setup grid
        self.bottomPanel = self.splitter.getSecondPanel()
        grid = pyui.layouts.GridLayoutManager(gridSize, gridSize)
        grid.padding = 1
        self.bottomPanel.setLayout(grid)
        for y in range(0,gridSize):
            for x in range(0,gridSize):
                g = gridSquare(x,y, self.onSquare, self)
                self.bottomPanel.addChild(g)
                self.gameGrid.append(g)
        self.mainWindow.pack()

    def gameSetup(self):
        """Setup required to start  a new game."""
        self.flagged = 0      # number of squares flagged
        self.cleared = 0      # number of squares cleared
        self.found = 0        # number of mines flagged
        
        self.foundLabel.setText("00%d" % self.flagged)
        self.newGameButton.setText("New")
        
        # setup all the squares
        for square in self.gameGrid:
            square.reset()

        # lay mines!
        for n in range(0,self.gridSize):
            r = whrandom.randint(0, len(self.gameGrid)-1)
            self.gameGrid[r].mined = 1

    def onNewGame(self, button):
        self.status = game.RUNNING
        self.gameSetup()

    def onSquare(self, button):
        if self.status != game.RUNNING:
            return
        offset = button.y * self.gridSize + button.x
        if button.cleared:
            return
        if button.mined:
            self.newGameButton.setText("you lose")
            self.status = game.LOST
        else:
            self.clear(button.x, button.y)

    def getAt(self, x, y):
        if x < 0 or x >= self.gridSize:
            return 0
        if y < 0 or y >= self.gridSize:
            return 0
        offset = self.gridSize * y + x
        return self.gameGrid[offset].mined
    
    def countNeighbors(self, x, y):
        n = 0
        n = n + self.getAt(x-1, y-1)
        n = n + self.getAt(x-1, y)
        n = n + self.getAt(x-1, y+1)
        n = n + self.getAt(x+1, y-1)
        n = n + self.getAt(x+1, y)
        n = n + self.getAt(x+1, y+1)
        n = n + self.getAt(x, y-1)
        n = n + self.getAt(x, y+1)
        return n

    def clear(self, x, y):
        if x < 0 or x >= self.gridSize:
            return
        if y < 0 or y >= self.gridSize:
            return

        offset = self.gridSize * y + x
        button = self.gameGrid[offset]
        if button.cleared or button.mined or button.flagged:
            return

        n = self.countNeighbors(x, y)
        button.clear(n)
        self.cleared = self.cleared + 1
        if self.found + self.cleared == self.gridSize * self.gridSize:
            self.win()
        
        if n == 0:
            # clear all neighbors
            self.clear(x-1,y-1)
            self.clear(x-1,y)
            self.clear(x-1,y+1)
            self.clear(x+1,y-1)
            self.clear(x+1,y)
            self.clear(x+1,y+1)
            self.clear(x,y+1)
            self.clear(x,y-1)                        

    def flag(self, x, y, mined):
        self.flagged = self.flagged + 1
        self.foundLabel.setText("00%d" % self.flagged)
        if mined:
            self.found = self.found + 1
        if self.found + self.cleared == self.gridSize * self.gridSize:
            self.win()

    def unflag(self, x, y, mined):
        self.flagged = self.flagged - 1
        self.foundLabel.setText("00%d" % self.flagged)
        if mined:
            self.found = self.found - 1
        
    def win(self):
        print "You won!"
        self.newGameButton.setText("You Won!")
        self.status = game.WON

def run():
    """The main game loop."""
    done = 1
    global sx, sy
    pyui.init(sx, sy, "p3d")
    #pyui.core.setTheme(pyui.theme.uglyTheme())        
    g = game()
    while done:
        pyui.draw()
        done = pyui.update()

    pyui.quit()

if __name__ == '__main__':
    run()
