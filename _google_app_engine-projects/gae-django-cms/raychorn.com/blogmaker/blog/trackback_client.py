''' Copyright (c) 2006-2007, PreFab Software Inc. '''


''' Utilities for autodiscovery and sending of trackback pings '''

import re, urllib, urllib2

errorRe = re.compile(r'<error>(\d+)</error>')
messageRe = re.compile(r'<message>(.*)</message>')

class TrackbackError(Exception): pass

def postTrackback(trackbackUrl, sourceUrl, title = None, excerpt = None, siteName = None):
    """Implements a trackback ping.  This method throws exceptions based upon
    the error returned from the trackback server, unless it is the successful
    error code '0'.
    """

    mapping = {"url": sourceUrl}
    if title:
        if isinstance(title, unicode):
            title = title.encode('utf-8')
        mapping["title"] = title
    if excerpt:
        if isinstance(excerpt, unicode):
            excerpt = excerpt.encode('utf-8')
        mapping["excerpt"] = excerpt
        
    if siteName:
        mapping["blog_name"] = siteName
    params = urllib.urlencode(mapping)

    request = urllib2.Request(trackbackUrl, params)
    request.add_header('Content-type',
    'application/x-www-form-urlencoded; charset=utf-8')
    
    response = urllib2.urlopen(request)
    data = response.read()
    response.close()
    
    m = errorRe.search(data)
    if not m:
        raise TrackbackError('Unrecognized response:\n' + data[:500])
    
    code = int(m.group(1))
    if code == 0:
        return
    
    m = messageRe.search(data)
    if not m:
        raise TrackbackError('Error %s' % code)
    
    raise TrackbackError('Error %s: %s' % (code, m.group(1)))


rdfRe = re.compile(r'<rdf:Description.*?/>', re.DOTALL)
rdfIdRe = re.compile(r'''dc:identifier=['"](.*?)['"]''')
rdfTbRe = re.compile(r'''trackback:ping=['"](.*?)['"]''')

linkTbRe = re.compile(r'''<(link|a) [^>]*rel=['"]trackback['"].*?>''', re.IGNORECASE)
aRe = re.compile(r'''<a [^>]*?>''', re.IGNORECASE)
hrefRe = re.compile(r'''href=['"](.*?)['"]''')

# This attempts to be a reasonably accurate regex for recognizing URLs that end in trackback
bareLinkRe = re.compile(r'''https?://[^<>"#%\s]+trackback[/]?''', re.IGNORECASE)

def discover(url, data=None):
    ''' Try to find a trackback at the given URL using RDF autodiscovery
        and other methods. Returns the trackback or None, and the raw page data. '''
    if data is None:
        response = urllib2.urlopen(url)
        data = response.read()
        response.close()

    # Try RDF autodiscovery
    # A page can have multiple RDF blocks; search for the one containing url
    for rdf in rdfRe.findall(data):
        # Check the identifier
        m = rdfIdRe.search(rdf)
        if not m: continue
        if m.group(1) != url:
            continue
        
        # Find the trackback
        m = rdfTbRe.search(rdf)
        if not m:
            continue
        return m.group(1), data
    
    # Any of the following can return find multiple links
    # Require that there be only one unique link
    
    # Look for a <link> or <a> with rel="trackback" and extract the href
    links = set()
    for linkMatch in linkTbRe.finditer(data):
        link = linkMatch.group(0)
        m = hrefRe.search(link)
        if m:
            links.add(m.group(1))
    if len(links) == 1:
        return links.pop(), data
        
    # Look for an <a> with "trackback" or "haloscan.com" in the href
    links = set()
    for aMatch in aRe.finditer(data):
        a = aMatch.group(0)
        m = hrefRe.search(a)
        if m:
            href = m.group(1)
            if 'trackback' in href.lower() or 'haloscan.com' in href.lower():
                links.add(href)
    if len(links) == 1:
        return links.pop(), data
        
    # Look for a trackback url in plain text
    links = set()
    for aMatch in bareLinkRe.finditer(data):
        href = aMatch.group(0)
        links.add(href)
    if len(links) == 1:
        return links.pop(), data
        
    return None, data
