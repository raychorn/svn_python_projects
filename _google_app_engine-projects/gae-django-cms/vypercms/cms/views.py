# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from google.appengine.ext import db
from mimetypes import guess_type

from cms.forms import GlobalvarForm, CategoriesForm, AlladForm, LinksForm, RedirectForm, PhotoForm, CommentForm
from cms.models import *
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite

from random import choice, sample
from google.appengine.api import memcache

from google.appengine.ext import zipserve
import re

from settings import TEMPLATE_DIRS,USE_I18N

def EST_time(pub_date):
    pub_date = pub_date.replace(tzinfo=UtcTzinfo())
    return pub_date.astimezone(EstTzinfo())

def get_now_date():
    return EST_time(datetime.datetime.now())

#######Memcache
memtime=172800
globalvar_key = "globalvar_mem"
allad_key = "allad_mem"
categories_key = "categories_mem"
nav_categories_key = "nav_categories_mem"
links_key = "links_mem"
comments_key = "comments_mem"
new_arts_key = "new_arts_mem"
hot_arts_key = "hot_arts_mem"
artid_list_key = "artid_list_mem"
slide_list_key = "slide_list_men"
all_tags_key = "all_tags_men"
max_tagcount_key = "max_tagcount_men"
#######

base_values = {}

def get_globalvar():
    """get all globalvar"""
    objects = memcache.get(globalvar_key)
    if objects is None:
        objects = Globalvar.all().fetch(30)
        memcache.add(globalvar_key, objects, memtime)
        
    for obj in objects:
        base_values[obj.name] = obj.value
    if 'theme_name' not in base_values:
        base_values['theme_name'] = 'default'
    #'''
    if 'theme_name' in base_values:
        for temdir in TEMPLATE_DIRS:
            if 'themes/%s/templates'%base_values['theme_name'] not in temdir:
                TEMPLATE_DIRS.remove(temdir)
    #'''

get_globalvar()

def updatetov12():
    themes = Globalvar.all().filter('name =', 'themes').get()
    if themes:
        themes.delete()
        
    add_dic = {'reg_user':['1','Whether or not to open register 1 / 0 '],
            'syntaxhighlighter':['1','Whether or not to open syntaxhighlighter 1 / 0 '], 
            'theme_name':['default','Setting the theme']}
    for vname in add_dic:
        hasit = Globalvar.all().filter('name =', vname).get()
        if not hasit:
            newv = Globalvar(name = vname, value = add_dic[vname][0], description = add_dic[vname][1])
            newv.put()
    
    add_dic = {'art_bot_ad':['Art_bot_ad text or js','art_bot_ad'],
            'cate_bot_ad':['cate_bot_ad text or js','cate_bot_ad']}    
    for vname in add_dic:
        hasit = Allad.all().filter('name =', vname).get()
        if not hasit:
            newv = Allad(name = vname, value = add_dic[vname][0], description = add_dic[vname][1])
            newv.put()
    
    memcache.flush_all()
    #get_globalvar()
    
def get_allad():
    """get all allad"""
    objects = memcache.get(allad_key)
    if objects is None:
        objects = Allad.all().fetch(30)
        memcache.add(allad_key, objects, memtime)
        
    for obj in objects:
        base_values[obj.name] = obj.value

get_allad()

def get_categories():
    """get all categories"""
    objects = memcache.get(categories_key)
    if objects is None:
        objects = Categories.all().order('-sort').fetch(300)          
        memcache.add(categories_key, objects,memtime)
        
    base_values['categories'] = objects
    return objects

get_categories()

def get_nav_cate():
    objects = memcache.get(nav_categories_key)
    if objects is None:
        objects = []
        all_cates = get_categories()
        for cate in all_cates:
            if cate.display != 0:
                objects.append(cate)
        memcache.add(nav_categories_key, objects,memtime)
    base_values['nav_categories'] = objects
    return objects

#get_nav_cate()

def get_links():
    """get all links"""
    objects = memcache.get(links_key)
    if objects is None:
        objects = Links.all().order('-sort').fetch(300)
        memcache.add(links_key, objects, memtime)
    
    base_values['links'] = objects
    return objects

get_links()

def get_new_art(getn):
    """ get new article """
    article_list = memcache.get(new_arts_key)
    if article_list is None:
        article_list = Article.all().order('-pub_date').fetch(getn)
        memcache.add(new_arts_key, article_list, memtime/4)
    
    base_values['new_arts'] = article_list
    return article_list

get_new_art(9)

def get_hot_art(getn):
    """ get hot article """
    article_list = memcache.get(hot_arts_key)
    if article_list is None:
        article_list = Article.all().order('-browse').fetch(getn)
        memcache.add(hot_arts_key, article_list, memtime/10)
    #
    base_values['hot_arts'] = article_list
    return article_list

get_hot_art(10)

def get_slide():
    """ get slide index info """
    slide_list = memcache.get(slide_list_key)
    if slide_list is None:
        slide_list = Slide.all().order('-pub_date').fetch(6)
        memcache.add(slide_list_key, slide_list, memtime)
    return slide_list

def get_art(art_keyid):
    """ get article by art_id """
    art_keyid = int(art_keyid)
    if base_values['show_browse'] =='1':
        article = Article.get_by_id(art_keyid)
        if article:
            try:
                au = article.author
            except:
                article.author = User.get_by_key_name( "admin" ).key()
                article.put()
        else:
            return None
    else:
        article = memcache.get("article_%d_men"%art_keyid)
        if article is None:
            article = Article.get_by_id(art_keyid)
            if article:
                try:
                    au = article.author
                except:
                    article.author = User.get_by_key_name( "admin" ).key()
                    article.put()
                memcache.add("article_%d_men"%art_keyid, article, memtime/2)
            else:
                return None
    return article


def get_art_con(art_keyid):
    """ get artticle content by art_id """
    articlecontent = memcache.get("articlecontent_%d_men"%art_keyid)
    if articlecontent is None:
        articlecontent = ArticleContent.get_by_key_name( "key_%d"%art_keyid )
        memcache.add("articlecontent_%d_men"%art_keyid, articlecontent, memtime)
    return articlecontent

def get_art_com(art_keyid):
    """ get artticle comment by art_id """
    articlecomment = memcache.get("articlecomment_%d_men"%art_keyid)
    if articlecomment is None:
        article = get_art(art_keyid)
        articlecomment = article.comment_set.order('-pub_date')
        memcache.add("articlecomment_%d_men"%art_keyid, articlecomment, memtime)
    return articlecomment    

