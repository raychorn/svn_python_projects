from django.contrib import admin

from models import Content
from models import Country
from models import MenuType
from models import Role
from models import SiteName
from models import SnippetType
from models import Snippet
from models import State
from models import URL
from models import UserActivity
from models import User
from models import Site

from vyperlogix.html import myOOHTML as oohtml

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)
    
class ContentAdmin(admin.ModelAdmin):
    def sites_list(self,aContent):
	h = oohtml.Html()
	ol = h.tagOL()
	for item in aContent.sites.all():
	    ol.tagLI(item.name)
	return h.toHtml()
    sites_list.short_description = 'Sites'
    sites_list.allow_tags = True
    sites_list.admin_order_field = 'menutype'
    
    list_display = ('id', 'sites_list', 'menutype', 'menu_tag', 'url', 'descr', 'target', 'admin_mode')
    search_fields = ['url']
    list_filter = ('admin_mode','menutype','menu_tag')
    ordering = ['url']
    
admin.site.register(Content, ContentAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'printable_name', 'iso', 'iso3')
    search_fields = ['name']
    ordering = ['printable_name']
    
admin.site.register(Country, CountryAdmin)

class MenuTypeAdmin(admin.ModelAdmin):
    list_display = ('menutype', 'descr')
    search_fields = ['menutype']
    ordering = ['menutype']

admin.site.register(MenuType,MenuTypeAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
    ordering = ['name']
    
admin.site.register(Role,RoleAdmin)

class SiteNameAdmin(admin.ModelAdmin):
    def user_info(self,aSiteName):
	h = oohtml.Html()
	ol = h.tagUL()
	ol.tagLI('Role: %s' % (aSiteName.user.role))
	ol.tagLI('Name: %s %s' % (aSiteName.user.firstname,aSiteName.user.lastname))
	ol.tagLI('EMail: %s' % (aSiteName.user.email_address))
	ol.tagLI('%s on %s' % ('ACTIVATED' if (aSiteName.user.activated) else '~activated',aSiteName.user.activated_on))
	return h.toHtml()
    user_info.short_description = 'User'
    user_info.allow_tags = True
    
    def site_info(self,aSiteName):
	h = oohtml.Html()
	ol = h.tagUL()
	ol.tagLI('Domain: %s' % (aSiteName.site.domain))
	ol.tagLI('Name: %s' % (aSiteName.site.name))
	return h.toHtml()
    site_info.short_description = 'Site'
    site_info.allow_tags = True
    
    list_display = ('user_info','site_info')
    #search_fields = ['user',]
    list_filter = ('user','site')
    ordering = ['site']
    
admin.site.register(SiteName,SiteNameAdmin)

snippet_type_info = lambda aSnippetType:'Administrative' if (aSnippetType.admin) else 'unrestricted'

class SnippetTypeAdmin(admin.ModelAdmin):
    def admin_info(self,aSnippetType):
	return snippet_type_info(aSnippetType)
    admin_info.short_description = 'Mode'
    admin_info.allow_tags = True
    
    list_display = ('admin_info', 'snippet_type', 'descr')
    search_fields = ['descr']
    list_filter = ('admin',)
    ordering = ['snippet_type']

admin.site.register(SnippetType,SnippetTypeAdmin)

class SnippetAdmin(admin.ModelAdmin):
    def sites_list(self,aSnippet):
	h = oohtml.Html()
	ol = h.tagUL()
	for item in aSnippet.sites.all():
	    ol.tagLI(item.name)
	return h.toHtml()
    sites_list.short_description = 'Sites'
    sites_list.allow_tags = True
    sites_list.admin_order_field = 'snippet_type'
    
    def snippet_type_info(self,aSnippet):
	h = oohtml.Html()
	ol = h.tagUL()
	ol.tagLI('%s' % (snippet_type_info(aSnippet.snippet_type)))
	ol.tagLI('Descr: %s' % (aSnippet.snippet_type.descr))
	ol.tagLI('Type: %s' % (aSnippet.snippet_type.snippet_type))
	return h.toHtml()
    snippet_type_info.short_description = 'Snippet Type'
    snippet_type_info.allow_tags = True
    
    list_display = ('id','sites_list', 'snippet_type_info', 'descr', 'snippet_tag')
    search_fields = ['snippet_type']
    list_filter = ('snippet_type','snippet_tag')
    ordering = ['snippet_tag']
    
admin.site.register(Snippet,SnippetAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbrev')
    search_fields = ['name']
    ordering = ['name']
   
admin.site.register(State,StateAdmin)

class URLAdmin(admin.ModelAdmin):
    def sites_list(self,aURL):
	h = oohtml.Html()
	ol = h.tagOL()
	for item in aURL.sites.all():
	    ol.tagLI(item.name)
	return h.toHtml()
    sites_list.short_description = 'Sites'
    sites_list.allow_tags = True
    
    list_display = ('sites_list', 'url', 'descr', 'url_tag')
    search_fields = ['url']
    list_filter = ('sites','url_tag')
    ordering = ['url']
    
admin.site.register(URL,URLAdmin)

class UserActivityAdmin(admin.ModelAdmin):
    def user_info(self,aUserActivity):
	return aUserActivity.user.email_address
    user_info.short_description = 'User'
    user_info.allow_tags = True
    
    list_display = ('timestamp', 'user_info', 'ip', 'action')
    search_fields = ['email_address']
    list_filter = ('user','timestamp')
    ordering = ['-timestamp']
    
admin.site.register(UserActivity,UserActivityAdmin)

class UserAdmin(admin.ModelAdmin):
    def user_name(self,aUser):
	return '%s %s' % (aUser.firstname,aUser.lastname)
    user_name.short_description = 'name'
    user_name.allow_tags = True
    
    def activation_info(self,aUser):
	return 'ACTIVATED' if (aUser.activated) else '~activated'
    activation_info.short_description = 'Activation'
    activation_info.allow_tags = True
    
    list_display = ('role', 'user_name', 'email_address', 'activation_info', 'activated_on')
    search_fields = ['email_address']
    list_filter = ('role','activated','activated_on','state','country')
    
admin.site.register(User,UserAdmin)

