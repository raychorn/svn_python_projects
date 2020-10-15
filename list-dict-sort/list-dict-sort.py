if (__name__ == '__main__'):
    lst = [{'a':3},{'a':2},{'a':1}]

    lst.sort(lambda a,b:-1 if (a.get('a',0) < b.get('a',0)) else 1 if (a.get('a',0) > b.get('a',0)) else 0)
    
    print '='*40
    for item in lst:
        print item
    print '='*40

        