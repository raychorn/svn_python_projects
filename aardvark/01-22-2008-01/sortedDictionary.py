# (IMHO) the simplest approach:
def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

# an alternative implementation, which
# happens to run a bit faster for large
# dictionaries on my machine:
def sortedDictValuesFaster(adict):
    keys = adict.keys()
    keys.sort()
    return [dict[key] for key in keys]

# a further slight speed-up on my box
# is to map a bound-method:
def sortedDictValuesFastest(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)