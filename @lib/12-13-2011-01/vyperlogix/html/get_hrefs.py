def get_hrefs_from_html(html):
    from vyperlogix.classes.SmartObject import SmartFuzzyObject
    from BeautifulSoup import BeautifulSoup
    hrefs = []
    soup = BeautifulSoup(html)
    for i in soup.a:
        d = SmartFuzzyObject(dict(i.parent.attrs))
        hrefs.append(d.href)
    return hrefs

