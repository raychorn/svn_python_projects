from django.contrib import admin

from models import Site, Document, Candidate, Cities

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('docfile','user_id')
    search_fields = ('docfile','user_id')
    ordering = ['docfile']

admin.site.register(Document, DocumentAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('fullname','phone','city','relocateable','user')
    search_fields = ('fullname','phone','city','relocateable','user')
    ordering = ['fullname','phone','city','relocateable','user']

admin.site.register(Candidate, CandidateAdmin)

class CitiesAdmin(admin.ModelAdmin):
    list_display = ('locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode')
    search_fields = ('locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode')
    ordering = ['locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode']

admin.site.register(Cities, CitiesAdmin)