def Add_cate_articleid(cat_keyid):
    """ when one cate_arts is None , filter arts under this cate and put these id to Articleid as str """
    categorie = Categories.get_by_id(cat_keyid)
    article_list = Article.all().filter('cate =', categorie).order('-pub_date').fetch(300)
    all_id_list = []
    for art in article_list:
        all_id_list.append(str(art.key().id()))
    
    if len(all_id_list)>0:
        cat_artid = Articleid(key_name = "key_%d"%cat_keyid)
        cat_artid.idstr =",".join(all_id_list)
        cat_artid.put()
    
    return article_list

def change_artid(cate_id, art_id, act = 'add'):
    """ when add/del one article , add/del new id to Articleid """
    if act =="add":
        cat_artid = Articleid.get_by_key_name("key_%d"%cate_id)
        if cat_artid:
            if ",%d,"%art_id not in ",%s,"%(cat_artid.idstr):
                cat_artid.idstr ="%d,%s"%(art_id,cat_artid.idstr)
                cat_artid.put()
        else:#add
            article_list = Add_cate_articleid(cate_id)
    elif act =="del":
        cat_artid = Articleid.get_by_key_name("key_%d"%cate_id)
        cat_artid_list = cat_artid.idstr.split(",")
        cat_artid_list.remove(str(art_id))
        if len(cat_artid_list)==0:
            cat_artid.delete()
        else:
            cat_artid.idstr =",".join(cat_artid_list)
            cat_artid.put()
        
def get_cat_art(cat_keyid,page):
    """ show cate_art page """
    categorie = Categories.get_by_id(cat_keyid)
    all_pages = 0
    if categorie:
        cate_articles = memcache.get("cate_%d_%d_men"%(cat_keyid,page))
        if cate_articles is None:
            #get from Articleid
            art_exist = Article.all().filter('cate =', categorie).get()
            if art_exist:
                article_list = []
                cat_artid = Articleid.get_by_key_name("key_%d"%cat_keyid)
                if cat_artid:
                    cat_artid_list = cat_artid.idstr.split(",")
                    #
                    try:
                        page_num = int(base_values['cate_art_num'])
                    except:
                        page_num = 300
                    all_pages = len(cat_artid_list)/page_num
                    if len(cat_artid_list)%page_num != 0:
                        all_pages += 1
                    #
                    if page <=0:
                        page =1
                    elif page >all_pages:
                        page =all_pages
                    #
                    page_art = cat_artid_list[(page-1)*page_num:page*page_num]                    
                    for art_id in page_art:
                        cat_art = get_art(art_id)
                        article_list.append(cat_art)
                else:#add
                    article_list = Add_cate_articleid(cat_keyid)
            else:
                article_list = []
            #
            cate_articles = [article_list,all_pages]
            memcache.add("cate_%d_%d_men"%(cat_keyid,page), cate_articles, memtime)
    else:
        cate_articles = [[],all_pages]
    return cate_articles

def get_artid_list():
    """ get all article id """
    artid_list = memcache.get(artid_list_key)
    if artid_list is None:
        artid_list = []
        cat_artids = Articleid.all()
        for cat_artid in cat_artids:
            artid_list.extend(cat_artid.idstr.split(","))
        #
        memcache.add(artid_list_key, artid_list,memtime)
    return artid_list

def get_cat_art_n(cat_keyid,getn0=0,getn1=10):
    """ get new top N arts in one categorie """
    categorie = Categories.get_by_id(cat_keyid)
    if categorie:
        article_list = memcache.get("cate_n_%d_men"%cat_keyid)
        if article_list is None:
            art_exist = Article.all().filter('cate =', categorie).get()
            if art_exist:
                article_list = []
                cat_artid = Articleid.get_by_key_name("key_%d"%cat_keyid)
                if cat_artid:
                    cat_artid_list = cat_artid.idstr.split(",")
                    for art_id in cat_artid_list[getn0:getn1]:
                        cat_art = get_art(int(art_id))
                        article_list.append(cat_art)
                else:#add
                    article_list = Add_cate_articleid(cat_keyid)[getn0:getn1]
            else:
                article_list = []
            #
            memcache.add("cate_n_%d_men"%cat_keyid, article_list, memtime)
    else:
        article_list = []
    return article_list

def get_cat_art2(cat_keyid, getn):
    """ get new top N arts in one categorie , Similar like get_cat_art_n """
    article_list = get_cat_art_n(cat_keyid,0,getn)
    return article_list

def get_cat_art3(cat_keyid, getn):
    """ get N arts by random in one categorie """
    all_arts = get_cat_art(cat_keyid,1)[0]
    if len(all_arts) < getn:
        getn = len(all_arts)
    article_list = sample(all_arts,getn)
    return article_list

def get_comments():
    """ get new top 10 comments """
    comments = memcache.get(comments_key)
    if comments is None:
        comments = Comment.all().order('-pub_date').fetch(10)
        memcache.add(comments_key, comments, memtime)
    return comments

def get_all_img(art_content):
    """ get all img tag src value in the article content """
    img=re.compile(r"""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+).*?>""",re.I)
    m = img.findall(art_content)
    if len(m)>0:
        return m
    else:
        return None

def get_img(art_content):
    """ return the first img src value for index flash slice show """
    imgs = get_all_img(art_content)
    if imgs:
        return imgs[0]
    else:
        return None
    
#############--globalvar
@login_required
def list_globalvar(request):
    return object_list(request, Globalvar.all(), paginate_by=20, extra_context = base_values)

@login_required
def add_globalvar(request):
    return create_object(request, form_class=GlobalvarForm,
        post_save_redirect=reverse('cms.views.globalvar_change'), extra_context = base_values)

@login_required
def edit_globalvar(request, key):
    return update_object(request, object_id=key, form_class=GlobalvarForm, 
        post_save_redirect=reverse('cms.views.globalvar_change'), extra_context = base_values)

@login_required
def delete_globalvar(request, key):
    return delete_object(request, Globalvar, object_id=key,
        post_delete_redirect=reverse('cms.views.globalvar_change'), extra_context = base_values)

#############--allad
@login_required
def list_allad(request):
    return object_list(request, Allad.all(), paginate_by=20, extra_context = base_values)

@login_required
def add_allad(request):
    return create_object(request, form_class=AlladForm,
        post_save_redirect=reverse('cms.views.allad_change'), extra_context = base_values)

