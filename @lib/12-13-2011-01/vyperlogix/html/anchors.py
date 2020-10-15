def parse_href(href):
    toks = href.split('href=')
    if (len(toks) == 2) and (toks[0] == ''):
        return [t for t in toks[-1].split('"') if (len(t) > 0)][0]
    return href

def rewrite_anchor(_url,params='',callback=None,isDebug=False):
    from vyperlogix import misc
    from vyperlogix.misc import _utils
    _url = _url.lower()
    subject = _url
    if (_url.find('.php') > -1):
        toks2 = _url.split('"')
        toks2_3 = (len(toks2) == 3)
        if (len(toks2) == 1) or (toks2_3):
            toks3 = toks2[1 if (toks2_3) else 0].split('?')
            if (len(toks3) == 2):
                try:
                    toks4 = [tuple(t.split('=')) for t in toks3[-1].replace('&&','&').split('&')]
                    d_toks4 = dict([t for t in toks4 if (len(t) == 2)])
                    if (len(params) > 0):
                        d_toks4['params'] = _utils.parse_key_value_pairs_as_dict(params) if (misc.isString(params)) else ''
                    if (callable(callback)):
                        try:
                            if (isDebug):
                                print '%s :: %s' % (misc.funcName(),str(d_toks4))
                            href = callback(d_toks4)
                        except:
                            href = _url # do nothing if there is not a callback...
                    return href
                except Exception, details:
                    print >>sys.stderr, _utils.formattedException(details=details)
    return _url

def rewrite_anchors(subject,callback=None,isDebug=False):
    '''
    subject contains a bunch of HTML tags that may contain anchors.
    '''
    import re
    import sys
    from vyperlogix.misc import _utils
    for match in re.finditer("(?si)<A[^>]*>(.*?)</A>", subject):
        for m in re.finditer(r'(?si)\w+\s*=\s*"[^"]*"', match.group()):
            toks = m.group().split('href=')
            if (len(toks) == 2) and (toks[0] == ''):
                href = rewrite_anchor(toks[-1],callback=callback,isDebug=isDebug)
                old_href = m.group()
                if (not m.group().startswith('href=')):
                    old_href = 'href=%s' % (m.group())
                if (not href.startswith('href=')):
                    href = 'href=%s' % (href)
                subject = subject.replace(old_href,href)
        else:
            subject = subject.replace(match.group(),match.group().replace('\\"','"').replace('\\"','"').replace('%5C%22%5C%22',''))
    return subject

