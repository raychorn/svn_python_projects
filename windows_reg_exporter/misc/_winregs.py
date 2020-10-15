from Registry import Registry

def rec(key, f):
    """
    Recurses across all RegistryKeys and applies the function f.

    key : A Registry.RegistryKey
    f : A function taking one argument, a Registry.RegistryKey
    returns : None
    """
    f(key)
    for subkey in key.subkeys():
        rec(subkey, f)

def print_key(key):
    """
    Print the path of a RegistryKey.

    key : A Registry.RegistryKey
    returns : None
    """
    print key.path()

f = open("NTUSER.DAT")
reg = Registry.Registry(f)
rec(reg.root(), print_key)