def rss_content(url,source_domain='',target_domain=''):
    import urllib

    from vyperlogix.rss import reader
    from vyperlogix.html import myOOHTML as oohtml
    
    from vyperlogix import misc

    try:
        rss = reader.read_feed_links(url)
    except Exception, e:
        rss = [['CANNOT ACCESS NEWS FEED :: %s' % (str(e)),url,'']]

    toks = list(urllib.splitquery(url))
    u = 'http://'+toks[0].split('http://')[-1].split('/')[0]
    if (len(source_domain) > 0) and (len(target_domain) > 0):
        u = u.replace(source_domain,target_domain)
    link = oohtml.renderAnchor(u,u)
    items = [['<h3 align="center">%s</h3>' % (link)]]

    h = oohtml.Html()
    if (misc.isList(rss)):
        try:
            ul = h.tag(oohtml.oohtml.UL)
            for item in rss:
                if (len(source_domain) > 0) and (len(target_domain) > 0):
                    item[1] = item[1].replace(source_domain,target_domain)
                rss_link = oohtml.renderAnchor('%s' % (item[1]),item[0])
                words = item[2].split()
                item[2] = ' '.join(words[0:0])
                ul._tagLI('%s<br/><small>%s</small>' % (rss_link,'<br/>'.join(item[2:])))
        except:
            h.tagTEXTAREA('ERROR: %s' % (rss),rows=10,cols=80)
    else:
        h.tagTEXTAREA('ERROR: %s' % (rss),rows=10,cols=80)
    items += [[h.toHtml()]]

    h = oohtml.Html()
    h.html_simple_table(items)
    content = h.toHtml()
    return content

