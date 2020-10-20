import _winreg

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

def walk(top, writeable=False):
    """walk the registry starting from the key represented by
  top in the form HIVE\\key\\subkey\\..\\subkey and generating
  (key_name, key), subkey_names, values at each level.

  subkey_names are simply names of the subkeys of that key
  values are 3-tuples containing (name, data, data-type).
  See the documentation for _winreg.EnumValue for more details.
  """
    keymode = _winreg.KEY_READ
    if writeable:
        keymode |= _winreg.KEY_SET_VALUE
    if "\\" not in top: top += "\\"
    root, subkey = top.split ("\\", 1)
    try:
        key = _winreg.OpenKey (getattr (_winreg, root), subkey, 0, keymode)
    except:
        key = None

    subkeys = []
    if (key):
        i = 0
        while True:
            try:
                subkeys.append (_winreg.EnumKey (key, i))
                i += 1
            except EnvironmentError:
                break

    values = []
    if (key):
        i = 0
        while True:
            try:
                values.append (_winreg.EnumValue (key, i))
                i += 1
            except EnvironmentError:
                break

    yield (top, key), subkeys, values
    for subkey in subkeys:
        for result in walk (top.rstrip ("\\") + "\\" + subkey, writeable):
            yield result
