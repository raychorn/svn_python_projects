import testopt
import time
import pyui
"""

"""

testText ="""

<HTML>

<HEAD>
  <TITLE> PyUI HTML Panel Test </TITLE>
</HEAD>

<BODY bgColor="#ffffd0" text="#000000">

<Table width=50%>
<tr> <td> test </td> <td> another cell with some text in it.</td> </tr>
</table>

<p>Menus are <i>instances of the class</i> widgets.Menu. They have menu
items added to them with the addItem() method. The addItem method
takes a title, a handler method and possibly a sub-menu. The handler <b>method will be called with the menuItem</b> instance as the argument.
The sub-menu argument can be used to add sub-menu to the menu
allowing hierarchies of menus.</p>
<hr>
<p> bottom of the page </p>

</BODY>
</HTML>
"""

def onbutton(self):
    print "got a button " 
    
def run():
    opts = testopt.parseCommandLine(1024, 768)
    done = 1
    frame = 0
    t = time.time()
    pyui.init(*opts)
    w = pyui.widgets.Frame(0,0,800,600, "HTML!")
    h = pyui.html.HTMLPanel()
    w.replacePanel(h)
    w.pack()

    #f = open('C:/ninja/Projects/pyui/website/index.html')
    #f = open('awful.html')
    #text = f.read()
    #f.close()
    #h.feed(text)
    
    h.feed(testText)

    w.resize(800,600)
    pyui.run()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