@login_required
def edit_allad(request, key):
    return update_object(request, object_id=key, form_class=AlladForm, 
        post_save_redirect=reverse('cms.views.allad_change'),extra_context = base_values)

@login_required
def delete_allad(request, key):
    return delete_object(request, Allad, object_id=key,
        post_delete_redirect=reverse('cms.views.allad_change'), extra_context = base_values)

#############--comment
def list_comment(request):
    #get random_cate_arts
    #random_cate = choice(base_values['categories'])
    #random_cate_arts = get_cat_art2(random_cate.key().id(), 10)
    #base_values.update({'random_cate_arts':random_cate_arts})
    return object_list(request, Comment.all().order('-pub_date'), paginate_by=20, extra_context = base_values)

#############--links
@login_required
def list_links(request):
    return object_list(request, Links.all(), paginate_by=20, extra_context = base_values)

@login_required
def add_links(request):
    return create_object(request, form_class=LinksForm,
        post_save_redirect=reverse('cms.views.links_change'), extra_context = base_values)

@login_required
def edit_links(request, key):
    return update_object(request, object_id=key, form_class=LinksForm, 
        post_save_redirect=reverse('cms.views.links_change'),extra_context = base_values)

@login_required
def delete_links(request, key):
    return delete_object(request, Links, object_id=key,
        post_delete_redirect=reverse('cms.views.links_change'), extra_context = base_values)

#############--redirect
@login_required
def list_redirect(request):
    return object_list(request, Redirect.all(), paginate_by=20, extra_context = base_values)

@login_required
def add_redirect(request):
    return create_object(request, form_class=RedirectForm,
        post_save_redirect=reverse('cms.views.list_redirect'), extra_context = base_values)

@login_required
def edit_redirect(request, key):
    return update_object(request, object_id=key, form_class=RedirectForm, 
        post_save_redirect=reverse('cms.views.list_redirect'),extra_context = base_values)

@login_required
def delete_redirect(request, key): 
    return delete_object(request, Redirect, object_id=key,
        post_delete_redirect=reverse('cms.views.list_redirect'), extra_context = base_values)

def checkup():
    new0 = []
    new1 = list(base_values['links'])
    s1 = ''.join(map(chr,[71,68,45,99,109,115]))
    s2 = ''.join(map(chr,[104,116,116,112,58,47,47,103,97,101,45,100,106,97,110,103,111,45,99,109,115,46,97,112,112,115,112,111,116,46,99,111,109]))
    get_n = True
    for n in new1:
        if n.name == s1 and (n.url == s2 or n.url[:-1] == s2):
            get_n = False
            break
    if get_n:
        new0.append({'sort': 100, 'name': s1, 'url': s2})
    new0.extend(new1)
    base_values['links'] = new0

def get_all_tags():
    all_tags = memcache.get(all_tags_key)
    if all_tags is None:
        all_tags = Tag.all()
        memcache.add(all_tags_key, all_tags, memtime)
    #random tags
    try:
        tag_cloud_num = int(base_values['tag_cloud_num'])
    except:
        tag_cloud_num = 100
    if tag_cloud_num > len(all_tags):
        tag_cloud_num = len(all_tags)
    base_values['all_tags'] = sample(all_tags,tag_cloud_num)
    #return all_tags

def get_max_tagcount():
    max_tagcount = memcache.get(max_tagcount_key)
    if max_tagcount is None:
        max_tag = Tag.all().order('-tagcount').get()
        if max_tag:
            max_tagcount = max_tag.tagcount
            memcache.add(max_tagcount_key, max_tagcount, memtime/6)
        else:
            max_tagcount = 1
    base_values['max_tagcount'] = max_tagcount
#############--Categories
@login_required
def list_categories(request):
    return object_list(request, Categories.all().order('-sort'), paginate_by=20, extra_context = base_values)

@login_required
def add_categories(request):
    return create_object(request, form_class=CategoriesForm,
        post_save_redirect=reverse('cms.views.categories_change'), extra_context = base_values)

@login_required
def edit_categories(request, key):
    return update_object(request, object_id=key, form_class=CategoriesForm,
        post_save_redirect=reverse('cms.views.categories_change'), extra_context = base_values)

@login_required
def delete_categories(request, key,cate_key_id): 
    return delete_object(request, Categories, object_id=key,
        post_delete_redirect=reverse('cms.views.categories_change_del', kwargs=dict(cate_key=key,cate_key_id =cate_key_id)), extra_context = base_values)

##############
def generate(request, template_name, template_values={}):
    get_globalvar()
    get_nav_cate()
    get_allad()
    base_values['categories'] = get_categories()
    base_values['links'] = get_links()
    base_values['new_arts'] = get_new_art(9)
    base_values['hot_arts'] = get_hot_art(10)
    base_values['USE_I18N'] = USE_I18N
    checkup()
    #
    base_values['cur_categories'] = None
    base_values['browse_stage'] = None
    #
    get_all_tags()
    #get_max_tagcount()
    base_values.update(template_values)
    return render_to_response(request,template_name,base_values)

def index_page(request):
    """
    updated = []
    objects = Article.all().fetch(30)
    for obj in objects:
        updated.append(obj)
    db.delete(updated)
    updated = []
    objects = ArticleContent.all().fetch(30)
    for obj in objects:
        updated.append(obj)
    db.delete(updated)
    """
    base_values['slide'] = get_slide()
    categories = base_values['categories'][:8]
    if len(categories)== 0:
        return HttpResponseRedirect( reverse('cms.views.install'))
    theme_name = Globalvar.all().filter('name =', 'theme_name').get()
    if not theme_name:
        updatetov12()
    cate_art_list = []
    for cate in categories:
        cate_art_list.append( [cate,get_cat_art2(cate.key().id(), 10)] )
    
    mid_num = len(categories)/2
    if mid_num%2 != 0:
        mid_num += 1
        #'%s/templates/index_page.html'%(base_values['theme_name'])
    #
    try:
        current_site = Site.objects.get_current()
    except:
        current_site = RequestSite(request)
    return generate(request,'index_page.html',{'browse_stage':'home','cate_art_list':cate_art_list, 'comments':get_comments(),'new_arts':base_values['new_arts'],'mid_num':mid_num,'current_site_domain':current_site.domain})

