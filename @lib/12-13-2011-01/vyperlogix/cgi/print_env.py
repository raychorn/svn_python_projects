import sys
import re
import os
import pwd
import cgi
import socket

__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def print_env():
    print 'Content-type: text/html; charset=utf-8\n\n'

    print '<h2>Environment</h2>'
    print '<table cellpadding="1" cellspacing="1">'
    keys = os.environ.keys()
    keys.sort()
    for env in keys:
	print '<tr>'
        print '<th align="left">', env, '</th>'
        print '<td>', (os.environ[env] or "&lt;EMPTY&gt;"), '</td>'
        print '</tr>'
    print "</table>"
    print ''

    form = cgi.FieldStorage()
    print '<h2>Form Fields</h2>'
    if len(form) == 0:
        print "<p>No form fields given."
    else:
        print '<table cellpadding="1" cellspacing="1">'
        keys = form.keys()
        keys.sort()
        for var in keys:
            print '<tr>'
            print '<th align="left">', var, '</th>'
            print '<td>',
            x = form[var]
            if isinstance(type(x), list):
                x = map(getattr, x, ["value"]*len(x))
                print ", ".join(x),
            elif x.file:
                print "(filename: %s, length: %d)" % (x.filename, len(x.value)),
            else:
                x, punt, encoding = decode(x.value)
                if isinstance(x, unicode):
                    x = x.encode("utf-8")
                print x, "(encoding: %s)"% encoding
            print '</td>'
            print '</tr>'
        print '</table>'

    print '<h2>Compiled-in Python Modules</h2>'
    modules = list(sys.builtin_module_names)
    modules.sort()
    print '<p>'
    for i in range(0, len(modules), 8):
	print '   ', ", ".join(modules[i:i+8])
    print '</p>'

    print '<h2>Modules Currently Loaded</h2>'
    modules = sys.modules.keys()
    modules.sort()
    print '<p>'
    print ", ".join(modules)
    print '</p>'

    print '<h2>User Information</h2>'
    print '<table cellpadding="1" cellspacing="1">'
    print '<tr>'
    print '<th align="left">User ID</th>',
    print '<td>', os.getuid(), '</td>'
    print '</tr>'
    print '<tr>'
    print '<th align="left">Group ID</th>',
    print '<td>', os.getgid(), '</td>'
    print '</tr>'
    print '<tr>'
    print '<th align="left">Effective User ID</th>',
    print '<td>', os.geteuid(), '</td>'
    print '</tr>'
    print '<tr>'
    print '<th align="left">Effective Group ID</th>',
    print '<td>', os.getegid(), '</td>'
    print '</tr>'
    print '</table>'

    print '<h2>Machine Information</h2>'
    print '<table cellpadding="1" cellspacing="1">'
    print '<tr>'
    print '<th align="left">True Hostname</th>',
    print '<td>', socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())), '</td>'
    print '<tr>'
    print '<th align="left">Virtual Hostname</th>',
    print '<td>', socket.gethostbyaddr(socket.gethostbyname(os.environ['SERVER_NAME'])), '</td>'
    print '</tr>'
    print '</table>'
