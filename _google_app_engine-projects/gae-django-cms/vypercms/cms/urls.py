# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('cms.views',
    (r'^$', 'index_page'),
    (r'^picasa.html$', 'picasa'),
    (r'^show_art_random.html$', 'show_art_random'),
    #
    (r'^photo_upload.html$', 'photo_upload'),
    (r'^photo_upload_done/(?P<key>.+)$', 'photo_upload_done'),
    (r'^photo_show/(?P<key>.+)\.jpg$', 'photo_show'),
    #
    (r'^list_globalvar$', 'list_globalvar'),
    (r'^add_globalvar$', 'add_globalvar'),
    (r'^edit_globalvar/(?P<key>.+)$', 'edit_globalvar'),
    (r'^delete_globalvar/(?P<key>.+)$', 'delete_globalvar'),
    #
    (r'^list_allad$', 'list_allad'),
    (r'^add_allad$', 'add_allad'),
    (r'^edit_allad/(?P<key>.+)$', 'edit_allad'),
    (r'^delete_allad/(?P<key>.+)$', 'delete_allad'), 
    #
    (r'^list_links$', 'list_links'),
    (r'^add_links$', 'add_links'),
    (r'^edit_links/(?P<key>.+)$', 'edit_links'),
    (r'^delete_links/(?P<key>.+)$', 'delete_links'),  
    #
    (r'^list_redirect$', 'list_redirect'),
    (r'^add_redirect$', 'add_redirect'),
    (r'^edit_redirect/(?P<key>.+)$', 'edit_redirect'),
    (r'^delete_redirect/(?P<key>.+)$', 'delete_redirect'),         
    #
    (r'^list_categories$', 'list_categories'),
    (r'^add_categories$', 'add_categories'),
    (r'^edit_categories/(?P<key>.+)$', 'edit_categories'),
    (r'^delete_categories/(?P<key>.+)/(?P<cate_key_id>.+)$', 'delete_categories'),
    (r'^show_categories/(?P<keyid>.+)_(?P<page>.+)\.html$', 'show_categories'),
    #
    (r'^add_article$', 'add_article'),
    (r'^list_article$', 'list_article'),
    (r'^my_article$', 'list_my_article'),
    (r'^show_article/(?P<keyid>.+)\.html$', 'show_article'),
    (r'^edit_article/(?P<keyid>.+)$', 'edit_article'),
    (r'^delete_article/(?P<keyid>.+)$', 'delete_article'),
    (r'^delete_comment/(?P<key>.+)$', 'delete_comment'),
    (r'^list_comment$', 'list_comment'),
    #
    (r'^globalvar_change$', 'globalvar_change'),
    (r'^allad_change$', 'allad_change'),
    (r'^links_change$', 'links_change'),
    (r'^categories_change$', 'categories_change'),
    (r'^categories_change_del/(?P<cate_key>.+)/(?P<cate_key_id>.+)$', 'categories_change_del'),
    #
    (r'^emptymem$', 'emptymem'),
    (r'^import_wp$', 'import_wp'),
    (r'^settheme$', 'settheme'),
    #
    (r'^tag/(?P<tag>.+)$', 'show_tag_arts_list'),
)
