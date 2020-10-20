__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

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
import winshell

def desktop():
    return winshell.desktop()

def common_desktop():
    return winshell.desktop(1)

def application_data():
    return winshell.application_data()

def common_application_data():
    return winshell.application_data(1)

def bookmarks():
    return winshell.bookmarks()

def common_bookmarks():
    return winshell.bookmarks(1)

def start_menu():
    return winshell.start_menu()

def common_start_menu():
    return winshell.start_menu(1)

def programs():
    return winshell.programs()

def common_programs():
    return winshell.programs(1)

def startup():
    return winshell.startup()

def common_startup():
    return winshell.startup(1)

def my_documents():
    return winshell.my_documents()

def recent():
    return winshell.recent()

def sendto():
    return winshell.sendto()
