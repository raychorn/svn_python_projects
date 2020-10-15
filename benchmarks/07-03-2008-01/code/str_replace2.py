def str_replace2(s,t,v):
    i = 0
    n = len(s)
    x = ''
    while (i < n):
        x += s[i] if (s[i] != t) else v
        i += 1
    return x
