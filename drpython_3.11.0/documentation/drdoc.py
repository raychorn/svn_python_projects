#!/usr/bin/python

#By Dan, GPL, etc.

#*****************************************************************************
#*You need to have docutils and SilverCity installed for this script to work.*
#*****************************************************************************

import os, sys

def DoDoc(title):
    print 'Processing:', title, '...'
    
    cwd = os.getcwd()
    
    fname = os.path.join(cwd, title + '.html')
    
    if title == 'gpl':
        os.system('pyrst2html.py --output-encoding=ascii %s.txt %s.html' % (title, title))
        
        f = file(fname, 'rb')
        text = f.read()
        f.close()
        
        text = text.replace('charset=ascii', '').replace('encoding="ascii"', '')
        text = text.replace('<h1', '<b><h3').replace('</h1>', '</h3></b>').replace('<h2', '<h3').replace('</h2>', '</h3>')
        text = text.replace('<div', '<br><div')
        
        f = file(fname, 'wb')
        f.write(text)
        f.close()
    else:
        os.system('pyrst2html.py %s.txt %s.html' % (title, title))
        
if len(sys.argv) > 1:
    DoDoc(sys.argv[1])
else:
    DoDoc('credits')
    DoDoc('gpl')
    DoDoc('drscript')
    DoDoc('help')
    DoDoc('northstar')
    DoDoc('plugins')
    DoDoc('preferences')
    DoDoc('thanks')
