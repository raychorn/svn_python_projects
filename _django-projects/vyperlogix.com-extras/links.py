# Migrate data

from content import models as content_models

from vyperlogix.html import parsers

def main():
    contents = content_models.Content.objects.all()
    for aContent in contents:
        links = parsers.parse_for_hrefs('a',aContent.content)
        for aLink in links:
            if (aLink.endswith('/')):
                aLink = aLink[0:-1]
            urls = content_models.URL.objects.filter(url=aLink)
            if (urls.count() == 0):
                print aLink
                _url_tag = aLink.split('://')[-1].split('/')[0]
                if (len(_url_tag) > 30):
                    _url_tag = _url_tag[0:27] + '...'
                _descr = str(aContent)
                if (len(_descr) > 128):
                    _descr = _descr[0:125] + '...'
                aURL = content_models.URL(url_tag=_url_tag,descr=_descr,url=aLink)
                aURL.save()
            else:
                print '(*) "%s" -> "%s"' % (aLink,str(aContent))
        pass

if (__name__ == '__main__'):
    print 'Begin:'
    main()
    print 'End !'
    
