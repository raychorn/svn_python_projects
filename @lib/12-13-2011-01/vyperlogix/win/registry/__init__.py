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
from vyperlogix.win.registry import winreg

from vyperlogix.misc import ObjectTypeName
from vyperlogix.classes import SmartObject

__rootKeyName__ = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion'
__target__ = 'Program Files'

def get_program_files_registry_values(rootKeyName=__rootKeyName__,target=__target__):
    values = []
    root = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, rootKeyName, winreg.KEY.ALL_ACCESS)
    targets = SmartObject.SmartFuzzyObject(dict([(k,root.values[k]) for k in root.values if (str(root.values[k]).find(target) > -1)]))
    for k,v in targets.asDict().iteritems():
        if (ObjectTypeName.typeClassName(v).find('.winreg.REG_SZ') > -1):
            values.append(tuple([k,v]))
    return SmartObject.SmartFuzzyObject(dict(values))

