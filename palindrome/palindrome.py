from vyperlogix import misc

def is_palindrome1(word):
    __is__ = False
    j = len(word)-1
    for i in xrange(0,len(word)):
        if (i != j) and (str(word[i]).lower() == str(word[j]).lower()):
            j -= 1
        else:
            break
    if (i == j):
        __is__ = True
    print '%s :: %s' % (misc.funcName(),word),
    return __is__

if (__name__ == '__main__'):
    words = ['Mom','Momi','Dad','Dadi','kayak','kayaks','odo']
    for word in words:
        print is_palindrome1(word)
    print '='*40