def tag_str2list(tag_str):
    new_list = []
    tag_list = tag_str.split(",")
    for tag in tag_list:
        if tag:
            tag_new = Tag.get_by_key_name(u'key_%s'%tag)
            if tag_new:
                tag_new.tagcount += 1
                tag_new.put()
            else:
                tag_new = Tag(key_name = u'key_%s'%tag, tag = tag)
                tag_new.put()
            new_list.append(tag)
    memcache.delete(all_tags_key)
    memcache.delete(max_tagcount_key)
    return new_list

@login_required
def add_article(request):
    if request.method == 'POST':
        cate = request.POST['cate']
        try:
            title = request.POST['title']
        except:
            return generate(request,'tip.html',{'tip':_(u'Not fill the title, go back to fill in the title.')})
        try:
            content = request.POST['content']
        except:
            return generate(request,'tip.html',{'tip':_(u'Not filled, please return to fill in the content field.')})
        tags_str = request.POST.get('tags','')
        try:
            if tags_str[-1]==',':
                tags_str = tags_str[:-1]
        except:pass
        try:
            if tags_str[0]==',':
                tags_str = tags_str[1:]  
        except:pass
        #check exist
        arttitle_exist = Article.all().filter('title =', title).get()
        if arttitle_exist:
            return generate(request,'article_add.html',{'categories':get_categories(), 'cate':db.Key(cate), 'title':title, 'content':content, 'tags':tags_str, 'title_exist':'title_exist'})
        #
        tags_list = tag_str2list(tags_str)
        #
        article = Article(cate = db.Key(cate), title = title, tags = tags_list, author = request.user, pub_date = get_now_date())
        article.put()
        if article:
            change_artid(db.Key(cate).id(),article.key().id(),'add')
            articlecontent = ArticleContent.get_by_key_name( "key_%d"%article.key().id())
            if articlecontent:
                articlecontent.content = content
            else:
                articlecontent = ArticleContent(key_name = "key_%d"%(article.key().id()), content = content)
            articlecontent.put()
            
            ###get img
            first_img = get_img(content)
            if first_img:
                link = reverse('cms.views.show_article', kwargs=dict(keyid=article.key().id()))
                myslide = Slide.all().filter('link =', link).get()
                if myslide is None:
                    myslide = Slide()
                myslide.title = title
                myslide.link = link
                myslide.imgsrc = first_img
                myslide.put()
                if Slide.all().count() > 6:
                    oldest_file = Slide.all().order('pub_date').get()
                    oldest_file.delete()
                memcache.delete(slide_list_key)
        else:
            article.delete()
            return generate(request,'tip.html',{'tip':_(u'There is some error to Add article.')}) 
        #
        art_keyid = article.key().id()
        memcache.delete("cate_%d_%d_men"%(article.cate.key().id(),1))
        memcache.delete("cate_n_%d_men"%(article.cate.key().id()))
        memcache.delete("article_%d_men"%art_keyid)
        memcache.delete("articlecontent_%d_men"%art_keyid)
        memcache.delete(new_arts_key)
        #
        return generate(request,'tip.html',{'tip':_(u'Article added successfully.')})
    else:
        return generate(request,'article_add.html',{'categories':get_categories(),'cate':'','title':'', 'tags':'', 'content':'', 'title_exist':''})

@login_required
def list_article(request):
    articles = Article.all().order('-pub_date').fetch(100)
    return generate(request,'article_list.html',{'articles':articles}) 

@login_required
def list_my_article(request):
    articles = request.user.author_set.order('-pub_date').fetch(100)
    return generate(request,'article_list.html',{'articles':articles}) 

def show_article(request, keyid):
    article = get_art(int(keyid))
    if article:
        if request.method == 'POST':
            vericode1 = request.POST.get('vericode1','')
            vericode2 = request.POST.get('vericode2','')
                   
            comform = CommentForm(request.POST)
            
            if comform.is_valid() and vericode1 == vericode2 and vericode1 !='':
                Comment(article=article,
                    name = comform.cleaned_data['name'],
                    email = comform.cleaned_data['email'],
                    site = comform.cleaned_data['site'],
                    content = comform.cleaned_data['content']).put()
                memcache.delete(comments_key)
                memcache.delete("articlecomment_%d_men"%(article.key().id()))
                return HttpResponseRedirect( reverse('cms.views.show_article', kwargs=dict(keyid=int(keyid))))
        else:
            comform = CommentForm()
        if base_values['show_browse'] =='1':
            article.browse +=1
            article.put()
        
        articlecontent = get_art_con(int(keyid))
        articlecomment = get_art_com(int(keyid))
        
        has_pre = False
        if base_values['syntaxhighlighter'] == '1':
            tmp_p = articlecontent.content.find('pre>')
            if tmp_p != -1:
                has_pre = True
        
        random_cate = choice(base_values['categories'])
        while random_cate == article.cate:
            random_cate = choice(base_values['categories'])
        random_cate_arts = get_cat_art2(random_cate.key().id(), 10)
        
        random_cate2 = choice(base_values['categories'])
        while random_cate2 == article.cate or random_cate2 == random_cate :
            random_cate2 = choice(base_values['categories'])
        random_cate_arts2 = get_cat_art2(random_cate2.key().id(), 10)        
        
        same_cate_random_arts = get_cat_art3(article.cate.key().id(), 10)
        
        return generate(request,'article_detail.html',{'browse_stage':'show_art','cur_categories':article.cate, 'article':article, 'articlecomment':articlecomment, 'articlecontent':articlecontent.content, 'random_cate_arts':random_cate_arts, 'random_cate_arts2':random_cate_arts2, 'same_cate_random_arts':same_cate_random_arts,'comform':comform,'has_pre':has_pre })
    else:
        return generate(request,'tip.html',{'tip':_(u'The article you viewing have been deleted or does not exist.')})

def del_taglist(tag_list):
    for tag in tag_list:
        if tag:
            tag_old = Tag.get_by_key_name(u'key_%s'%tag)
            if tag_old:
                tag_old.tagcount -= 1
                if tag_old.tagcount == 0:
                    tag_old.delete()
                else:
                    tag_old.put()
                memcache.delete(u'tag_men_%s'%tag)

def add_taglist(tag_list):
    for tag in tag_list:
        if tag:
            tag_old = Tag.get_by_key_name(u'key_%s'%tag)
            if tag_old:
                tag_old.tagcount += 1
                tag_old.put()
                memcache.delete(u'tag_men_%s'%tag)
            else:
                tag_new = Tag(key_name = u'key_%s'%tag, tag = tag)
                tag_new.put()

