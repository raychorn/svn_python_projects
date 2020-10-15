from django.contrib import admin

from models import Site
from models import QuoteContact, Cities

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)


class QuoteContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone')
    search_fields = ('name','email','phone')
    ordering = ['name','email','phone']

admin.site.register(QuoteContact, QuoteContactAdmin)

class CitiesAdmin(admin.ModelAdmin):
    list_display = ('locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode')
    search_fields = ('locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode')
    ordering = ['locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode']

admin.site.register(Cities, CitiesAdmin)
