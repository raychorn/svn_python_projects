"""
translate.py

Translates strings using Google Translate

All input and output is in unicode.
"""

__all__ = ('source_languages', 'target_languages', 'translate')

import sys
import urllib2
import urllib

from BeautifulSoup import BeautifulSoup

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'translate.py/0.1')]

# lookup supported languages

translate_page = opener.open("http://translate.google.com/translate_t")
translate_soup = BeautifulSoup(translate_page)

source_languages = {}
target_languages = {}

for language in translate_soup("select", id="old_sl")[0].childGenerator():
    if language['value'] != 'auto':
        source_languages[language['value']] = language.string

for language in translate_soup("select", id="old_tl")[0].childGenerator():
    if language['value'] != 'auto':
        target_languages[language['value']] = language.string

def translate(sl, tl, text):

    """ Translates a given text from source language (sl) to
        target language (tl) """

    assert sl in source_languages, "Unknown source language."
    assert tl in target_languages, "Unknown taret language."

    assert type(text) == type(u''), "Expects input to be unicode."

    # Do a POST to google
    
    # I suspect "ie" to be Input Encoding. 
    # I have no idea what "hl" is.

    translated_page = opener.open(
        "http://translate.google.com/translate_t?" + 
        urllib.urlencode({'sl': sl, 'tl': tl}),
        data=urllib.urlencode({'hl': 'en',
                               'ie': 'UTF8',
                               'text': text.encode('utf-8'),
                               'sl': sl, 'tl': tl})
    )
    
    translated_soup = BeautifulSoup(translated_page)

    return translated_soup('div', id='result_box')[0].string

