"""
Helpers for gathering login information

Author:        Kevin Shuk <surf@surfous.com>
Date:        Sep 16, 2005
Copyright:     (c) 2005, Kevin Shuk
                All Rights Reserved
"""

import base64
from getpass import getpass

def getinput(prompt="Input"):
    input = raw_input(prompt+': ')
    return input

if __name__ == "__main__":
    print
    print "Encode a password in base64\n"
    print "  NOTE - this is NOT heavy security. It merely provides an alternative"
    print "  store storing a password as plaintext in a config file."
    print "    You have been warned.\n"

    pw = getpass("Password to encode: ")
    encpw = base64.encodestring(pw)

    print "Encoded password is:\n"
    print encpw
