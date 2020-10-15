import xml.dom.minidom

document = """\
<command>Demo slideshow</command>
"""

def getText(nodelist):
    rc = ""
    for node in nodelist:
	if node.nodeType == node.TEXT_NODE:
	    rc = rc + node.data
    return rc

doc = xml.dom.minidom.parseString(document)

cmds = doc.getElementsByTagName("command")

print 'cmds=(%s)' % str(cmds)
for c in cmds:
    print getText(c.childNodes)
