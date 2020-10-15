from django.contrib import admin

from models import Site

from vyperlogix.html import myOOHTML as oohtml

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)

from models import Json

class JSonAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'uuid')
    search_fields = ('name', 'state', 'uuid')
    ordering = ['name']

admin.site.register(Json, JSonAdmin)
    
from models import Protocols

class ProtocolsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'uuid')
    search_fields = ('name', 'value', 'uuid')
    ordering = ['name']

admin.site.register(Protocols, ProtocolsAdmin)
    
from models import Environments

class EnvironmentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    search_fields = ('name', 'uuid')
    ordering = ['name']

admin.site.register(Environments, EnvironmentsAdmin)
