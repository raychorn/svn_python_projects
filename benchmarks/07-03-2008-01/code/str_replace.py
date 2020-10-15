def str_replace(s,t,v):
    i = 0
    n = len(s)
    _s = [ch for ch in s]
    while (i < n):
        if (_s[i] == t):
            _s[i] = v
        i += 1
    return ''.join(_s)
