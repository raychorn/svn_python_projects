#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# regwalker.py
# 
# Version: 1.0
# 
# Copyright (C) 2009  novacane novacane@dandies.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import _winreg as winreg
import re

def get_reg_value(key, subkey, name):

    """
    Walk the registry on a specified key und look for a subkey that matches
    a string. If a subkey is found return the value of the defined entry name.
    """
    
    values = []
    matches = []
    subkeys = []
    index = 0
    
    # Split the defined registry path.
    key_lst = [t for t in key.split("\\") if (len(t) > 0)]
    # Cut off the first listing
    # (e.g. SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall).
    key = "\\".join(key_lst[1:])
    # Construct the winreg.HKEY_* OpenKey.
    topkey = "winreg." + key_lst[0]
    
    # Open the registry.
    try:
        # EVAL converts the string to the PyHKEY object.
        hkey = winreg.OpenKey(eval(topkey), key)
    except WindowsError:
        return None

    try:
        # Run through the subkeys.
        while True:
            try:
                subs = winreg.EnumKey(hkey, index)
                # Save all subkeys to the list.
                subkeys.append(subs)
                index += 1
            # At the end of the subkeys Windows returns an error.
            # Break the loop if the error occurs.
            except WindowsError:
                break
    finally:
        # Close the key.
        winreg.CloseKey(hkey)
    
    # Find a matching subkey
    for i in subkeys:
        if re.search(subkey, i, re.I):
            # Save all matches to the list.
            matches.append(i)
    
    # Open the registry.
    for j in matches:
        try:
            _key_ = j
            if (len(key) > 0):
                _key_ = key + "\\" + j
            hkey = winreg.OpenKey(eval(topkey), _key_)
        except WindowsError:
            return None
        
        try:
            # Retrieve the value of the registry key. Regtype is an integer
            # giving the registry type for this value (optional).
            value, regtype = winreg.QueryValueEx(hkey, name)
            # Save all values to the list.
            values.append(value)
        except WindowsError:
            pass
    
    # Close the key.  
    winreg.CloseKey(hkey)
    
    # Return the list of located Registry values.
    return values

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "\n\t[*] regwalker.py 1.0 [*]"
        print "\n\tUsage: regwalker.py <key> <subkey> <name>"
        sys.exit(1)

    key = sys.argv[1]
    subkey = sys.argv[2]
    name = sys.argv[3]

    for value in get_reg_value(key, subkey, name):
        print value
