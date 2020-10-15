def str_replace2(s,t,v):
    i = 0
    n = len(s)
    x = ''
    while (i < n):
        if (s[i] != t):
            x += s[i]
        else:
            x += v
        i += 1
    return x