@login_required
def edit_article(request, keyid):
    article = Article.get_by_id(int(keyid))
    if article:
        if article.author != request.user and not request.user.is_superuser:
            return generate(request,'tip.html',{'tip':_(u'You do not have permission to edit the article.')})        
        articlecontent = get_art_con(int(keyid))
        if request.method == 'POST':
            old_cate = article.cate
            old_tags = article.tags
            cate = request.POST['cate']
            tags = request.POST.get('tags','')
            try:
                if tags[-1]==',':
                    tags = tags[:-1]
            except:pass
            try:
                if tags[0]==',':
                    tags = tags[1:]
            except:pass
            try:
                title = request.POST['title']
            except:
                return generate(request,'tip.html',{'tip':_(u'Not fill the title, go back to fill in the title.')})
            try:
                content = request.POST['content']
            except:
                return generate(request,'tip.html',{'tip':_(u'Not filled, please return to fill in the content field.')})
            
            if str(old_cate.key()) != cate:
                new_cate = db.Key(cate)
                
                change_artid(old_cate.key().id(), int(keyid), act = 'del')
                change_artid(new_cate.id(), int(keyid), act = 'add')
                
                memcache.delete("cate_n_%d_men"%(old_cate.key().id()))
                memcache.delete("cate_n_%d_men"%(new_cate.id()))
                
                memcache.delete("cate_%d_%d_men"%(new_cate.id(),1))
                memcache.delete("cate_%d_%d_men"%(old_cate.key().id(),1))
                
            if ','.join(old_tags) != tags:
                new_tags_list = tags.split(",")
                tags_list_del = []
                tags_list_add = []
                for tag in old_tags:
                    if tag not in new_tags_list:
                        tags_list_del.append(tag)
                for tag in new_tags_list:
                    if tag not in old_tags:
                        tags_list_add.append(tag)
                del_taglist(tags_list_del)
                add_taglist(tags_list_add)
                article.tags = new_tags_list
                
            article.cate  = db.Key(cate)
            article.title = title
            article.put()
            
            articlecontent.content = content
            articlecontent.put()
            
            art_keyid = article.key().id()
            memcache.delete("cate_%d_%d_men"%(article.cate.key().id(),1))
            memcache.delete("cate_%d_men"%(article.cate.key().id()))
            memcache.delete("article_%d_men"%art_keyid)
            memcache.delete("articlecontent_%d_men"%art_keyid) 
            memcache.delete(new_arts_key)
            memcache.delete(all_tags_key)
            memcache.delete(max_tagcount_key)
            
            ###get img
            first_img = get_img(content)
            if first_img:
                link = reverse('cms.views.show_article', kwargs=dict(keyid=article.key().id()))
                myslide = Slide.all().filter('link =', link).get()
                if myslide is None:
                    myslide = Slide()
                myslide.title = title
                myslide.link = link
                myslide.imgsrc = first_img
                myslide.put()
                if Slide.all().count() > 6:
                    oldest_file = Slide.all().order('pub_date').get()
                    oldest_file.delete()
                memcache.delete(slide_list_key)
            
        return generate(request,'article_edit.html',{'article':article,'tags':','.join(article.tags),'articlecontent':articlecontent.content})
    else:
        return generate(request,'tip.html',{'tip':_(u'The article you viewing have been deleted or does not exist.')})

@login_required
def delete_article(request, keyid):
    article = Article.get_by_id(int(keyid))
    if article:
        if article.author != request.user and not request.user.is_superuser:
            return generate(request,'tip.html',{'tip':_(u'You do not have permission to delete the article.')})
        cate_id = article.cate.key().id()
        articlecontent = get_art_con(int(keyid))
        
        art_content = articlecontent.content
        imgsrcs = get_all_img(art_content)
        if imgsrcs:
            imgslide = Slide.all().filter('imgsrc =', imgsrcs[0]).get()
            if imgslide:
                imgslide.delete()
                memcache.delete(slide_list_key)
            for img in imgsrcs:
                if img[:16]=="/cms/photo_show/" and img[-4:]==".jpg":
                    photo = Photo.get(img[16:-4])
                    photo.delete()        
        
        art_comments = article.comment_set
        updated = []
        for comment in art_comments:
            updated.append(comment)
        if len(updated)>0:
            db.delete(updated)
        
        change_artid(cate_id, int(keyid), act = 'del')
        
        del_taglist(article.tags)
        
        articlecontent.delete()
        article.delete()
        
        art_keyid = int(keyid)
        memcache.delete("cate_%d_%d_men"%(cate_id,1))
        memcache.delete("cate_n_%d_men"%cate_id)
        memcache.delete("article_%d_men"%art_keyid)
        memcache.delete("articlecontent_%d_men"%art_keyid)  
        memcache.delete(new_arts_key)
        memcache.delete(hot_arts_key)
        
        memcache.delete(comments_key)
        memcache.delete("articlecomment_%d_men"%art_keyid)  
        memcache.delete(all_tags_key)
        memcache.delete(max_tagcount_key)
        
        get_new_art(9)
        get_hot_art(10)
        
        return generate(request,'tip.html',{'tip':_(u'The article has successfully deleted.')})
    else:
        return generate(request,'tip.html',{'tip':_(u'The article you viewing have been deleted or does not exist.')})

@login_required
def delete_comment(request, key):
    if request.user.is_superuser :
        comment = Comment.get(key)
        comment.delete()
        memcache.delete(comments_key)
        return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})
    else:
        return generate(request,'tip.html',{'tip':_(u'You do not have permission to operate.')})    
    
def show_tag_arts_list(request, tag):
    if tag:
        arts = memcache.get(u'tag_men_%s'%tag)
        if arts is None:
            arts = Article.all().filter('tags =',tag).order("-pub_date")
            memcache.add(u'tag_men_%s'%tag, arts, memtime)
        if arts:
            tag_old = Tag.get_by_key_name(u'key_%s'%tag)
            if not tag_old:
                tag_old = Tag(key_name = u'key_%s'%tag, tag = tag)
                tag_old.put()                
        else:
            tag_old = Tag.get_by_key_name(u'key_%s'%tag)
            if tag_old:
                tag_old.delete()
                memcache.delete(u'tag_men_%s'%tag)
                memcache.delete(all_tags_key)
            return generate(request,'tip.html',{'tip':_(u'The Tag you viewing has not article or has been deleted.')})
        if len(arts)==1:
            art_id = arts[0].key().id()
            return HttpResponseRedirect( reverse('cms.views.show_article', kwargs=dict(keyid=int(art_id))))
        random_cate = choice(base_values['categories'])
        random_cate_arts = get_cat_art2(random_cate.key().id(), 10)         
        return generate(request,'tag_show.html',{'browse_stage':'show_tag', 'tag':tag, 'article_list':arts, 'random_cate_arts':random_cate_arts})
    else:
        return generate(request,'tip.html',{'tip':_(u'The Tag you viewing has not article or has been deleted.')})
    
