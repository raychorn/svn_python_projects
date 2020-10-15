import time

import pyui
from pyui.locals import *


class app:
    def __init__(self):

        # create gui objects
        print "Initializing"

        self.frame = pyui.widgets.Frame(10, 100, 400, 400, "see my tree")
        self.frame.setLayout( pyui.layouts.BorderLayoutManager() )
        self.frame.registerEvent(TREENODE_SELECTED, self.onSelected)
        
        # create widgets
        self.label = pyui.widgets.Button("nothin...", None)
        self.tree = pyui.tree.Tree()

        #add nodes
        node1 = pyui.tree.TreeNode("Test")
        node2 = pyui.tree.TreeNode("Testing")
        node3 = pyui.tree.TreeNode("foo foo")
        node4 = pyui.tree.TreeNode("have another")
        node5 = pyui.tree.TreeNode("have another1")
        node6 = pyui.tree.TreeNode("have another2")
        node7 = pyui.tree.TreeNode("have another3")
        node8 = pyui.tree.TreeNode("last one")                        
        
        self.tree.addNode(node1)
        node1.addNode(node2)
        node1.addNode(node3)
        node1.addNode(node4)
        node3.addNode(node5)
        node3.addNode(node6)
        node3.addNode(node7)
        node7.addNode(node8)
        
        self.frame.addChild(self.tree, CENTER)
        self.frame.addChild(self.label, SOUTH)
        self.frame.pack()
        
    def onSelected(self, event):
        self.label.text = "Selected:" + event.node.title

    def cleanup(self):
        self.frame = None

def run():
    done = 1
    frame = 0
    t = time.time()

    import testopt
    opts = testopt.parseCommandLine(640, 480)
    pyui.init(*opts)
    
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
