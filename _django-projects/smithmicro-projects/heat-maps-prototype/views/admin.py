from django.contrib import admin

from models import Site

from vyperlogix.html import myOOHTML as oohtml

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)