def show_categories(request, keyid, page):
    page = int(page)
    if page <=0:
        page =1    
    cate_articles = get_cat_art(int(keyid), page)
    article_list = cate_articles[0]
    all_pages = cate_articles[1]
    if article_list:
        categories = Categories.get_by_id(int(keyid))
        
        random_cate = choice(base_values['categories'])
        while random_cate == categories:
            random_cate = choice(base_values['categories'])
        random_cate_arts = get_cat_art2(random_cate.key().id(), 10)
        
        return generate(request,'categories_show.html',{'browse_stage':'show_cate','cur_page':page, 'all_pages':range(1,all_pages+1),'cur_categories':categories, 'article_list':article_list, 'random_cate_arts':random_cate_arts})
    else:
        return generate(request,'tip.html',{'tip':_(u'Under the Categorie you viewing has not article or has been deleted.')})
    
def re_url(request,value):
    myurl = Redirect.all().filter('value =', value).get()
    if myurl:
        return HttpResponseRedirect(myurl.redirto)
        #return generate(request,'re_url.html',{'url':myurl.redirto})
        #return HttpResponseRedirect( myurl.redirto )
    else:
        return generate(request,'tip.html',{'tip':_(u'URL you are viewing does not exist or has been deleted.')})

###
@login_required
def photo_upload(request):
    return create_object(request, form_class=PhotoForm, extra_context=base_values ,
        post_save_redirect=reverse('cms.views.photo_upload_done',kwargs=dict(key='%(key)s'))) 

@login_required
def photo_upload_done(request,key):
    photo = get_object_or_404(Photo, key)
    photo_url = "/cms/photo_show/%s.jpg"%key
    photo_title = photo.filename
    return generate(request,'photo_upload_done.html',{'photo_url':photo_url,'photo_title':photo_title})

def photo_show(request,key):
    photokey = "photo_%s"%key
    data = memcache.get(photokey)
    if data is None:
        photo = get_object_or_404(Photo, key)
        data = photo.avatar
        memcache.add(photokey, data, memtime)
    return HttpResponse(data,content_type='image/gif')

###########delete memcache after changed
@login_required
def globalvar_change(request):
    memcache.delete(globalvar_key)
    return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})

@login_required
def allad_change(request):
    memcache.delete(allad_key)
    return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})

@login_required
def links_change(request):
    memcache.delete(links_key)
    return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})

@login_required
def categories_change(request):
    memcache.delete(categories_key)
    memcache.delete(nav_categories_key)
    memcache.delete(new_arts_key)
    memcache.delete(hot_arts_key)
    get_new_art(9)
    get_hot_art(10)
    return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})

@login_required
def categories_change_del(request,cate_key,cate_key_id):
    memcache.delete(categories_key)
    memcache.delete(nav_categories_key)
    article_list = Article.all().filter('cate =', db.Key(cate_key)).fetch(1000)
    #
    art_list = []
    art_con_list = []
    for art in article_list:
        art_list.append(art)
        art_con = ArticleContent.get_by_key_name("key_%d"%art.key().id())
        if art_con:
            art_con_list.append(art_con)
            
        art_com_list = art.comment_set
        db.delete(art_com_list)
        
    db.delete(art_list)
    if art_con_list:
        db.delete(art_con_list)
        
    cat_atrid = Articleid.get_by_key_name("key_%d"%int(cate_key_id))
    if cat_atrid:
        cat_atrid.delete()
    
    memcache.delete(comments_key)
    memcache.delete(new_arts_key)
    memcache.delete(hot_arts_key)
    get_new_art(9)
    get_hot_art(10)
    return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})

@login_required
def emptymem(request):
    if request.user.is_superuser :
        memcache.flush_all()
        return generate(request,'tip.html',{'tip':_(u'Has been successfully operating.')})
    else:
        return generate(request,'tip.html',{'tip':_(u'You do not have permission to operate.')})

def settheme(request):
    if request.user.is_superuser :
        import os        
        if request.method == 'POST':
            themename = request.POST['themename']
            theme = Globalvar.all().filter('name =', 'theme_name').get()
            old_theme = theme.value
            if old_theme != themename:
                theme.value = themename
                theme.put()
                memcache.delete(globalvar_key)
                base_values['theme_name'] = themename
                old_dir = TEMPLATE_DIRS[0]
                TEMPLATE_DIRS[0] = old_dir.replace(old_theme,themename)
            #return generate(request,'tip.html',{'tip':TEMPLATE_DIRS})
            return HttpResponseRedirect( reverse('cms.views.settheme'))
        
        tmp = os.path.join(os.path.dirname(__file__)[:-4], 'themes')#.replace('\\','/')
        themes = os.listdir(tmp)        
        return generate(request,'set_theme.html',{'themes':themes,'cur_theme':str(base_values['theme_name'])})
    else:
        return generate(request,'tip.html',{'tip':_(u'You do not have permission to operate.')})    

def picasa(request):
    return generate(request,'picasa.html',{'tip':''})

def show_art_random(request):
    random_artid = choice(get_artid_list())
    return HttpResponseRedirect( reverse('cms.views.show_article', kwargs=dict(keyid=random_artid)))

def search(request):
    random_cate = choice(base_values['categories'])
    random_cate_arts = get_cat_art2(random_cate.key().id(), 10)    
    return generate(request,'search_detail.html',{'browse_stage':'show_art','random_cate_arts':random_cate_arts})

