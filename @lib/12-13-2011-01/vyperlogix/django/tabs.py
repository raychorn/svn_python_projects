_navigation_menu_types = ['basictab','glowingtabs','solidblockmenu','ddcolortabs','chromemenu']

def tab_num_from_url(url,navigation_tabs):
    i = 0
    _url = '%s%s' % ('/' if (not url.startswith('/')) else '',url)
    for tab in navigation_tabs:
        if (tab[0] == _url):
            return i
        i += 1
    return -1
