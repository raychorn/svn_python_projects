import os, sys
import re
import urlparse

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect

from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.misc import ObjectTypeName

from vyperlogix.http import urlreader

from vyperlogix.html import myOOHTML as oohtml

from django.conf import settings

import BeautifulSoup

_reDoctype = re.compile(r"<!DOCTYPE([^>]*?)>")
_reConditionalCss = re.compile(r"\[if\s(?:[^<]+|<(?!!\[endif\]-->))*<!\[endif\]")

class VyperOptimizeMiddleware(object):
    '''Optimize static content on-the-fly'''

    def __retrieve_content__(self,url,MEDIA_URL,MEDIA_ROOT):
        foo = urlparse.urlparse(url)
        is_local_to_site = (foo[0:2] == ('', ''))
        if (is_local_to_site):
            if (foo[2].lower().startswith(MEDIA_URL.lower())):
                toks = [t.strip() for t in foo[2].split('/') if (len(t.strip()) > 0)]
                fpath = os.path.join(MEDIA_ROOT,os.sep.join(toks[1:]))
                if (os.path.exists(fpath)):
                    fdata = _utils.readFileFrom(fpath)
                    return fdata
        else:
            fdata = urlreader.read_from_url(foo[1],foo[2])
            return fdata
        return ''
    
    def __get_doctype__(self,content):
	match = _reDoctype.search(content, re.IGNORECASE)
	if match:
	    return match.group()
	return ''
    
    def process_response(self, request, response):
        if (ObjectTypeName.typeClassName(response) == 'django.http.HttpResponse'):
            s = ''.join([t.strip() for t in str(response.content).split('\n') if (len(t.strip()) > 0)])
            soup = BeautifulSoup.BeautifulSoup(s)
            head = soup.find('head')
            body = soup.find('body')
            tags = []
            css = []
            comments = []
            styles = []
            scripts = []
            host = request.META['HTTP_HOST']
            if (head is not None):
                for aTag in head.childGenerator():
                    if (ObjectTypeName.typeClassName(aTag) != 'BeautifulSoup.Comment'):
                        try:
                            d_attrs = lists.HashedFuzzyLists2(dict(aTag.attrs))
                            if (aTag.name == 'script'):
                                scripts.append(aTag)
                            elif (aTag.name == 'link') and (d_attrs['rel'] == 'stylesheet'):
                                css.append(aTag)
                            elif (aTag.name == 'style'):
                                styles.append(aTag)
                            else:
                                tags.append(aTag)
                        except Exception, e:
                            info_string = _utils.formattedException(details=e)
                            pass
                    else:
                        t = aTag.decode()
                        if (_reConditionalCss.match(t)):
                            comments.append('<!--%s-->' % (t))
                contents = []
                for aTag in tags:
                    contents.append(str(aTag))
                css_content = ''
                for aTag in css:
                    d_attrs = lists.HashedFuzzyLists2(dict(aTag.attrs))
                    fdata = self.__retrieve_content__(lists.get(d_attrs,'href',''),settings.MEDIA_URL,settings.MEDIA_ROOT)
                    css_content += fdata
                for aTag in styles:
                    for someContent in aTag.contents:
                        css_content += someContent.decode().replace('<!--','').replace('-->','')
                h = oohtml.Html()
                h.tagSTYLE(css_content)
                contents.append(h.toHtml())
                js_content = ''
                for aTag in scripts:
                    d_attrs = lists.HashedFuzzyLists2(dict(aTag.attrs))
                    src = lists.get(d_attrs,'src','')
                    if (len(src) > 0):
                        fdata = self.__retrieve_content__(src,settings.MEDIA_URL,settings.MEDIA_ROOT)
                        js_content += fdata
                    # script tags can have both a src= and contents although this may not be a common usage just yet (circa. 2009)
                    fdata = ''
                    for someContent in aTag.contents:
                        fdata += _utils.ascii_only(someContent)
                    js_content += fdata
                h = oohtml.Html()
                h.tagSCRIPT(js_content,language="javascript")
                contents.append(h.toHtml())
                doctype = self.__get_doctype__(s)
                h = oohtml.Html()
		headTag = h.tag(oohtml.oohtml.HEAD)
		headTag.text(''.join(contents))
                new_content = doctype+h.toHtml()+body.decode()
		response.content = new_content
        return response

    #def process_exception(self, request, exception):
        #return None
    