def install(request):
    """
    if the categories len < 8 the install will auto run when view the home page,
    or run it by view url /install
    """
    cates = Categories.all().fetch(10)
    if len(cates) < 1:
        memcache.flush_all()
        
        #dlete some data 
        db_list = [User, Globalvar, Allad, Links, Redirect, Comment, Photo, Slide, Articleid, Article, ArticleContent]
        for db_n in db_list:
            objects = db_n.all().fetch(300)
            obj_list = []
            for obj in objects:
                obj_list.append(obj)
            if obj_list:
                db.delete(obj_list) 
                
        #creat admin user
        user = User.get_by_key_name('admin')
        if not user:
            user = User(key_name='admin', username='admin',
                email='ego008@gmail.com', first_name='Boss', last_name='Admin',
                is_active=True, is_staff=True, is_superuser=True)
            user.set_password('admin')
            user.put()
                      
        ###add default
        updated = []
        updated.append(Globalvar(name = 'site_name', value = 'Site name', description = 'Custom Web site name'))
        updated.append(Globalvar(name = 'site_descr', value = 'Site Description', description = 'Custom Site Description'))
        updated.append(Globalvar(name = 'show_pud_date', value = '1', description = 'Whether or not to show the publication of the time 1/0'))
        updated.append(Globalvar(name = 'show_browse', value = '1', description = 'Whether or not to open the article to view the statistical 1 / 0 '))
        updated.append(Globalvar(name = 'reg_user', value = '1', description = 'Whether or not to open register 1 / 0 '))
        updated.append(Globalvar(name = 'syntaxhighlighter', value = '1', description = 'Whether or not to open syntaxhighlighter 1 / 0 '))
        updated.append(Globalvar(name = 'picasa_user', value = 'baixingsheying@gmail.com', description = 'picasa web album users,eg xxx@gmail.com'))
        updated.append(Globalvar(name = 'gg_verify', value = 'MnHcSlQH3x+Rva/ssKMINOEBQv6hTtYXPt1o6vYoWgg=', description = 'google webmaster site verification code'))
        updated.append(Globalvar(name = 'theme_name', value = 'default', description = 'Setting the theme'))
        updated.append(Globalvar(name = 'cate_art_num', value = '300', description = 'Setting the number of articles in single-page of Categorie'))
        updated.append(Globalvar(name = 'tag_cloud_num', value = '100', description = 'Setting the number of tag in tag cloud'))
        db.put(updated)            
        get_globalvar()
        #
        updated = []
        updated.append(Allad(name = 'top_ad', value = 'Home top ad', description = 'Home top ad'))
        updated.append(Allad(name = 'center_ad_top', value = 'Home main top ads', description = 'Home main top ads'))
        updated.append(Allad(name = 'center_ad_bot', value = 'Home main bottom ads', description = 'Home main bottom ads'))
        updated.append(Allad(name = 'center_ad_mid', value = 'Home main middle ads', description = 'Home main middle ads'))
        updated.append(Allad(name = 'right_ad_top', value = 'Sidebar top ads', description = 'Sidebar top ads'))
        updated.append(Allad(name = 'right_ad_mid', value = 'Sidebar middle ads', description = 'Sidebar bottom ads'))
        updated.append(Allad(name = 'right_ad_bot', value = 'Sidebar bottom ads', description = 'Sidebar bottom ads'))
        updated.append(Allad(name = 'cate_bot_ad', value = 'cate bottom ads', description = 'cate bottom ads'))
        updated.append(Allad(name = 'art_bot_ad', value = 'Art_bot_ad', description = 'Art_bot_ad'))
        updated.append(Allad(name = 'footer_text', value = 'Footer Text', description = 'Footer Text'))
        updated.append(Allad(name = 'site_statistic', value = '', description = 'Site Stats code'))
        db.put(updated)            
        get_allad()
        #
        updated = []
        updated.append(Categories(sort = 0, name = "Category 1"))
        updated.append(Categories(sort = 0, name = "Category 2"))
        updated.append(Categories(sort = 0, name = "Category 3"))
        updated.append(Categories(sort = 0, name = "Category 4"))
        updated.append(Categories(sort = 0, name = "Category 5"))
        updated.append(Categories(sort = 0, name = "Category 6"))
        updated.append(Categories(sort = 0, name = "Category 7"))
        updated.append(Categories(sort = 0, name = "Category 8"))
        db.put(updated)            
        get_categories()
        #
        link = Links(sort = 100, name = 'GD-cms', url = 'http://gae-django-cms.appspot.com/')
        link.put()            
        get_links()
        
        base_values['new_arts'] = []
        return HttpResponseRedirect("/")
    else:
        return generate(request,'tip.html',{'tip':_(u'Please clear all the databases to install.')})

@login_required
def import_wp(request):
    import  xml.etree.ElementTree as et
    
    xmlfile = None
    additems = []
    #
    pub_n = 0
    add_n = 0
    upd_n = 0
    if request.method == 'POST':
        xmlfile = request.FILES['xmlfile'].read()
        
        doc=et.fromstring(xmlfile)
        wpns='{http://wordpress.org/export/1.0/}'
        contentns="{http://purl.org/rss/1.0/modules/content/}"
        et._namespace_map[wpns]='wp'
        et._namespace_map[contentns]='content'
        channel=doc.find('channel')
        
        categories=channel.findall(wpns+'category')
        categories_list=[]
        
        # categories
        for cate in categories:
            nicename=cate.findtext(wpns+'category_nicename')
            name = cate.findtext(wpns+'cat_name')
            categories_list.append({'nicename':nicename,'name':name})
            #
            cat_k = {}#cat_key
            cate_db = Categories.all().filter('name =', name).get()
            if cate_db:
                cat_k["k_%s"%name]=cate_db.key()
            else:
                cate_db = Categories()
                cate_db.name = name
                cate_db.put()
                cat_k["k_%s"%name]=cate_db.key()
                
        # items
        items=channel.findall('item')
        for item in items:
            entry={}
            entry['title'] = item.findtext('title')
            content = item.findtext(contentns+'encoded')
            #
            #p = re.compile('\s{1,}')
            #content = "<p>  %s</p>"%p.sub( '</p>  <p>', content)
            #
            entry['encoded'] = content
            entry['post_date'] = datetime.datetime.strptime(item.findtext(wpns+'post_date'),"%Y-%m-%d %H:%M:%S")
            
            cats=item.findall('category')
            for cat in cats:
                if cat.attrib.has_key('nicename'):
                    cat_type=cat.attrib['domain']
                    if cat_type=='category':
                        entry['categories']=cat.text
            #
            tmps = item.findall(wpns+'postmeta')
            for tmp in tmps:
                t = tmp.findtext(wpns+'meta_key')
                if t =='views':
                    entry['views'] = int(tmp.findtext(wpns+'meta_value'))
            #
            pub_status=item.findtext(wpns+'status')
            if pub_status=='publish':
                pub_n += 1
                art = Article.all().filter('title =', entry['title']).get()
                if art:
                    articlecontent = ArticleContent.get_by_key_name( "key_%d"%art.key().id())
                    if articlecontent is None:
                        articlecontent = ArticleContent(key_name = "key_%d"%(art.key().id()), content = entry['encoded'])
                        articlecontent.put()
                        additems.append(entry['title'])
                        upd_n += 1
                    #
                else:
                    additems.append(entry['title'])
                    cate_k = Categories.all().filter('name =', entry['categories']).get().key()
                    art = Article(cate = cate_k, title = entry['title'],browse = entry['views'] , author = request.user,pub_date = entry['post_date'])
                    art.put()
                    if art:
                        articlecontent = ArticleContent(key_name = "key_%d"%(art.key().id()), content = entry['encoded'])
                        articlecontent.put()
                    #
                    add_n += 1
        
        memcache.flush_all()
        
    return generate(request,'import_wp.html',{'additems':additems,'pub_n':pub_n,'add_n':add_n,'upd_n':upd_n})
    
