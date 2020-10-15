import models

from vyperlogix.html import strip
from vyperlogix.hash import lists

letters = [chr(ch) for ch in xrange(ord('a'),ord('z')+1)] + [chr(ch) for ch in xrange(ord('A'),ord('Z')+1)]

def handle_keywords(id,content,division):
    d = lists.HashedLists()
    toks = [t for t in [s.strip() for s in strip.strip_tags(content).split()] if (len(t) > 0) and (all([ch in letters for ch in t]))]
    for t in toks:
        d[t] = t
    _keywords = models.Keywords.objects.filter(gid=id).filter(division=division)
    if (_keywords.count() > 0):
        for _keyword in _keywords:
            _keyword.delete()
    for aKeyword in d.keys():
        anItem = models.Keywords(gid=id,keyword=aKeyword,division=division)
        anItem.save()
