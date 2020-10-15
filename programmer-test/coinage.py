'''
#2
'''
__coin_types__ = {
    'penny': 0.01,
    'nickel': 0.05,
    'dime': 0.10,
    'quarter': 0.25,
    '50-cent': 0.50,
    'Suzie B.': 1.00,
}

__normalize__ = lambda val:str('%10.2f' % (float('%10.2f'%(val)))).strip()

def normalize(val):
    n = __normalize__(val)
    return '0.00' if (n == '-0.00') else n

__coin_values__ = {}

for k, v in __coin_types__.iteritems():
    __coin_values__[v] = k
    
def compare(a, b):
    result = 0
    if (a < b):
        result = -1
    elif (a > b):
        result = 1
    #print 'DEBUG: %s %s --> %s' % (a, b, result)
    return result

__coins__ = [float(k) for k in __coin_values__.keys()]
__coins__.sort(compare)

__coin_counts__ = {}

def __init__():
    for k, v in __coin_values__.iteritems():
        __coin_counts__[k] = 0

def how_much_change_do_i_use(val):
    __init__()
    v = float(val)
    coins = [c for c in __coins__]
    coins.reverse()
    i = 0
    while (1):
        c = coins[i]
        t = float(normalize(v-c))
        if t >= 0.00:
            __coin_counts__[c] = __coin_counts__[c] + 1
            v = v - c
            if (v <= 0.00):
                break
        else:
            i += 1
            if (i > len(coins)-1):
                break
    return __coin_counts__

def determine_value_of_result(result):
    the_value = 0.00
    for k, v in result.iteritems():
        the_value += k * v
    return the_value

def explain_the_result(result):
    the_explanation = []
    for k, v in result.iteritems():
        if (v > 0):
            the_explanation.append('There %s %d %s.' % ('is' if (v == 1) else 'are', v, __coin_values__[k]))
    return '\n'.join(the_explanation)

if (__name__ == '__main__'):
    __value__ = 9.99
    print 'INPUT: %s' % (__value__)
    result = how_much_change_do_i_use(__value__)
    value = determine_value_of_result(result)
    f_value = normalize(value)
    f__value__ = normalize(__value__)
    assert f_value == f__value__, 'OOPS - your logic is flawed... Doh !!!'
    print explain_the_result(result)
    print 'OUTPUT: %s' % (f_value)
