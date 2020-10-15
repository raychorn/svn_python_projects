import htmllib
import urllib
import formatter
import sys
import time
import os
import string

import pyui
from pyui.locals import *


class app:
    def __init__(self):

        # create gui objects
        print "Initializing"
        self.frame = pyui.widgets.Frame(10, 10, 700, 600, "URL Link Viewer")
        self.frame.setLayout( pyui.layouts.BorderLayoutManager() )
        self.frame.registerEvent(TREENODE_SELECTED, self.onSelected)
        
        # create widgets
        self.label = pyui.widgets.Button("nothin...", self.onButton)
        self.tree = pyui.tree.Tree()
        self.tree.topNode.populated = 0

        
        #add nodes
        newNode = pyui.tree.TreeNode("http://www.sourceforge.net/")
        newNode.urlType = "href"        
        self.tree.addNode(newNode)
        self.frame.addChild(self.tree, CENTER)
        self.frame.addChild(self.label, SOUTH)
        self.frame.pack()

    def addURL(self, node, address):
        print "Openning URL:", address
        p = parser()
        try:
            f = urllib.urlopen(address)
            data = f.read()
            f.close()
        except IOError, e:
            print "Error: <%s> not found." % address
            return
        p.feed(data)
        node.titles = {}
        for link in p.links:
            print link
            title = link[1]
            if not title[0:4] == 'http':
                pos = string.rfind(address, "/")
                title = address[0:pos] + "/" + title
                if title == address:
                    return
            if node.titles.has_key(title):
                continue
            newNode = pyui.tree.TreeNode(title, link[0] + ".bmp")
            newNode.urlType = link[0]
            node.addNode(newNode)
            node.titles[title] = 1
        
    def onSelected(self, event):
        url = event.node.title
        if event.node.urlType == "href":
            self.addURL(event.node, url)
        self.label.text = url

    def onButton(self, button):
        os.system('explorer "%s"' % self.label.text)
        
    def cleanup(self):
        self.frame = None

class parser(htmllib.HTMLParser):
    """Parses the links from a page."""
    def __init__(self):
        abs_formatter = formatter.NullFormatter()
        htmllib.HTMLParser.__init__(self, abs_formatter)
        self.links = []

    def start_a(self, data):
        self.links.append(data[0])

    def start_img(self, data):
        self.links.append(data[0])

def run():
    done = 1
    frame = 0
    t = time.time()
    
    import testopt
    opts = testopt.parseCommandLine(800, 600)
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
