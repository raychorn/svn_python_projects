list2d = [[1,2,3],[4,5,6], [7], [8,9]]
list2d1 = [[1,2,[2.1,2.2,2.3]],[4,5,6], [7], [8,9]]
list2d2 = [['1','2',['2.1','2.2',['2.3.1', '2.3.2', '2.3.3']]],['4','5','6'], ['7'], ['8','9']]
list2d3 = [['1','2',['2.1','2.2', '2.3',['2.3.1', '2.3.2', '2.3.3', ['2.3.3.1', '2.3.3.2', '2.3.3.3']]]],['4','5','6'], ['7'], ['8','9']]

def flatten_using_recursion(list_of_lists, flattened=[]):
    for sublist in list_of_lists:
        if (isinstance(sublist, list)):
            for val in sublist:
                if (isinstance(val, list)):
                    flatten_using_recursion(val, flattened)
                else:
                    flattened.append(val)
        else:
            flattened.append(sublist)


def flatten_using_iteration(list_of_lists, flattened=[]):
    for sublist in list_of_lists:
        if (isinstance(sublist, list)):
            for val in sublist:
                if (isinstance(val, list)):
                    n = 0
                    stack = []
                    while (n < len(val)):
                        item = val[n]
                        if (isinstance(item, list)):
                            stack.append(tuple([val,n]))
                            n = -1
                            val = item
                        else:
                            flattened.append(item)
                        if (n >= len(val)):
                            if (len(stack) > 0):
                                item = stack.pop()
                                val = item[0]
                                n = item[-1]
                                n += 1
                        n += 1
                else:
                    flattened.append(val)
        else:
            flattened.append(sublist)


__flatt__ = []
flatten_using_recursion(list2d, __flatt__)
print __flatt__

__flatt__ = []
flatten_using_recursion(list2d1, __flatt__)
print __flatt__

__flatt__ = []
flatten_using_recursion(list2d2, __flatt__)
print __flatt__

__flatt__ = []
flatten_using_recursion(list2d3, __flatt__)
print __flatt__

__flatt__ = []
flatten_using_iteration(list2d3, __flatt__)
print __flatt__
