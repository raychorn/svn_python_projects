''' Copyright (c) 2006-2007, PreFab Software Inc. '''


import htmlentitydefs, re, logging, os
from django.conf import settings
        
#: List of (shortcut, expansion)
_shortcuts = [
    ('%portal%', settings.SITE_ROOT),
    ('%blog%', settings.BLOG_ROOT),
    ('%emphasis-added%', '<span class="note">(emphasis added)</span>'),
    ('%info%', '<img src="%smedia/public/images/info_small.gif" border="0" />' % settings.SITE_ROOT),
    ('%link-out%', '<img src="%smedia/public/images/link_out_black.gif" border="0" />' % settings.SITE_ROOT),

    
]

def expand_shortcuts(content):
    ''' Substitutes shortcuts '''
    for original, replacement in _shortcuts:
        content = content.replace(original, replacement)
    return content


def strip_url(url):
    ''' Strips leading 'http://' and leading 'www.'
        and trailing './' from URLs
    '''
    url = re.sub(r'^(http(s)?://)?(www\d?\.)?', '', url)
    url = url.rstrip('/').rstrip('.')
    return url


def strip_domain(url):
    ''' Returns just the domain name from a URL with any leading www stripped. '''
    return strip_domain_and_rest(url)[0]


def strip_tlds(url):
    ''' Like strip_domain() but also removes the top-level domain name(s) '''
    domain = strip_domain(url)
    domain = domain.rsplit('.', 1)[0]
    
    # Strip possible additional domain so e.g. www.modernlifeisrubbish.co.uk -> modernlifeisrubbish
    if domain.endswith(('.com', '.co')):
        domain = domain.rsplit('.', 1)[0]
    
    return domain
    
    
def strip_domain_and_rest(url):
    ''' Get the stripped domain plus whatever follows the first slash.
        'rest' will always start with / and never end with /
    '''
    domain, _, rest = strip_url(url).partition('/')
    # Make rest look like a real path
    rest = '/' + rest
    return domain, rest


def unescape(text):
    ''' Removes HTML or XML character references and entities from a text string.
    
        Note: If text contains references or entities that resolve to Unicode characters,
        text itself must be (decoded) Unicode or ascii. If not you will get UnicodeDecodeError.
        
        @param text The HTML (or XML) source text.
        @return The plain text, as a Unicode string, if necessary.
        @author Fredrik Lundh http://effbot.org/zone/re-sub.htm#unescape-html
    '''
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                value = htmlentitydefs.name2codepoint[text[1:-1]]
                if value < 128:
                    # Return plain string if possible
                    text = chr(value)
                else:
                    text = unichr(value)
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
    
    
def logToData(fileName):
    ''' Initialize logging with a rollover file to LOG_DIRECTORY ''' 
    from logging.handlers import TimedRotatingFileHandler
    
    path = os.path.join(settings.LOG_DIRECTORY, fileName)
    handler = TimedRotatingFileHandler(path, 'midnight')
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S %Z')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)
    
    
def formatChanges(source, changes):
    '''Defines a formatted string to add change to admin
    change log'''

    log_changes = ['%s changed ' % source]
    for change in changes:
        log_changes.append('%s(new:%s | old:%s)' % (change[1], change[3], change[2]))
        if len(changes) != 1:
            if len(changes) == 2 and change == changes[-2]:
                log_changes.append(' and ')
            elif len(changes) > 2 and change != changes[-2] and change != changes[-1]:
                log_changes.append(', ')
            elif len(changes) > 2 and change == changes[-2]:
                log_changes.append(' and ')
    log_changes = ''.join(log_changes)

    return log_changes