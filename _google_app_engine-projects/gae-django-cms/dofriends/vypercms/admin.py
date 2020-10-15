from django.contrib import admin
from models import StyleSheet, Title, Head, Template, Page, Domain

class StyleSheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', )

admin.site.register(StyleSheet, StyleSheetAdmin)

class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', )

admin.site.register(Title, TitleAdmin)

class HeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', )

admin.site.register(Head, HeadAdmin)

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', )

admin.site.register(Template, TemplateAdmin)

class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', )

admin.site.register(Domain, DomainAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'title', 'timestamp', )

admin.site.register(Page, PageAdmin)

