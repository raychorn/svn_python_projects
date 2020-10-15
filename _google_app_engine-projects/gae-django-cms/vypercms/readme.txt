gae-django-cms (GD-cms) is a Multi-Author CMS running on the Google App Engine implemented by python and django.

= Features =
 * overcome the 1,000 result limit of Google's datastore
 * Multi-Author , after registration through the mail to activate
 * rich content editor by tinymce integrated picasa album or upload photos to Google's datastore
 * import data from wordpress export file
 * cache enabled
 * I18N suport
 * Themes suport
 * Syntaxhighlighter
 * RSS
 * Sitemap

Now you can view the sample sites:

http://gae-django-cms.appspot.com

Download open project source from http://code.google.com/p/gae-django-cms/

= How to =
 * Set "application: your_gae_id" in app.yaml
 * Set "DEFAULT_FROM_EMAIL = 'yourgmail@gmail.com'" in settings.py
 * Set utcoffset of class EstTzinfo in /cms/models.py
 * Replace logo.gif and favicon.ico at /media/images/
 * update to your GAE

= Tips =
 * The default administrator with the username and password "admin"
 * Set "USE_I18N = False" in settings.py to set GD-cms default language to 'en'

Users to retain powered by information

Creat: Jul 29, 2009
Update: Sep 3, 2009 
Update: Nov 2, 2009

////////////////////////////////////////////////

gae-django-cms (GD-cms) ��һ�����û�����python��д��������GAE�ϵ�CMS��

= һ����Ҫ���ܣ� =
 * ���¡�����û�����ƣ������GAE��������ֻ����1000�������Ч���淵�ؽ��ָ�����ӵ����⣩
 * ���û���ע���ͨ�����伤��ɣ�Ͷ������
 * ��tinymce�༭��������picasa��ᡢ��ֱ�Ӱ���Ƭ�ϴ���GAE���ݿ�
 * ���Ե����wordpress����������
 * ֧�ֻ��棬����ٶȺܿ죬�������Ҳ�ܿ죨��wordpress�����屶��
 * �������֧��
 * ֧�ֶ�����
 * �������
 * RSS
 * Sitemap

GD-cms��վ��ʾ���ĵ�http://gae-django-cms.appspot.com

= ����ʹ��˵���� =
 * ���غ��޸�app.yaml��application: your_gae_id��
 * �޸�settings.py��DEFAULT_FROM_EMAIL = 'yourgmail@gmail.com'��
 * Ĭ��ΪӢ�İ棬�޸�settings.py��USE_I18N = True#��Ϊ���ģ�
 * �滻/media/images/�µ�favicon.ico�ļ���
 * �滻/themes/XXXXXX/images/�µ�logo.gif��logo.png�ļ���
 * �ϴ�����ʹ��

ע��Ĭ�Ϲ���Ա�ʻ������붼�ǣ�admin���û�ϵͳ������google�ʻ�

GD-cms���ص�ַhttp://code.google.com/p/gae-django-cms/

= ��������ʹ�ã� =

Ҳ�����Լ��������⣬����������ο�http://gae-django-cms.appspot.com/cms/show_categories/18_1.html

����Ľ���ʹ�ÿɲο��ĵ�http://gae-django-cms.appspot.com/cms/show_categories/18_1.html

ʹ�����������˵��Ͷ���ʵ������powered by��Ϣ

2009.07.29����
2009.09.03����
2009.11.02����

= Screenshots =

Main Page
<p><img src="http://laiba.tianya.cn/laiba/images/1075271/12501726461866459327/A/1/m.jpg" alt="" width="732" height="999" /></p>

Add/Edit Blog
<p><img src="http://laiba.tianya.cn/laiba/images/1075271/12501726630197686829/A/1/m.jpg" alt="" width="732" height="508" /></p>

<p><img src="http://laiba.tianya.cn/laiba/images/1075271/12501726151276319923/A/1/m.jpg" alt="" width="732" height="512" /></p>