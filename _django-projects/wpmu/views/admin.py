from django.contrib import admin

from models import Site
from models import Country
from models import State
from models import UserActivity
from models import User
from models import Role

from vyperlogix.html import myOOHTML as oohtml

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)
    
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'printable_name', 'iso', 'iso3')
    search_fields = ['name']
    ordering = ['printable_name']
    
admin.site.register(Country, CountryAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbrev')
    search_fields = ['name']
    ordering = ['name']
   
admin.site.register(State,StateAdmin)

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

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
    ordering = ['name']
    
admin.site.register(Role,RoleAdmin)

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

