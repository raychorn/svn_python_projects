# Migrate data

from content import models as content_models

def main():
    menutype = content_models.MenuType.objects.get(menutype='bottom')
    contents = content_models.Content.objects.all()
    for aContent in contents:
        try:
            c = content_models.Content2.objects.get(menutype=menutype,url=aContent.url,menu_tag=aContent.menu_tag)
        except:
            c = None
        if (c is None):
            newContent = content_models.Content2(menutype=menutype,url=aContent.url,menu_tag=aContent.menu_tag,content=aContent.content)
            newContent.save()

if (__name__ == '__main__'):
    print 'Begin:'
    main()
    print 'End !'
    
