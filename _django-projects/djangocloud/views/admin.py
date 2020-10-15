from django.contrib import admin

from models import Site, DjangoApplication, DjangoServer

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)

class DjangoApplicationAdmin(admin.ModelAdmin):
    list_display = ('name','user')
    search_fields = ('name','user')
    ordering = ['name']

admin.site.register(DjangoApplication, DjangoApplicationAdmin)

class DjangoServerAdmin(admin.ModelAdmin):
    list_display = ('servername','user')
    search_fields = ('servername','user')
    ordering = ['servername']

admin.site.register(DjangoServer, DjangoServerAdmin)
