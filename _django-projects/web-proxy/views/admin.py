from django.contrib import admin

from models import Site, GeonosisClass, GeonosisObject

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)


class GeonosisClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']

admin.site.register(GeonosisClass, GeonosisClassAdmin)


class GeonosisObjectAdmin(admin.ModelAdmin):
    list_display = ('cid', 'key', 'value')
    search_fields = ('cid', 'key', 'value')
    ordering = ['cid', 'key', 'value']

admin.site.register(GeonosisObject, GeonosisObjectAdmin)