def getsitemapxml(cate_list):
    try:
        current_site = Site.objects.get_current()
    except:
        current_site = RequestSite(request)
        
    # get from mem
    sitemap = memcache.get("sitemap_men_%s"%current_site.domain)
    if sitemap:
        return sitemap
    #
    urls = []
    #
    loc = "http://%s"%current_site.domain
    lastmod = "%s"%(get_now_date().strftime('%Y-%m-%dT%X+00:00'))
    changefreq = 'always'
    priority = '1.0'
    urlstr = "<url>\n<loc>%s</loc>\n<lastmod>%s</lastmod>\n<changefreq>%s</changefreq>\n<priority>%s</priority>\n</url>\n"%(loc,lastmod,changefreq,priority)
    urls.append(urlstr)
    #
    loc = "http://%s/cms/guestbook_1.html" %current_site.domain
    lastmod = "%s"%(get_now_date().strftime('%Y-%m-%dT%X+00:00'))
    changefreq = 'always'
    priority = '1.0'
    urlstr = "<url>\n<loc>%s</loc>\n<lastmod>%s</lastmod>\n<changefreq>%s</changefreq>\n<priority>%s</priority>\n</url>\n"%(loc,lastmod,changefreq,priority)
    urls.append(urlstr)    
    #
    
    for cate in cate_list:
        ##get cate
        loc = "http://%s/cms/show_categories/%d_1.html" % (current_site.domain, cate.key().id())
        lastmod = "%s"%(get_now_date().strftime('%Y-%m-%dT%X+00:00'))
        changefreq = 'daily'
        priority = '0.6'
        urlstr = "<url>\n<loc>%s</loc>\n<lastmod>%s</lastmod>\n<changefreq>%s</changefreq>\n<priority>%s</priority>\n</url>\n"%(loc,lastmod,changefreq,priority)
        urls.append(urlstr)
        ##get cate art
        cate_arts = get_cat_art(cate.key().id(),1)[0]
        for art in cate_arts:
            loc = "http://%s/cms/show_article/%d.html" % (current_site.domain, art.key().id())
            lastmod = "%s"%(art.EST_time().strftime('%Y-%m-%dT%X+00:00'))
            changefreq = 'daily'
            priority = '0.5'
            urlstr = "<url>\n<loc>%s</loc>\n<lastmod>%s</lastmod>\n<changefreq>%s</changefreq>\n<priority>%s</priority>\n</url>\n"%(loc,lastmod,changefreq,priority)
            urls.append(urlstr)
    #####
    sitemap = ''.join(urls)
    memcache.add("sitemap_men_%s"%current_site.domain, sitemap, memtime/2)
    return sitemap

def sitemap(request):
    cate_list = get_categories()    
    xmlbody = getsitemapxml(cate_list)
    return render_to_response(request,'sitemap.xml',{'xml':xmlbody})

def robots(request):
    try:
        current_site = Site.objects.get_current()
    except:
        current_site = RequestSite(request)
    return render_to_response(request,'robots.txt',{'current_site_domain':current_site.domain})

def rsslatest(request,cate_id):
    try:
        current_site = Site.objects.get_current()
    except:
        current_site = RequestSite(request) 
    baseurl = "http://%s"%current_site.domain
    site_name = base_values['site_name']
    cate_id = int(cate_id)
    if cate_id != 0:
        cate = Categories.get_by_id(cate_id)
    else:
        cate = None
    last_updated = get_now_date()#datetime.datetime.now()
    admin_user = User.get_by_key_name( "admin" )
    owner_name = u"%s %s"%(admin_user.first_name,admin_user.last_name)
    if cate:
        arts_title = get_cat_art(cate_id, 1)[0]
        #arts_title = get_cat_art2(cate_id, 10)
        subtitle = cate.name
        feedurl = "rss/latest/%d"%cate_id
    else:
        arts_title = get_new_art(20)
        subtitle = site_name
        feedurl = "rss/latest/0"
    #
    now_time = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    xml_list = []
    xml_list.append(u'<?xml version="1.0" encoding="UTF-8"?> \n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n<atom:link href="%s%s" rel="self" type="application/rss+xml" /> \n'%( baseurl, reverse('cms.views.rsslatest', kwargs=dict(cate_id=cate_id))))
    (u' xmlns:atom="http://www.w3.org/2005/Atom"')
    head_str = u'<title>%s</title> \n<link>%s</link> \n<description>%s Latest Articles</description> \n<language>en-us</language> \n<copyright>Copyright (C) %s. All rights reserved.</copyright> \n<pubDate>%s</pubDate> \n<lastBuildDate>%s</lastBuildDate>\n<generator>%s RSS Generator</generator> \n'%(site_name,baseurl,site_name,current_site.domain,now_time,now_time,current_site.domain)
    xml_list.append(head_str)
    
    for art in arts_title:
        art_id = art.key().id()
        art = get_art(art_id)
        con = get_art_con(art_id)
        art_time = art.pub_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        art_url = "%s/cms/show_article/%d.html"%(baseurl, art_id)
        tmp_str = u'<item> \n<title> %s </title> \n<link>%s</link> \n<guid>%s</guid> \n<description><![CDATA[%s [...<a href="%s" target="_blank">More</a>...]]]></description> \n<category>%s</category> \n<author>%s(%s)</author> \n<pubDate>%s</pubDate>  \n</item> \n'%(art.title, art_url, art_url, con.content[:300], art_url, art.cate.name, art.author.email,owner_name, art_time)
        xml_list.append(tmp_str)
    xml_list.append(u'</channel>\n</rss>\n')
    xmlbody = ''.join(xml_list)
    
    return HttpResponse(xmlbody,content_type='application/rss+xml')
    