def sum_ints(value):
    the_sum = 0
    for i in xrange(0, value+1):
        the_sum += i
    return the_sum

print sum_ints(1)
print sum_ints(2)
print sum_ints(10)
print sum_ints(100)

def reverse_list(source):
    result = []
    k = 0
    for i in source:
        if (k == 0):
            result.append(i)
        else:
            result.insert(0, i)
        k += 1
    return result

print reverse_list([1,2,3])
print reverse_list(['a', 'b', 'c'])


def uniques(str1, str2):
    result = ''
    for s in str1:
        if (s not in result):
            result += s
    for s in str2:
        if (s not in result):
            result += s
    return result

print uniques('abbcde', 'deefgh')

