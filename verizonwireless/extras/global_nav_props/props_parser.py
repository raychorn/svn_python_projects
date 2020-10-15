from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

def parse_url(url,value=None):
    from vyperlogix.classes import SmartObject
    toks = url.split('//')
    protocol = '//'.join(toks[0]) if (len(toks) == 2) else 'http://'
    _toks = toks[-1].split('/')
    dname = _toks[0]
    so = SmartObject.SmartFuzzyObject()
    so.protocol = protocol;
    so.domain = dname
    so.url = '/'.join(_toks[1:])
    if (value is not None):
        so.value = value
    return so

def parse_props_file(fname,comment_symbol='#',mode=1):
    stack = []
    d = lists.HashedLists2()
    if (mode == 2):
        dd = lists.HashedLists2()
    stack.append(d)
    dp = stack[-1]
    lines = [t.strip().split('=') for t in _utils.readFileFrom(fname).split('\n') if (len(t.strip()) > 0)]
    for l in lines:
        if (misc.__unpack__(l).startswith(comment_symbol)):
            if (len(stack) > 1):
                stack.pop()
                dp = stack[-1]
            dp[misc.__unpack__(l)] = lists.HashedLists2()
            stack.append(dp[misc.__unpack__(l)])
            dp = stack[-1]
        else:
            toks = l[-1].split(comment_symbol)
            if (len(toks) > 1):
                aKey = ''
                if (dp[aKey] == None):
                    dp[aKey] = lists.HashedLists2()
                dp = dp[aKey]
            dp[l[0]] = l[-1]
            if (mode == 2):
                aKey = l[-1].split(comment_symbol)[0].strip()
                so = parse_url(aKey)
                dd[so.domain] = (l[0],dp)
            if (len(toks) > 1):
                dp = stack[-1]
    if (mode == 2):
        return d,dd
    return d
