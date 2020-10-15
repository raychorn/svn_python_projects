import os, sys

import logging

from vyperlogix.misc import _utils

__vowels__ = ['a', 'e', 'i', 'o', 'u', 'y']

is_even = lambda word:(len(word) % 2) == 0

def rule_1_num(aName):
    return len([ch for ch in aName if (ch in __vowels__)])

def rule_1(num):
    return num * 1.5

def rule_2(cust_name):
    return len([ch for ch in cust_name if (ch not in __vowels__)])

def rule_2_num(aName):
    return rule_2(aName)

def callersName():
    """ get name of caller of a function """
    import sys
    return sys._getframe(2).f_code.co_name

def formattedException(details='',_callersName=None):
    _callersName = _callersName if (_callersName is not None) else callersName()
    import traceback
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    return '(' + _callersName + ') :: "' + str(details) + '". ' + info_string

def score_prods(items,custs):
    score = 0.0
    n = 0
    if (len(items) == len(custs)):
        for item in items:
            aCust = custs[n]
            chars = len(item)
            _is_even = is_even(item)
            item_rule1 = rule_1_num(item)
            cust_rule1 = rule_1_num(aCust)
            if (_is_even):
                score += rule_1(cust_rule1)
            else:
                score += rule_2(aCust)
            item_rule2 = rule_2_num(item)
            cust_rule2 = rule_2_num(aCust)
            if (item_rule1 == cust_rule1) and (item_rule2 == cust_rule2):
                score = score * 1.5
            n += 1
    else:
        logging.warning('Number of products and customers is not the same !  Are you sure you know what you are doing today ?!?')
    return score

if (__name__ == '__main__'):
    '''
    Produces:
     18.00 :: ['Jack Abraham', 'John Evans', 'Ted Dziuba'] --> ['iPad 2 - 4-pack', 'Girl Scouts Thin Mints', 'Nerf Crossbow']
     61.00 :: ['Jeffery Lebowski', 'Walter Sobchak', 'Theodore Donald Kerabatsos', 'Peter Gibbons', 'Michael Bolton', 'Samir Nagheenanajar'] --> ['Half & Half', 'Colt M1911A1', '16lb Bowling ball', 'Red Swingline Stapler', 'Printer paper', 'Vibe Magazine Subscriptions - 40 pack']

     The method for determining the number of common factors is not well defined in the Spec however if one uses the context of the Spec alone one might infer there are only two common factors when in-fact additional common factors might exist in a larger context.
    '''
    fpath = sys.argv[1] if (len(sys.argv) > 1) else None
    if (os.path.exists(fpath)):
        f_in = open(fpath,'r')
        try:
            _line = 1
            for item in f_in.readlines():
                toks = [str(s).strip() for s in item.split(';')]
                if (len(toks) == 2):
                    custs = toks[0].split(',')
                    prods = toks[-1].split(',')
                    score = score_prods(prods,custs)
                    print '%10.2f :: %s --> %s' % (score,custs,prods)
                else:
                    logging.warning('Invalid item at line %d in "%s".' % (_line,fpath))
                _line += 1
        except Exception, ex:
            logging.error(formattedException(details=ex))
        f_in.close()
    pass
