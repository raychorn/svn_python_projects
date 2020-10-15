from django.contrib import admin

from models import Site, GitHubUser, Document

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    ordering = ['domain']

admin.site.register(Site, SiteAdmin)

class GitHubUserAdmin(admin.ModelAdmin):
    list_display = ('username','user')
    search_fields = ('username','user')
    ordering = ['username']

admin.site.register(GitHubUser, GitHubUserAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('docfile','user')
    search_fields = ('docfile','user')
    ordering = ['docfile']

admin.site.register(Document, DocumentAdmin)

