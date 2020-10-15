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

gae-django-cms (GD-cms) 是一个多用户、用python编写、运行在GAE上的CMS，

= 一、主要功能： =
 * 文章、分类没有限制（解决了GAE搜索数据只返回1000个结果、效率随返回结果指数增加的问题）
 * 多用户（注册后通过邮箱激活即可）投递文章
 * 用tinymce编辑器，集成picasa相册、或直接把照片上传到GAE数据库
 * 可以导入从wordpress导出的文章
 * 支持缓存，浏览速度很快，添加文章也很快（比wordpress快四五倍）
 * 多国语言支持
 * 支持多主题
 * 代码高亮
 * RSS
 * Sitemap

GD-cms网站演示及文档http://gae-django-cms.appspot.com

= 二、使用说明： =
 * 下载后修改app.yaml的application: your_gae_id；
 * 修改settings.py的DEFAULT_FROM_EMAIL = 'yourgmail@gmail.com'；
 * 默认为英文版，修改settings.py的USE_I18N = True#即为中文；
 * 替换/media/images/下的favicon.ico文件；
 * 替换/themes/XXXXXX/images/下的logo.gif、logo.png文件；
 * 上传即可使用

注：默认管理员帐户和密码都是：admin，用户系统独立于google帐户

GD-cms下载地址http://code.google.com/p/gae-django-cms/

= 三、进阶使用： =

也可以自己制作主题，制作主题请参考http://gae-django-cms.appspot.com/cms/show_categories/18_1.html

更多的进阶使用可参考文档http://gae-django-cms.appspot.com/cms/show_categories/18_1.html

使用请尊重他人的劳动果实，保留powered by信息

2009.07.29创建
2009.09.03更新
2009.11.02更新

= Screenshots =

Main Page
<p><img src="http://laiba.tianya.cn/laiba/images/1075271/12501726461866459327/A/1/m.jpg" alt="" width="732" height="999" /></p>

Add/Edit Blog
<p><img src="http://laiba.tianya.cn/laiba/images/1075271/12501726630197686829/A/1/m.jpg" alt="" width="732" height="508" /></p>

<p><img src="http://laiba.tianya.cn/laiba/images/1075271/12501726151276319923/A/1/m.jpg" alt="" width="732" height="512" /></p>