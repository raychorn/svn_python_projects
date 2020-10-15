"""Various utility functions used throughout the package.
"""

def booleanize(data):
    if data in (True, 1, '1', 'true', 'True', 'TRUE'):
        return True
    elif data in (False, 0, '0', 'false', 'False', 'FALSE', ''):
        return False
    else:
        return bool(data)
        #raise ValueError, "invalid boolean value %s" %data

def listify(maybe_list):
    """Ensure that input is a list, even if only a list of one item
    @param maybe_list: Item that shall join a list.
    @return: maybe_list coerced to a list 
    @note: If maybe_list is a list, leave it alone
    """
    if isinstance(maybe_list, list):
        definitely_list = maybe_list
    elif isinstance(maybe_list, (tuple, set)):
        definitely_list = list(maybe_list)
    else:
        definitely_list = list([maybe_list,])
    return definitely_list

def uniq(in_list_or_tuple):
    is_tuple = False
    if isinstance(in_list_or_tuple, tuple):
        is_tuple = True
    elif not isinstance(in_list_or_tuple, list):
        raise TypeError, "argument must be either a list or a tuple" 
    uniq_set = set(in_list_or_tuple)
    if is_tuple:
        return tuple(uniq_set)
    else:
        return list(uniq_set)
    
