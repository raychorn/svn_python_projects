"""
Various utility functions used throughout the package.
"""

def booleanize(data):
    if data in (True, 1, '1', 'true'):
        return True
    elif data in (False, 0, '0', 'false', ''):
        return False
    else:
        raise ValueError, "invalid boolean value %s" %data


def listify(maybe_list):
    """
    Ensure that input is a list, even if only a list of one item
    @maybeList: Item that shall join a list. If Item is a list, leave it alone
    """
    definitely_list = []
    if isinstance(maybe_list, tuple):
        # maybe_list is a tuple
        definitely_list = list(maybe_list)
    elif not isinstance(maybe_list, list):
        # maybe_list is a scalar of some non-list type
        definitely_list = list([maybe_list,])
    else:
        #maybe_list is already a list
        definitely_list = maybe_list
        pass

    return definitely_list


def uniq(in_list):
    uniq_dict = {}
    for item in in_list:
        uniq_dict[item] = None

    return uniq_dict.keys()

    
