import time
import os
import stat

import pyui
from pyui.locals import *

sx = 800
sy = 800


class app:
    def __init__(self):

        # create gui objects
        print "Initializing"
        self.root = "c:/"
        self.frame = pyui.widgets.Frame(10, 10, 400, 200, "Directory Path Viewer")
        self.frame.setLayout( pyui.layouts.BorderLayoutManager() )
        self.frame.registerEvent(TREENODE_SELECTED, self.onSelected)
        
        # create widgets
        self.label = pyui.widgets.Button("nothin...", None)
        self.tree = pyui.tree.Tree()
        self.tree.topNode.populated = 0

        #add nodes
        self.addDir(self.tree, self.root)
        
        self.frame.addChild(self.tree, CENTER)
        self.frame.addChild(self.label, SOUTH)
        self.frame.pack()

        self.d = pyui.dialogs.FileDialog("c:\\", self.gotit, ".*")

    def gotit(self, file):
        print "got file:", file
        
    def addDir(self, node, path):
        print "Adding path", path
        files = os.listdir(path)
        for file in files:
            print "adding:", file
            info = os.stat(path+"/"+file)
            isdir = stat.S_ISDIR(info[stat.ST_MODE])
            if isdir:
                icon = "folder.png"
            else:
                icon = "instance.png"
            newNode = pyui.tree.TreeNode(file, icon)
            newNode.populated = 0
            node.addNode( newNode )
        
    def onSelected(self, event):
        fullPath = event.node.title
        parent = event.node.parent
        while parent and parent.title:
            fullPath = parent.title + "/" + fullPath
            parent = parent.parent
        fullPath = "c:/" + fullPath            

        if event.node.populated:
            return
        
        self.label.text = fullPath
        info = os.stat(fullPath)
        isdir = stat.S_ISDIR(info[stat.ST_MODE])
        if isdir:
            self.addDir(event.node, fullPath)
            event.node.populated = 1
        


    def cleanup(self):
        self.frame = None

def run():
    done = 1
    frame = 0
    t = time.time()
    global sx, sy
    pyui.init(sx, sy, "dx" )
    g = app()
    while done:
        pyui.draw()
        now = int(time.time())
        if now != t:
            print frame
            frame = 0
            t = now
        frame = frame + 1
        done = pyui.update()        


    print "done X"
    g.cleanup()
    pyui.quit()
    print "quit."



if __name__ == '__main__':
   run()
