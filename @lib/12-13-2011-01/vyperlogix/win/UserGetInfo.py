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
import win32net

def UserGetInfo():
    import win32api
    import win32netcon
    
    dc = win32net.NetServerEnum(None,100,win32netcon.SV_TYPE_DOMAIN_CTRL)
    user = win32api.GetUserName()
    if dc[0]:
        dcname = dc[0][0]['name']
        return win32net.NetUserGetInfo("\\\\"+dcname,user,1)
    else:
        return win32net.NetUserGetInfo(None,user,1)
    
if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    print UserGetInfo()
    